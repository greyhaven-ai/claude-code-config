#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["psutil"]
# ///
"""
Performance Regression Detector Hook
====================================
Type: PostToolUse
Description: Detects performance regressions by running micro-benchmarks on changed functions

This hook identifies performance-critical code changes and runs quick benchmarks
to detect regressions before they reach production.
"""

import json
import sys
import subprocess
import re
import ast
from pathlib import Path
from typing import List, Dict, Optional
import tempfile


def extract_functions_from_diff(
    old_content: str, new_content: str, language: str
) -> List[Dict]:
    """Extract function changes from diff"""
    functions = []

    if language == "python":
        try:
            # Parse old and new AST
            old_tree = ast.parse(old_content) if old_content else None
            new_tree = ast.parse(new_content) if new_content else None

            # Extract function definitions
            old_funcs = {}
            new_funcs = {}

            if old_tree:
                for node in ast.walk(old_tree):
                    if isinstance(node, ast.FunctionDef):
                        old_funcs[node.name] = (
                            ast.unparse(node) if hasattr(ast, "unparse") else None
                        )

            if new_tree:
                for node in ast.walk(new_tree):
                    if isinstance(node, ast.FunctionDef):
                        new_funcs[node.name] = (
                            ast.unparse(node) if hasattr(ast, "unparse") else None
                        )

            # Find modified functions
            for func_name in new_funcs:
                if (
                    func_name in old_funcs
                    and old_funcs[func_name] != new_funcs[func_name]
                ):
                    functions.append(
                        {
                            "name": func_name,
                            "language": "python",
                            "old": old_funcs[func_name],
                            "new": new_funcs[func_name],
                        }
                    )
        except Exception:
            pass

    elif language in ["javascript", "typescript"]:
        # Simple regex-based extraction for JS/TS
        old_func_pattern = r"(?:function\s+(\w+)|const\s+(\w+)\s*=.*=>)"
        new_func_pattern = old_func_pattern

        old_matches = re.findall(old_func_pattern, old_content) if old_content else []
        new_matches = re.findall(new_func_pattern, new_content) if new_content else []

        # Extract function names
        old_names = set(m[0] or m[1] for m in old_matches)
        new_names = set(m[0] or m[1] for m in new_matches)

        # Find modified functions
        for name in new_names.intersection(old_names):
            functions.append(
                {
                    "name": name,
                    "language": language,
                    "old": None,  # Would need more complex parsing
                    "new": None,
                }
            )

    return functions


def identify_performance_patterns(content: str, language: str) -> List[str]:
    """Identify performance-sensitive patterns in code"""
    patterns = []

    # Common performance anti-patterns
    antipatterns = {
        "python": [
            (r"for.*in.*for.*in", "nested_loops"),
            (r"\.append\(.*\).*for", "list_comprehension_candidate"),
            (r"sum\(\[.*\]\)", "sum_with_list_comprehension"),
            (r"\+\s*=.*loop", "string_concatenation_in_loop"),
            (r"global\s+\w+", "global_variable_access"),
        ],
        "javascript": [
            (r"for.*for", "nested_loops"),
            (r"document\.querySelector.*for", "dom_query_in_loop"),
            (r"\.push\(.*\).*for", "array_push_in_loop"),
            (r"JSON\.parse.*JSON\.stringify", "deep_clone_inefficient"),
        ],
    }

    language_patterns = antipatterns.get(language, [])

    for pattern, name in language_patterns:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            patterns.append(name)

    return patterns


def create_micro_benchmark(
    func_name: str, language: str, file_path: str
) -> Optional[Dict]:
    """Create a micro-benchmark for a function"""

    if language != "python":
        # Currently only supporting Python benchmarks
        return None

    try:
        # Create a simple benchmark
        benchmark_code = f"""
import sys
import timeit
import importlib.util

# Load the module
spec = importlib.util.spec_from_file_location("module", "{file_path}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Benchmark the function
if hasattr(module, '{func_name}'):
    # Create a simple test case
    setup = '''
from __main__ import module
import random
# Setup test data
test_data = [random.random() for _ in range(100)]
    '''
    
    stmt = f'''
# Call the function with test data
try:
    if module.{func_name}.__code__.co_argcount == 0:
        module.{func_name}()
    elif module.{func_name}.__code__.co_argcount == 1:
        module.{func_name}([1, 2, 3])
    else:
        pass  # Skip functions with multiple arguments
except:
    pass
    '''
    
    # Run benchmark
    times = timeit.repeat(stmt, setup, repeat=3, number=1000)
    avg_time = sum(times) / len(times)
    print(avg_time)
else:
    print(-1)
"""

        # Write benchmark to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(benchmark_code)
            benchmark_file = f.name

        # Run benchmark
        result = subprocess.run(
            ["python", benchmark_file], capture_output=True, text=True, timeout=5
        )

        # Clean up
        Path(benchmark_file).unlink()

        if result.returncode == 0 and result.stdout:
            time_ms = float(result.stdout.strip()) * 1000
            if time_ms > 0:
                return {"function": func_name, "time_ms": time_ms, "iterations": 1000}
    except Exception:
        pass

    return None


def analyze_complexity(content: str, language: str) -> Dict[str, int]:
    """Analyze code complexity metrics"""
    metrics = {
        "lines": len(content.splitlines()),
        "loops": 0,
        "conditionals": 0,
        "function_calls": 0,
    }

    # Count loops
    loop_patterns = [
        r"\bfor\b",
        r"\bwhile\b",
        r"\.forEach",
        r"\.map",
        r"\.filter",
        r"\.reduce",
    ]
    for pattern in loop_patterns:
        metrics["loops"] += len(re.findall(pattern, content))

    # Count conditionals
    conditional_patterns = [
        r"\bif\b",
        r"\belse\b",
        r"\belif\b",
        r"\bswitch\b",
        r"\?.*:",
    ]
    for pattern in conditional_patterns:
        metrics["conditionals"] += len(re.findall(pattern, content))

    # Count function calls (approximate)
    metrics["function_calls"] = len(re.findall(r"\w+\s*\(", content))

    # Calculate cyclomatic complexity (simplified)
    metrics["complexity"] = 1 + metrics["conditionals"] + metrics["loops"]

    return metrics


def compare_performance_metrics(old_metrics: Dict, new_metrics: Dict) -> Dict:
    """Compare performance metrics between old and new code"""
    comparison = {}

    for key in new_metrics:
        if key in old_metrics:
            old_val = old_metrics[key]
            new_val = new_metrics[key]

            if old_val > 0:
                change_pct = ((new_val - old_val) / old_val) * 100
                comparison[key] = {
                    "old": old_val,
                    "new": new_val,
                    "change_pct": change_pct,
                }

    return comparison


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process for Edit tools
        if tool_name not in ["Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        old_content = tool_input.get("old_string", "")
        new_content = tool_input.get("new_string", "")

        if not file_path or not new_content:
            sys.exit(0)

        # Detect language
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
        }

        language = language_map.get(ext, "unknown")

        if language == "unknown":
            sys.exit(0)

        # Analyze complexity
        old_metrics = analyze_complexity(old_content, language) if old_content else {}
        new_metrics = analyze_complexity(new_content, language)

        # Compare metrics
        comparison = (
            compare_performance_metrics(old_metrics, new_metrics) if old_metrics else {}
        )

        # Identify performance patterns
        patterns = identify_performance_patterns(new_content, language)

        # Extract modified functions
        functions = extract_functions_from_diff(old_content, new_content, language)

        # Run micro-benchmarks for Python functions
        benchmark_results = []
        if language == "python" and functions:
            for func in functions[:3]:  # Limit to 3 functions
                result = create_micro_benchmark(func["name"], language, file_path)
                if result:
                    benchmark_results.append(result)

        # Generate output
        output_parts = []
        has_issues = False

        output_parts.append("=" * 60)
        output_parts.append("⚡ Performance Analysis")
        output_parts.append("=" * 60)

        # Complexity changes
        if comparison:
            output_parts.append("\n📊 Complexity Metrics:")
            for metric, values in comparison.items():
                change = values["change_pct"]
                if metric == "complexity" and change > 20:
                    output_parts.append(
                        f"  ⚠️  {metric}: {values['old']} → {values['new']} (+{change:.1f}%)"
                    )
                    has_issues = True
                elif change > 50:
                    output_parts.append(
                        f"  ⚠️  {metric}: {values['old']} → {values['new']} (+{change:.1f}%)"
                    )
                    has_issues = True
                else:
                    emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
                    output_parts.append(
                        f"  {emoji} {metric}: {values['old']} → {values['new']} ({change:+.1f}%)"
                    )

        # Performance patterns
        if patterns:
            output_parts.append("\n⚠️  Performance Patterns Detected:")
            for pattern in patterns:
                pattern_name = pattern.replace("_", " ").title()
                output_parts.append(f"  • {pattern_name}")
                has_issues = True

        # Benchmark results
        if benchmark_results:
            output_parts.append("\n⏱️  Micro-benchmark Results:")
            for result in benchmark_results:
                output_parts.append(
                    f"  • {result['function']}(): {result['time_ms']:.3f}ms per 1000 calls"
                )

        # Recommendations
        if has_issues:
            output_parts.append("\n💡 Performance Recommendations:")

            if "nested_loops" in patterns:
                output_parts.append(
                    "  • Consider using vectorized operations or optimized algorithms"
                )

            if "list_comprehension_candidate" in patterns:
                output_parts.append(
                    "  • Use list comprehensions instead of append in loops"
                )

            if "dom_query_in_loop" in patterns:
                output_parts.append("  • Cache DOM queries outside of loops")

            if comparison.get("complexity", {}).get("change_pct", 0) > 20:
                output_parts.append("  • Consider breaking down complex functions")

            output_parts.append("\n🔧 Tools to help:")

            if language == "python":
                output_parts.append("  • Profile with: python -m cProfile")
                output_parts.append("  • Line profiler: pip install line_profiler")
            elif language in ["javascript", "typescript"]:
                output_parts.append("  • Use Chrome DevTools Performance tab")
                output_parts.append("  • Consider: npm install benchmark")
        else:
            output_parts.append("\n✅ No significant performance concerns detected")

        output_parts.append("=" * 60)

        # Print analysis
        print("\n".join(output_parts))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Performance detector error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

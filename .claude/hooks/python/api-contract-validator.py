#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["jsonschema", "pyyaml", "openapi-spec-validator"]
# ///
"""
API Contract Validator Hook
===========================
Type: PreToolUse (Edit)
Description: Validates API changes against OpenAPI/Swagger specifications

This hook ensures API endpoints remain compliant with their documented
contracts, preventing breaking changes and maintaining consistency.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPISpecValidatorError


def find_openapi_spec(project_dir: str) -> Optional[Path]:
    """Find OpenAPI/Swagger specification file"""
    spec_patterns = [
        "openapi.yaml",
        "openapi.yml",
        "openapi.json",
        "swagger.yaml",
        "swagger.yml",
        "swagger.json",
        "api.yaml",
        "api.yml",
        "api.json",
        "docs/api.yaml",
        "docs/openapi.yaml",
        "spec/openapi.yaml",
        "api/openapi.yaml",
    ]

    project_path = Path(project_dir)
    for pattern in spec_patterns:
        spec_path = project_path / pattern
        if spec_path.exists():
            return spec_path

    # Search recursively for any OpenAPI file
    for spec_file in project_path.rglob("*openapi*.y*ml"):
        return spec_file
    for spec_file in project_path.rglob("*swagger*.y*ml"):
        return spec_file

    return None


def load_openapi_spec(spec_path: Path) -> Optional[Dict]:
    """Load and validate OpenAPI specification"""
    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            if spec_path.suffix in [".yaml", ".yml"]:
                spec = yaml.safe_load(f)
            else:
                spec = json.load(f)

        # Basic validation
        validate_spec(spec)
        return spec

    except (yaml.YAMLError, json.JSONDecodeError, OpenAPISpecValidatorError) as e:
        print(f"⚠️  Invalid OpenAPI spec: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️  Error loading spec: {e}", file=sys.stderr)
        return None


def extract_api_endpoints_from_code(content: str, language: str) -> List[Dict]:
    """Extract API endpoint definitions from code"""
    endpoints = []

    if language == "python":
        # Flask patterns
        flask_patterns = [
            r'@app\.route\([\'"]([^\'"\s]+)[\'"].*?methods=\[([^\]]+)\]',
            r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"\s]+)[\'"]',
        ]

        for pattern in flask_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                if len(match) == 2 and "." in match[0]:
                    method = match[0].upper()
                    path = match[1]
                else:
                    methods = match[1] if len(match) > 1 else match[0]
                    path = match[0] if len(match) > 1 else match[1]
                    method = methods.upper() if isinstance(methods, str) else "GET"

                endpoints.append({"path": path, "method": method, "framework": "flask"})

        # FastAPI patterns
        fastapi_patterns = [
            r'@(?:app|router)\.(get|post|put|delete|patch)\([\'"]([^\'"\s]+)[\'"]',
        ]

        for pattern in fastapi_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                endpoints.append(
                    {
                        "path": match[1],
                        "method": match[0].upper(),
                        "framework": "fastapi",
                    }
                )

        # Django patterns
        django_patterns = [
            r'path\([\'"]([^\'"\s]+)[\'"].*?views\.(\w+)',
        ]

        for pattern in django_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                endpoints.append(
                    {
                        "path": "/" + match[0],
                        "method": "GET",  # Default, would need more analysis
                        "framework": "django",
                    }
                )

    elif language in ["javascript", "typescript"]:
        # Express patterns
        express_patterns = [
            r'(?:app|router)\.(get|post|put|delete|patch)\([\'"]([^\'"\s]+)[\'"]',
            r'(?:app|router)\.route\([\'"]([^\'"\s]+)[\'"]\)\.(\w+)',
        ]

        for pattern in express_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                if "." in pattern:  # route().method pattern
                    endpoints.append(
                        {
                            "path": match[0],
                            "method": match[1].upper(),
                            "framework": "express",
                        }
                    )
                else:
                    endpoints.append(
                        {
                            "path": match[1],
                            "method": match[0].upper(),
                            "framework": "express",
                        }
                    )

        # Next.js API routes (file-based)
        if "/api/" in content or "pages/api" in content:
            # Extract from export default function
            if "export default" in content:
                endpoints.append(
                    {
                        "path": "/api/unknown",  # Would need file path for exact route
                        "method": "GET/POST",
                        "framework": "nextjs",
                    }
                )

    elif language == "java":
        # Spring patterns
        spring_patterns = [
            r'@(?:Get|Post|Put|Delete|Patch)Mapping\([\'"]([^\'"\s]+)[\'"]',
            r'@RequestMapping\(.*?value\s*=\s*[\'"]([^\'"\s]+)[\'"].*?method\s*=\s*RequestMethod\.(\w+)',
        ]

        for pattern in spring_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                if len(match) == 2:
                    endpoints.append(
                        {"path": match[0], "method": match[1], "framework": "spring"}
                    )
                else:
                    method = "GET"
                    if "Post" in pattern:
                        method = "POST"
                    elif "Put" in pattern:
                        method = "PUT"
                    elif "Delete" in pattern:
                        method = "DELETE"

                    endpoints.append(
                        {
                            "path": match[0] if isinstance(match, tuple) else match,
                            "method": method,
                            "framework": "spring",
                        }
                    )

    return endpoints


def validate_endpoint_against_spec(endpoint: Dict, spec: Dict) -> List[str]:
    """Validate an endpoint against OpenAPI spec"""
    violations = []

    if "paths" not in spec:
        return violations

    path = endpoint["path"]
    method = endpoint["method"].lower()

    # Convert path parameters from framework format to OpenAPI format
    # e.g., /users/:id -> /users/{id} or /users/<id> -> /users/{id}
    openapi_path = re.sub(r":(\w+)", r"{\1}", path)
    openapi_path = re.sub(r"<(\w+)>", r"{\1}", openapi_path)

    # Check if path exists in spec
    if openapi_path not in spec["paths"]:
        # Check for similar paths
        similar = [
            p for p in spec["paths"] if p.split("/")[:2] == openapi_path.split("/")[:2]
        ]
        if similar:
            violations.append(f"Path '{path}' not in spec. Similar: {similar[0]}")
        else:
            violations.append(f"Path '{path}' not documented in OpenAPI spec")
        return violations

    # Check if method exists for path
    path_spec = spec["paths"][openapi_path]
    if method not in path_spec:
        available_methods = [
            m.upper()
            for m in path_spec.keys()
            if m in ["get", "post", "put", "delete", "patch"]
        ]
        violations.append(
            f"Method {endpoint['method']} not documented for {path}. Available: {available_methods}"
        )
        return violations

    # Validate method specification
    method_spec = path_spec[method]

    # Check for required elements
    if "responses" not in method_spec:
        violations.append(f"No responses documented for {endpoint['method']} {path}")

    if "description" not in method_spec and "summary" not in method_spec:
        violations.append(f"No description for {endpoint['method']} {path}")

    return violations


def extract_request_response_models(content: str, language: str) -> Dict:
    """Extract request/response model definitions from code"""
    models = {"requests": [], "responses": []}

    if language == "python":
        # Pydantic models
        pydantic_classes = re.findall(r"class\s+(\w+)\(.*BaseModel.*?\):", content)
        models["requests"].extend(pydantic_classes)

        # TypedDict models
        typed_dicts = re.findall(r'(\w+)\s*=\s*TypedDict\([\'"](\w+)[\'"]', content)
        models["requests"].extend([td[1] for td in typed_dicts])

    elif language in ["javascript", "typescript"]:
        # TypeScript interfaces
        interfaces = re.findall(r"interface\s+(\w+)\s*{", content)
        models["requests"].extend(interfaces)

        # Type definitions
        types = re.findall(r"type\s+(\w+)\s*=\s*{", content)
        models["requests"].extend(types)

    return models


def suggest_spec_updates(endpoints: List[Dict], spec: Dict) -> List[str]:
    """Suggest updates to OpenAPI spec based on code"""
    suggestions = []

    documented_paths = set(spec.get("paths", {}).keys())

    for endpoint in endpoints:
        openapi_path = re.sub(r":(\w+)", r"{\1}", endpoint["path"])
        openapi_path = re.sub(r"<(\w+)>", r"{\1}", openapi_path)

        if openapi_path not in documented_paths:
            suggestions.append(
                f"Add documentation for: {endpoint['method']} {endpoint['path']}"
            )

    return suggestions


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process for Edit tools on API files
        if tool_name not in ["Edit", "Write", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        new_content = tool_input.get("new_string", "") or tool_input.get("content", "")

        if not file_path or not new_content:
            sys.exit(0)

        # Check if this is an API-related file
        api_indicators = ["api", "route", "endpoint", "controller", "views", "handlers"]
        if not any(indicator in file_path.lower() for indicator in api_indicators):
            # Also check content for API patterns
            if not any(
                pattern in new_content
                for pattern in ["@app.route", "@router", "@app.", "router.", "Mapping"]
            ):
                sys.exit(0)

        # Get project directory
        project_dir = data.get("project_dir", ".")

        # Find OpenAPI spec
        spec_path = find_openapi_spec(project_dir)

        if not spec_path:
            # No spec found - provide guidance
            print("=" * 60)
            print("📋 API Contract Validator")
            print("=" * 60)
            print("⚠️  No OpenAPI/Swagger specification found")
            print("\n💡 Consider adding an OpenAPI spec for:")
            print("   • API documentation")
            print("   • Contract validation")
            print("   • Client SDK generation")
            print("\nCreate 'openapi.yaml' in your project root")
            print("=" * 60)
            sys.exit(0)

        # Load spec
        spec = load_openapi_spec(spec_path)
        if not spec:
            sys.exit(0)

        # Detect language
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
        }

        language = language_map.get(ext, "unknown")

        # Extract endpoints from code
        endpoints = extract_api_endpoints_from_code(new_content, language)

        if not endpoints:
            sys.exit(0)

        # Validate endpoints
        all_violations = []
        for endpoint in endpoints:
            violations = validate_endpoint_against_spec(endpoint, spec)
            if violations:
                all_violations.extend(violations)

        # Extract models
        models = extract_request_response_models(new_content, language)

        # Generate suggestions
        suggestions = suggest_spec_updates(endpoints, spec)

        # Generate output
        if all_violations or suggestions:
            output = []
            output.append("=" * 60)
            output.append("📋 API Contract Validation")
            output.append("=" * 60)
            output.append(f"Spec: {spec_path.name}")
            output.append(
                f"OpenAPI Version: {spec.get('openapi', spec.get('swagger', 'unknown'))}"
            )
            output.append("")

            if endpoints:
                output.append(f"🔍 Found {len(endpoints)} endpoint(s) in code:")
                for endpoint in endpoints[:5]:
                    output.append(
                        f"   • {endpoint['method']} {endpoint['path']} ({endpoint['framework']})"
                    )
                if len(endpoints) > 5:
                    output.append(f"   ... and {len(endpoints) - 5} more")
                output.append("")

            if all_violations:
                output.append("❌ Contract Violations:")
                for violation in all_violations[:5]:
                    output.append(f"   • {violation}")
                if len(all_violations) > 5:
                    output.append(f"   ... and {len(all_violations) - 5} more")
                output.append("")

                output.append("🔧 How to fix:")
                output.append("   1. Update OpenAPI spec to match implementation")
                output.append("   2. Or adjust implementation to match spec")
                output.append(
                    "   3. Run: openapi-generator validate -i " + str(spec_path)
                )

            if suggestions:
                output.append("💡 Suggested spec updates:")
                for suggestion in suggestions[:3]:
                    output.append(f"   • {suggestion}")
                output.append("")

            if models["requests"]:
                output.append("📦 Request/Response models found:")
                for model in models["requests"][:5]:
                    output.append(f"   • {model}")
                output.append("   Consider adding these to spec components/schemas")

            output.append("")
            output.append("📚 Best Practices:")
            output.append("   • Keep spec and code in sync")
            output.append("   • Version your API properly")
            output.append("   • Document all status codes")
            output.append("   • Include request/response examples")

            output.append("=" * 60)

            # Print output
            print("\n".join(output))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"API validator error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

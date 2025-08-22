#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["sqlparse"]
# ///
"""
Database Query Analyzer Hook
============================
Type: PreToolUse (Bash)
Description: Intercepts and analyzes SQL queries for performance issues

This hook catches SQL queries in commands, analyzes them for common
performance problems, and suggests optimizations like indexes.
"""

import json
import sys
import re
import sqlparse
from typing import List, Dict, Optional


def extract_sql_from_command(command: str) -> List[str]:
    """Extract SQL queries from a bash command"""
    queries = []

    # Common patterns for SQL in commands
    patterns = [
        r'psql.*-c\s+["\']([^"\']+)["\']',  # PostgreSQL
        r'mysql.*-e\s+["\']([^"\']+)["\']',  # MySQL
        r'sqlite3.*["\']([^"\']+)["\']',  # SQLite
        r'sqlcmd.*-Q\s+["\']([^"\']+)["\']',  # SQL Server
        # Python/Node scripts with SQL
        r'"""(SELECT.*?)"""',  # Python triple quotes
        r"'''(SELECT.*?)'''",  # Python triple quotes
        r"`(SELECT.*?)`",  # JavaScript template literals
        # Direct SQL statements
        r"\b(SELECT\s+.*?FROM.*?(?:WHERE|GROUP BY|ORDER BY|LIMIT|;|$))",
        r"\b(INSERT\s+INTO.*?(?:VALUES|SELECT).*?(?:;|$))",
        r"\b(UPDATE\s+.*?SET.*?(?:WHERE|;|$))",
        r"\b(DELETE\s+FROM.*?(?:WHERE|;|$))",
        r"\b(CREATE\s+(?:TABLE|INDEX).*?(?:;|$))",
        r"\b(ALTER\s+TABLE.*?(?:;|$))",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, command, re.IGNORECASE | re.DOTALL)
        queries.extend(matches)

    # Also check for SQL files being executed
    if ".sql" in command:
        sql_file_pattern = r"[<@]\s*(\S+\.sql)"
        sql_files = re.findall(sql_file_pattern, command)
        for sql_file in sql_files:
            queries.append(f"-- SQL file: {sql_file}")

    return queries


def parse_sql_query(query: str) -> Optional[Dict]:
    """Parse SQL query and extract key components"""
    try:
        parsed = sqlparse.parse(query)[0]

        # Get query type
        query_type = parsed.get_type()

        # Extract tables
        tables = extract_tables(parsed)

        # Extract WHERE conditions
        where_conditions = extract_where_conditions(query)

        # Extract JOIN conditions
        joins = extract_joins(query)

        # Extract columns
        columns = extract_columns(query)

        return {
            "type": query_type,
            "tables": tables,
            "where_conditions": where_conditions,
            "joins": joins,
            "columns": columns,
            "raw": query,
        }

    except Exception:
        return None


def extract_tables(parsed) -> List[str]:
    """Extract table names from parsed SQL"""
    tables = []

    # Simple extraction from tokens
    from_seen = False
    for token in parsed.tokens:
        if token.ttype is None:
            if "FROM" in str(token).upper():
                from_seen = True
            elif from_seen and str(token).strip() not in (
                "",
                ",",
                "WHERE",
                "JOIN",
                "LEFT",
                "RIGHT",
                "INNER",
                "OUTER",
            ):
                # This might be a table name
                table_name = str(token).strip()
                if table_name and not table_name.startswith("("):
                    tables.append(table_name.split()[0])  # Handle aliases

    return tables


def extract_where_conditions(query: str) -> List[str]:
    """Extract WHERE clause conditions"""
    conditions = []

    where_match = re.search(
        r"WHERE\s+(.*?)(?:GROUP BY|ORDER BY|LIMIT|;|$)",
        query,
        re.IGNORECASE | re.DOTALL,
    )
    if where_match:
        where_clause = where_match.group(1)
        # Split by AND/OR
        parts = re.split(r"\s+(?:AND|OR)\s+", where_clause, flags=re.IGNORECASE)
        conditions = [part.strip() for part in parts if part.strip()]

    return conditions


def extract_joins(query: str) -> List[str]:
    """Extract JOIN clauses"""
    joins = []

    join_patterns = [
        r"((?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\s+\S+\s+ON\s+[^J]+)",
    ]

    for pattern in join_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        joins.extend(matches)

    return joins


def extract_columns(query: str) -> List[str]:
    """Extract column names from query"""
    columns = []

    # Extract from SELECT clause
    select_match = re.match(r"SELECT\s+(.*?)\s+FROM", query, re.IGNORECASE | re.DOTALL)
    if select_match:
        select_clause = select_match.group(1)
        if "*" in select_clause:
            columns.append("*")
        else:
            # Split by comma, handle aliases
            parts = select_clause.split(",")
            for part in parts:
                col = part.strip().split()[0]  # Get first word (column name)
                if col:
                    columns.append(col)

    return columns


def analyze_query_performance(parsed_query: Dict) -> List[Dict]:
    """Analyze query for performance issues"""
    issues = []

    if not parsed_query:
        return issues

    query_type = parsed_query["type"]
    parsed_query["tables"]
    where_conditions = parsed_query["where_conditions"]
    joins = parsed_query["joins"]
    columns = parsed_query["columns"]
    raw_query = parsed_query["raw"]

    # Check for SELECT *
    if query_type == "SELECT" and "*" in columns:
        issues.append(
            {
                "severity": "medium",
                "issue": "SELECT * detected",
                "suggestion": "Specify only needed columns to reduce data transfer",
                "impact": "performance",
            }
        )

    # Check for missing WHERE clause in UPDATE/DELETE
    if query_type in ["UPDATE", "DELETE"] and not where_conditions:
        issues.append(
            {
                "severity": "high",
                "issue": f"{query_type} without WHERE clause",
                "suggestion": "Add WHERE clause to avoid affecting all rows",
                "impact": "safety",
            }
        )

    # Check for LIKE with leading wildcard
    for condition in where_conditions:
        if re.search(r"LIKE\s+['\"]%", condition, re.IGNORECASE):
            issues.append(
                {
                    "severity": "high",
                    "issue": "LIKE with leading wildcard",
                    "suggestion": "Leading wildcards prevent index usage",
                    "impact": "performance",
                }
            )

    # Check for OR conditions
    if any("OR" in cond.upper() for cond in where_conditions):
        issues.append(
            {
                "severity": "medium",
                "issue": "OR conditions in WHERE clause",
                "suggestion": "Consider using UNION or IN for better performance",
                "impact": "performance",
            }
        )

    # Check for functions in WHERE clause
    for condition in where_conditions:
        if re.search(
            r"(UPPER|LOWER|SUBSTRING|DATE|YEAR|MONTH)\s*\(", condition, re.IGNORECASE
        ):
            issues.append(
                {
                    "severity": "medium",
                    "issue": "Function in WHERE clause",
                    "suggestion": "Functions on columns prevent index usage",
                    "impact": "performance",
                }
            )
            break

    # Check for JOINs without ON clause
    if joins:
        for join in joins:
            if "ON" not in join.upper():
                issues.append(
                    {
                        "severity": "high",
                        "issue": "JOIN without ON clause",
                        "suggestion": "Specify JOIN conditions to avoid cartesian product",
                        "impact": "performance",
                    }
                )

    # Check for multiple JOINs
    if len(joins) > 3:
        issues.append(
            {
                "severity": "medium",
                "issue": f"Query has {len(joins)} JOINs",
                "suggestion": "Consider denormalizing or using materialized views",
                "impact": "performance",
            }
        )

    # Check for subqueries
    if "(SELECT" in raw_query.upper():
        issues.append(
            {
                "severity": "medium",
                "issue": "Subquery detected",
                "suggestion": "Consider using JOINs or CTEs for better performance",
                "impact": "performance",
            }
        )

    # Check for DISTINCT
    if "DISTINCT" in raw_query.upper():
        issues.append(
            {
                "severity": "low",
                "issue": "DISTINCT clause used",
                "suggestion": "Ensure proper indexing or consider GROUP BY",
                "impact": "performance",
            }
        )

    # Check for lack of LIMIT in SELECT
    if (
        query_type == "SELECT"
        and "LIMIT" not in raw_query.upper()
        and not any(
            agg in raw_query.upper() for agg in ["COUNT", "SUM", "AVG", "MAX", "MIN"]
        )
    ):
        issues.append(
            {
                "severity": "low",
                "issue": "No LIMIT clause in SELECT",
                "suggestion": "Consider adding LIMIT for large result sets",
                "impact": "performance",
            }
        )

    return issues


def suggest_indexes(parsed_query: Dict) -> List[str]:
    """Suggest indexes based on query analysis"""
    suggestions = []

    if not parsed_query:
        return suggestions

    tables = parsed_query["tables"]
    where_conditions = parsed_query["where_conditions"]
    joins = parsed_query["joins"]

    # Suggest indexes for WHERE conditions
    for condition in where_conditions:
        # Extract column name from condition
        col_match = re.match(r"(\w+)\s*[=<>]", condition)
        if col_match:
            column = col_match.group(1)
            if tables:
                suggestions.append(
                    f"CREATE INDEX idx_{tables[0]}_{column} ON {tables[0]}({column});"
                )

    # Suggest indexes for JOIN conditions
    for join in joins:
        # Extract JOIN columns
        on_match = re.search(
            r"ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)", join, re.IGNORECASE
        )
        if on_match:
            table1, col1, table2, col2 = on_match.groups()
            suggestions.append(f"CREATE INDEX idx_{table1}_{col1} ON {table1}({col1});")
            suggestions.append(f"CREATE INDEX idx_{table2}_{col2} ON {table2}({col2});")

    # Remove duplicates
    suggestions = list(set(suggestions))

    return suggestions


def check_for_n_plus_one(command: str, queries: List[str]) -> bool:
    """Check for potential N+1 query problems"""
    # Look for patterns like loops with queries inside
    loop_patterns = [
        r"for.*in.*do.*(?:psql|mysql|sqlite)",
        r"while.*do.*(?:psql|mysql|sqlite)",
        r"\.forEach.*(?:query|execute)",
        r"for.*:\s*#.*(?:SELECT|INSERT|UPDATE|DELETE)",
    ]

    for pattern in loop_patterns:
        if re.search(pattern, command, re.IGNORECASE | re.DOTALL):
            return True

    # Check for multiple similar queries
    if len(queries) > 5:
        # Check if queries are similar (potential N+1)
        if all("SELECT" in q.upper() for q in queries[:5]):
            return True

    return False


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process for Bash commands
        if tool_name != "Bash":
            sys.exit(0)

        command = tool_input.get("command", "")

        if not command:
            sys.exit(0)

        # Extract SQL queries from command
        queries = extract_sql_from_command(command)

        if not queries:
            sys.exit(0)

        # Analyze each query
        all_issues = []
        all_suggestions = []

        for query in queries[:5]:  # Limit to first 5 queries
            if query.startswith("--"):
                continue  # Skip file references

            parsed = parse_sql_query(query)
            if parsed:
                issues = analyze_query_performance(parsed)
                all_issues.extend(issues)

                suggestions = suggest_indexes(parsed)
                all_suggestions.extend(suggestions)

        # Check for N+1 problems
        has_n_plus_one = check_for_n_plus_one(command, queries)

        # Generate output
        if all_issues or all_suggestions or has_n_plus_one:
            output = []
            output.append("=" * 60)
            output.append("🔍 Database Query Analysis")
            output.append("=" * 60)

            if queries:
                output.append(f"\n📝 Found {len(queries)} SQL query(ies)")
                for query in queries[:2]:
                    if len(query) > 100:
                        display_query = query[:100] + "..."
                    else:
                        display_query = query
                    output.append(f"   {display_query}")

            if has_n_plus_one:
                output.append("\n⚠️  N+1 Query Problem Detected!")
                output.append("   Queries in loops can cause performance issues")
                output.append("   Consider:")
                output.append("   • Batch queries using IN clause")
                output.append("   • Use JOIN to fetch related data")
                output.append("   • Implement eager loading")

            if all_issues:
                # Group by severity
                high_issues = [i for i in all_issues if i["severity"] == "high"]
                medium_issues = [i for i in all_issues if i["severity"] == "medium"]
                low_issues = [i for i in all_issues if i["severity"] == "low"]

                if high_issues:
                    output.append("\n🔴 High Priority Issues:")
                    for issue in high_issues[:3]:
                        output.append(f"   • {issue['issue']}")
                        output.append(f"     → {issue['suggestion']}")

                if medium_issues:
                    output.append("\n🟡 Medium Priority Issues:")
                    for issue in medium_issues[:3]:
                        output.append(f"   • {issue['issue']}")
                        output.append(f"     → {issue['suggestion']}")

                if low_issues:
                    output.append("\n🟢 Optimization Opportunities:")
                    for issue in low_issues[:2]:
                        output.append(f"   • {issue['issue']}")

            if all_suggestions:
                output.append("\n💡 Suggested Indexes:")
                for suggestion in list(set(all_suggestions))[:3]:
                    output.append(f"   {suggestion}")
                output.append("\n   ⚠️  Test indexes in development first!")

            output.append("\n📚 Query Optimization Tips:")
            output.append("   • Use EXPLAIN/EXPLAIN ANALYZE to understand query plans")
            output.append("   • Monitor slow query logs")
            output.append("   • Keep statistics updated (ANALYZE/VACUUM)")
            output.append("   • Consider query result caching")

            output.append("=" * 60)

            # Print output
            print("\n".join(output))

            # If there are high severity issues, return exit code 2 for feedback
            if any(
                i["severity"] == "high" and i["impact"] == "safety" for i in all_issues
            ):
                print("\n⛔ Blocking dangerous query! Please review.", file=sys.stderr)
                sys.exit(2)

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Query analyzer error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

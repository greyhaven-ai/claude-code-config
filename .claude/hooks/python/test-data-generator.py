#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["faker"]
# ///
"""
Test Data Generator Hook
========================
Type: UserPromptSubmit
Description: Generates realistic test data when writing tests

This hook detects when you're writing tests and automatically generates
appropriate test data using domain-specific patterns.
"""

import json
import sys
import re
from typing import List, Dict, Any
from faker import Faker
import random
from datetime import datetime

# Initialize Faker
fake = Faker()


def detect_test_context(prompt: str) -> Dict[str, Any]:
    """Detect what kind of test data is needed from the prompt"""
    prompt_lower = prompt.lower()
    context = {"is_test": False, "data_types": [], "domain": None, "quantity": 1}

    # Check if this is test-related
    test_indicators = ["test", "spec", "mock", "fixture", "sample", "example", "dummy"]
    if any(indicator in prompt_lower for indicator in test_indicators):
        context["is_test"] = True

    # Detect data types needed
    data_patterns = {
        "user": ["user", "account", "profile", "customer", "person"],
        "product": ["product", "item", "sku", "inventory", "catalog"],
        "order": ["order", "purchase", "transaction", "cart", "checkout"],
        "payment": ["payment", "billing", "invoice", "subscription"],
        "address": ["address", "location", "shipping", "delivery"],
        "company": ["company", "organization", "business", "vendor"],
        "email": ["email", "message", "notification"],
        "api": ["api", "endpoint", "request", "response"],
        "database": ["database", "table", "record", "row"],
        "file": ["file", "document", "upload", "attachment"],
    }

    for data_type, keywords in data_patterns.items():
        if any(keyword in prompt_lower for keyword in keywords):
            context["data_types"].append(data_type)

    # Detect domain
    domain_patterns = {
        "ecommerce": ["shop", "store", "cart", "product", "order"],
        "social": ["post", "comment", "like", "follow", "share"],
        "finance": ["account", "transaction", "balance", "payment"],
        "healthcare": ["patient", "appointment", "prescription", "medical"],
        "education": ["student", "course", "grade", "enrollment"],
    }

    for domain, keywords in domain_patterns.items():
        if any(keyword in prompt_lower for keyword in keywords):
            context["domain"] = domain
            break

    # Detect quantity
    quantity_match = re.search(
        r"(\d+)\s*(?:users?|items?|records?|samples?)", prompt_lower
    )
    if quantity_match:
        context["quantity"] = min(int(quantity_match.group(1)), 100)  # Cap at 100

    return context


def generate_user_data(count: int = 1) -> List[Dict]:
    """Generate realistic user test data"""
    users = []
    for _ in range(count):
        user = {
            "id": fake.uuid4(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password": "Test123!@#",  # Static for testing
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "full_name": fake.name(),
            "phone": fake.phone_number(),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18, maximum_age=80
            ).isoformat(),
            "created_at": fake.date_time_this_year().isoformat(),
            "is_active": random.choice([True, True, True, False]),  # 75% active
            "avatar_url": f"https://avatars.example.com/{fake.uuid4()}.jpg",
            "bio": fake.text(max_nb_chars=200),
            "timezone": fake.timezone(),
            "language": random.choice(["en", "es", "fr", "de", "zh"]),
            "preferences": {
                "notifications": random.choice([True, False]),
                "newsletter": random.choice([True, False]),
                "theme": random.choice(["light", "dark", "auto"]),
            },
        }
        users.append(user)
    return users


def generate_product_data(count: int = 1) -> List[Dict]:
    """Generate realistic product test data"""
    products = []
    categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Toys"]

    for _ in range(count):
        product = {
            "id": fake.uuid4(),
            "sku": fake.ean13(),
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=500),
            "price": round(random.uniform(9.99, 999.99), 2),
            "cost": round(random.uniform(5.00, 500.00), 2),
            "category": random.choice(categories),
            "brand": fake.company(),
            "in_stock": random.choice([True, True, True, False]),
            "stock_quantity": random.randint(0, 1000),
            "weight": round(random.uniform(0.1, 50.0), 2),
            "dimensions": {
                "length": round(random.uniform(1, 100), 1),
                "width": round(random.uniform(1, 100), 1),
                "height": round(random.uniform(1, 100), 1),
            },
            "images": [
                f"https://products.example.com/{fake.uuid4()}.jpg"
                for _ in range(random.randint(1, 5))
            ],
            "tags": fake.words(nb=random.randint(2, 6)),
            "rating": round(random.uniform(1.0, 5.0), 1),
            "reviews_count": random.randint(0, 500),
            "created_at": fake.date_time_this_year().isoformat(),
            "updated_at": fake.date_time_this_month().isoformat(),
        }
        products.append(product)
    return products


def generate_order_data(count: int = 1) -> List[Dict]:
    """Generate realistic order test data"""
    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

    for _ in range(count):
        num_items = random.randint(1, 5)
        items = []
        subtotal = 0

        for _ in range(num_items):
            item_price = round(random.uniform(9.99, 199.99), 2)
            quantity = random.randint(1, 3)
            item_total = item_price * quantity
            subtotal += item_total

            items.append(
                {
                    "product_id": fake.uuid4(),
                    "product_name": fake.catch_phrase(),
                    "quantity": quantity,
                    "price": item_price,
                    "total": item_total,
                }
            )

        tax = round(subtotal * 0.08, 2)  # 8% tax
        shipping = round(random.uniform(5.00, 25.00), 2)
        total = subtotal + tax + shipping

        order = {
            "id": fake.uuid4(),
            "order_number": f"ORD-{fake.random_number(digits=8)}",
            "customer_id": fake.uuid4(),
            "customer_email": fake.email(),
            "status": random.choice(statuses),
            "items": items,
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "total": total,
            "currency": "USD",
            "payment_method": random.choice(
                ["credit_card", "paypal", "stripe", "bank_transfer"]
            ),
            "shipping_address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "zip": fake.postcode(),
                "country": fake.country_code(),
            },
            "tracking_number": fake.ean13() if random.choice([True, False]) else None,
            "notes": fake.sentence() if random.choice([True, False]) else None,
            "created_at": fake.date_time_this_month().isoformat(),
            "updated_at": fake.date_time_this_week().isoformat(),
        }
        orders.append(order)
    return orders


def generate_api_data() -> Dict:
    """Generate API request/response test data"""
    return {
        "request": {
            "method": random.choice(["GET", "POST", "PUT", "PATCH", "DELETE"]),
            "url": f"https://api.example.com/v1/{fake.word()}",
            "headers": {
                "Authorization": f"Bearer {fake.sha256()}",
                "Content-Type": "application/json",
                "X-Request-ID": fake.uuid4(),
                "User-Agent": fake.user_agent(),
            },
            "params": {
                "page": random.randint(1, 10),
                "limit": random.choice([10, 20, 50, 100]),
                "sort": random.choice(["asc", "desc"]),
                "filter": fake.word(),
            },
            "body": {
                "data": {
                    "id": fake.uuid4(),
                    "attributes": {"name": fake.name(), "value": fake.random_number()},
                }
            },
        },
        "response": {
            "status": random.choice([200, 201, 204, 400, 401, 403, 404, 500]),
            "headers": {
                "Content-Type": "application/json",
                "X-Response-ID": fake.uuid4(),
                "X-Rate-Limit": "100",
                "X-Rate-Remaining": str(random.randint(0, 100)),
            },
            "body": {
                "success": True,
                "data": [],
                "meta": {"total": random.randint(0, 1000), "page": 1, "per_page": 20},
            },
        },
    }


def generate_edge_cases(data_type: str) -> List[Any]:
    """Generate edge case test data"""
    edge_cases = {
        "string": [
            "",  # Empty string
            " ",  # Whitespace
            "a" * 1000,  # Very long string
            "你好世界",  # Unicode
            "😀🎉🚀",  # Emojis
            '<script>alert("xss")</script>',  # XSS attempt
            "'; DROP TABLE users; --",  # SQL injection
            None,  # Null
        ],
        "number": [
            0,
            -1,
            1,
            999999999,
            -999999999,
            0.1,
            -0.1,
            float("inf"),
            float("-inf"),
            None,
        ],
        "email": [
            "test@example.com",
            "test+tag@example.com",
            "test.name@example.co.uk",
            "a@b.c",
            "very.long.email.address.with.many.dots@example.com",
            "@example.com",  # Invalid
            "test@",  # Invalid
            "test",  # Invalid
            "",  # Empty
        ],
        "date": [
            datetime.now().isoformat(),
            datetime(1900, 1, 1).isoformat(),
            datetime(2099, 12, 31).isoformat(),
            "2024-02-29",  # Leap year
            "2023-02-29",  # Invalid date
            "not-a-date",  # Invalid format
            None,
        ],
    }

    return edge_cases.get(data_type, [])


def format_test_data(data: Any, language: str = "javascript") -> str:
    """Format test data for different programming languages"""
    if language == "python":
        return f"test_data = {repr(data)}"
    elif language == "javascript":
        return f"const testData = {json.dumps(data, indent=2)};"
    elif language == "typescript":
        return f"const testData: any = {json.dumps(data, indent=2)};"
    elif language == "java":
        return f"// Test data (convert to appropriate Java objects)\n/* {json.dumps(data, indent=2)} */"
    else:
        return json.dumps(data, indent=2)


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        if not prompt:
            sys.exit(0)

        # Detect test context
        context = detect_test_context(prompt)

        if not context["is_test"] and not context["data_types"]:
            sys.exit(0)

        # Generate test data
        output = []
        output.append("=" * 60)
        output.append("🧪 Test Data Generator")
        output.append("=" * 60)

        generated_data = {}

        # Generate data based on detected types
        if "user" in context["data_types"]:
            users = generate_user_data(context["quantity"])
            generated_data["users"] = users
            output.append(f"\n📤 Generated {len(users)} user(s)")

        if "product" in context["data_types"]:
            products = generate_product_data(context["quantity"])
            generated_data["products"] = products
            output.append(f"\n📦 Generated {len(products)} product(s)")

        if "order" in context["data_types"]:
            orders = generate_order_data(context["quantity"])
            generated_data["orders"] = orders
            output.append(f"\n🛒 Generated {len(orders)} order(s)")

        if "api" in context["data_types"]:
            api_data = generate_api_data()
            generated_data["api"] = api_data
            output.append("\n🌐 Generated API request/response data")

        # If no specific type detected, generate generic data
        if not generated_data and context["is_test"]:
            generated_data = {
                "sample_user": generate_user_data(1)[0],
                "sample_id": fake.uuid4(),
                "sample_email": fake.email(),
                "sample_date": fake.date_time_this_year().isoformat(),
                "sample_text": fake.text(max_nb_chars=200),
                "sample_number": random.randint(1, 100),
                "sample_boolean": random.choice([True, False]),
            }
            output.append("\n📝 Generated generic test data")

        if generated_data:
            # Format the data
            output.append("\n" + "=" * 60)
            output.append("// Copy this test data to your test file:")
            output.append("=" * 60)

            # Detect likely language from prompt
            if "python" in prompt.lower() or ".py" in prompt.lower():
                language = "python"
            elif "typescript" in prompt.lower() or ".ts" in prompt.lower():
                language = "typescript"
            elif "java" in prompt.lower():
                language = "java"
            else:
                language = "javascript"

            formatted = format_test_data(generated_data, language)
            output.append(formatted)

            # Add edge cases
            output.append("\n" + "=" * 60)
            output.append("⚠️  Don't forget edge cases:")
            output.append("=" * 60)
            output.append("• Empty values (empty string, null, undefined)")
            output.append("• Boundary values (0, -1, MAX_INT)")
            output.append("• Invalid formats (malformed email, dates)")
            output.append("• Special characters (unicode, emojis)")
            output.append("• Security tests (XSS, SQL injection attempts)")

            # Add testing tips
            output.append("\n💡 Testing Best Practices:")
            output.append("• Test both happy path and error cases")
            output.append("• Use deterministic data for reproducible tests")
            output.append("• Keep test data minimal but realistic")
            output.append("• Consider using factories for complex objects")

            output.append("=" * 60)

            # Print output
            print("\n".join(output))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Test data generator error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

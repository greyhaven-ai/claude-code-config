# Nested Validation Example

Advanced nested validation patterns with discriminated unions, recursive structures, and complex validation context.

## Goal

Master advanced validation patterns:
- Discriminated unions for polymorphic data
- Recursive validation (tree/graph structures)
- Forward references for circular dependencies
- Validation context passing
- List validation with constraints
- Complex nested object hierarchies

## Pattern 1: Discriminated Unions

### Use Case: Payment Methods

```python
# app/schemas/payment.py
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Union
from datetime import date

class CreditCardPayment(BaseModel):
    """Credit card payment method."""
    type: Literal['credit_card'] = 'credit_card'
    card_number: str = Field(..., pattern=r'^\d{16}$')
    expiry_date: str = Field(..., pattern=r'^\d{2}/\d{2}$')
    cvv: str = Field(..., pattern=r'^\d{3,4}$')

    @field_validator('expiry_date')
    @classmethod
    def validate_expiry(cls, v: str) -> str:
        month, year = v.split('/')
        if int(month) < 1 or int(month) > 12:
            raise ValueError('Invalid month')
        return v


class PayPalPayment(BaseModel):
    """PayPal payment method."""
    type: Literal['paypal'] = 'paypal'
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    account_id: str = Field(..., min_length=10)


class BankTransferPayment(BaseModel):
    """Bank transfer payment method."""
    type: Literal['bank_transfer'] = 'bank_transfer'
    account_number: str = Field(..., pattern=r'^\d{10,12}$')
    routing_number: str = Field(..., pattern=r'^\d{9}$')
    account_holder: str = Field(..., min_length=2)


# Discriminated union using type field
Payment = Union[CreditCardPayment, PayPalPayment, BankTransferPayment]


class PaymentRequest(BaseModel):
    """Payment request with discriminated union."""
    amount: float = Field(..., gt=0)
    currency: str = Field(default='USD', pattern=r'^[A-Z]{3}$')
    payment_method: Payment = Field(..., discriminator='type')

    model_config = {'validate_assignment': True}
```

### Testing Discriminated Unions

```python
# tests/test_payment_validation.py
import pytest
from pydantic import ValidationError
from app.schemas.payment import PaymentRequest

def test_credit_card_payment():
    data = {
        'amount': 100.00,
        'payment_method': {
            'type': 'credit_card',
            'card_number': '4532015112830366',
            'expiry_date': '12/25',
            'cvv': '123'
        }
    }
    payment = PaymentRequest(**data)
    assert payment.payment_method.type == 'credit_card'


def test_paypal_payment():
    data = {
        'amount': 50.00,
        'payment_method': {
            'type': 'paypal',
            'email': 'user@example.com',
            'account_id': 'PAYPAL12345'
        }
    }
    payment = PaymentRequest(**data)
    assert payment.payment_method.type == 'paypal'


def test_invalid_discriminator():
    data = {
        'amount': 100.00,
        'payment_method': {
            'type': 'invalid_type',
            'card_number': '4532015112830366'
        }
    }
    with pytest.raises(ValidationError) as exc:
        PaymentRequest(**data)
    assert 'discriminator' in str(exc.value.errors())
```

## Pattern 2: Recursive Validation

### Use Case: Comment Thread

```python
# app/schemas/comment.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class Comment(BaseModel):
    """Recursive comment with replies."""
    id: UUID
    author_id: UUID
    content: str = Field(..., min_length=1, max_length=1000)
    created_at: datetime

    # Forward reference for recursive type
    replies: List['Comment'] = Field(default_factory=list)

    @property
    def reply_count(self) -> int:
        """Total replies including nested."""
        return len(self.replies) + sum(r.reply_count for r in self.replies)

    @property
    def max_depth(self) -> int:
        """Maximum nesting depth."""
        if not self.replies:
            return 0
        return 1 + max(r.max_depth for r in self.replies)


# Required for forward references
Comment.model_rebuild()
```

### Testing Recursive Structures

```python
# tests/test_comment_validation.py
import pytest
from datetime import datetime
from uuid import uuid4
from app.schemas.comment import Comment

def test_single_comment():
    data = {
        'id': uuid4(),
        'author_id': uuid4(),
        'content': 'Top-level comment',
        'created_at': datetime.utcnow(),
        'replies': []
    }
    comment = Comment(**data)
    assert comment.reply_count == 0
    assert comment.max_depth == 0


def test_nested_comments():
    data = {
        'id': uuid4(),
        'author_id': uuid4(),
        'content': 'Top comment',
        'created_at': datetime.utcnow(),
        'replies': [
            {
                'id': uuid4(),
                'author_id': uuid4(),
                'content': 'Reply 1',
                'created_at': datetime.utcnow(),
                'replies': [
                    {
                        'id': uuid4(),
                        'author_id': uuid4(),
                        'content': 'Nested reply',
                        'created_at': datetime.utcnow(),
                        'replies': []
                    }
                ]
            }
        ]
    }
    comment = Comment(**data)
    assert comment.reply_count == 2
    assert comment.max_depth == 2
```

## Pattern 3: Validation Context

### Use Case: Conditional Validation

```python
# app/schemas/document.py
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Literal

class Document(BaseModel):
    """Document with context-aware validation."""
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    status: Literal['draft', 'review', 'published'] = 'draft'
    reviewer_notes: Optional[str] = None

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str, info: ValidationInfo) -> str:
        """Validate content based on status."""
        status = info.data.get('status', 'draft')

        if status == 'published':
            # Published documents must have substantial content
            if len(v) < 100:
                raise ValueError('Published documents must have at least 100 characters')

        if status == 'review' and len(v) < 50:
            raise ValueError('Documents under review must have at least 50 characters')

        return v

    @field_validator('reviewer_notes')
    @classmethod
    def validate_reviewer_notes(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Require reviewer notes for certain statuses."""
        status = info.data.get('status', 'draft')

        if status == 'published' and not v:
            raise ValueError('Published documents must have reviewer notes')

        return v
```

### Testing Context-Aware Validation

```python
# tests/test_document_validation.py
import pytest
from pydantic import ValidationError
from app.schemas.document import Document

def test_draft_minimal_content():
    """Draft can have minimal content."""
    data = {
        'title': 'Draft Doc',
        'content': 'Short',
        'status': 'draft'
    }
    doc = Document(**data)
    assert doc.status == 'draft'


def test_review_requires_more_content():
    """Review status requires more content."""
    data = {
        'title': 'Review Doc',
        'content': 'Too short',
        'status': 'review'
    }
    with pytest.raises(ValidationError) as exc:
        Document(**data)
    assert 'at least 50 characters' in str(exc.value.errors())


def test_published_requires_notes():
    """Published requires reviewer notes."""
    data = {
        'title': 'Published Doc',
        'content': 'A' * 150,  # Sufficient length
        'status': 'published'
        # Missing reviewer_notes
    }
    with pytest.raises(ValidationError) as exc:
        Document(**data)
    assert 'reviewer notes' in str(exc.value.errors())
```

## Pattern 4: Complex Nested Lists

### Use Case: Course Curriculum

```python
# app/schemas/course.py
from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import timedelta

class Lesson(BaseModel):
    """Individual lesson."""
    title: str = Field(..., min_length=3, max_length=100)
    duration_minutes: int = Field(..., ge=5, le=180)
    video_url: str = Field(..., pattern=r'^https://')
    resources: List[str] = Field(default_factory=list, max_length=10)


class Module(BaseModel):
    """Course module with lessons."""
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., max_length=500)
    lessons: List[Lesson] = Field(..., min_length=1, max_length=20)

    @property
    def total_duration(self) -> int:
        """Total duration in minutes."""
        return sum(lesson.duration_minutes for lesson in self.lessons)

    @field_validator('lessons')
    @classmethod
    def validate_lessons(cls, lessons: List[Lesson]) -> List[Lesson]:
        """Validate total module duration."""
        total = sum(l.duration_minutes for l in lessons)
        if total > 600:  # 10 hours max per module
            raise ValueError('Module duration cannot exceed 10 hours')
        return lessons


class Course(BaseModel):
    """Complete course with modules."""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., max_length=2000)
    modules: List[Module] = Field(..., min_length=1, max_length=12)
    price: float = Field(..., ge=0, le=999.99)

    @property
    def total_duration(self) -> int:
        """Total course duration in minutes."""
        return sum(module.total_duration for module in self.modules)

    @property
    def total_lessons(self) -> int:
        """Total lesson count."""
        return sum(len(module.lessons) for module in self.modules)

    @field_validator('modules')
    @classmethod
    def validate_modules(cls, modules: List[Module]) -> List[Module]:
        """Validate course structure."""
        total = sum(m.total_duration for m in modules)
        if total < 60:  # At least 1 hour
            raise ValueError('Course must be at least 1 hour long')
        if total > 3600:  # Max 60 hours
            raise ValueError('Course cannot exceed 60 hours')
        return modules
```

### Testing Nested Lists

```python
# tests/test_course_validation.py
import pytest
from pydantic import ValidationError
from app.schemas.course import Course

def test_valid_course():
    data = {
        'title': 'Python Fundamentals',
        'description': 'Learn Python from scratch',
        'price': 49.99,
        'modules': [
            {
                'title': 'Introduction',
                'description': 'Getting started',
                'lessons': [
                    {
                        'title': 'Welcome',
                        'duration_minutes': 10,
                        'video_url': 'https://example.com/video1',
                        'resources': []
                    },
                    {
                        'title': 'Setup',
                        'duration_minutes': 20,
                        'video_url': 'https://example.com/video2',
                        'resources': ['https://python.org']
                    }
                ]
            },
            {
                'title': 'Variables',
                'description': 'Learn about variables',
                'lessons': [
                    {
                        'title': 'Variable Basics',
                        'duration_minutes': 30,
                        'video_url': 'https://example.com/video3',
                        'resources': []
                    }
                ]
            }
        ]
    }
    course = Course(**data)
    assert course.total_lessons == 3
    assert course.total_duration == 60


def test_course_too_short():
    data = {
        'title': 'Mini Course',
        'description': 'Too short',
        'price': 9.99,
        'modules': [
            {
                'title': 'Quick Intro',
                'description': 'Brief intro',
                'lessons': [
                    {
                        'title': 'Hello',
                        'duration_minutes': 5,
                        'video_url': 'https://example.com/video',
                        'resources': []
                    }
                ]
            }
        ]
    }
    with pytest.raises(ValidationError) as exc:
        Course(**data)
    assert 'at least 1 hour' in str(exc.value.errors())


def test_module_too_long():
    lessons = [
        {
            'title': f'Lesson {i}',
            'duration_minutes': 60,
            'video_url': f'https://example.com/video{i}',
            'resources': []
        }
        for i in range(11)  # 11 hours total
    ]

    data = {
        'title': 'Course',
        'description': 'Test',
        'price': 99.99,
        'modules': [
            {
                'title': 'Long Module',
                'description': 'Too long',
                'lessons': lessons
            }
        ]
    }
    with pytest.raises(ValidationError) as exc:
        Course(**data)
    assert 'cannot exceed 10 hours' in str(exc.value.errors())
```

## Summary

| Pattern | Use Case | Key Feature |
|---------|----------|-------------|
| **Discriminated Unions** | Payment methods | Type-based polymorphism |
| **Recursive Validation** | Comment threads | Self-referencing structures |
| **Validation Context** | Conditional rules | Status-dependent validation |
| **Nested Lists** | Course curriculum | Multi-level hierarchies |

## Key Takeaways

1. **Discriminated Unions**: Use `discriminator='type'` for polymorphic data
2. **Forward References**: Use string quotes and `model_rebuild()` for recursion
3. **Validation Context**: Use `ValidationInfo` to access other field values
4. **List Constraints**: Use `min_length`, `max_length` for list validation
5. **Nested Properties**: Compute aggregates with @property decorators
6. **Cross-Field Validation**: Use `@field_validator` with `info.data`

---

**Previous**: [Order Validation Example](order-validation-example.md) | **Index**: [Examples Index](INDEX.md)

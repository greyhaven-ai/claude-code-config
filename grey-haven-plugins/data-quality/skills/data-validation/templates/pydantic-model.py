"""
Pydantic Model Template

Copy this template to create new Pydantic validation models.
Replace {ModelName}, {field_name}, and {FieldType} with your actual values.
"""

from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr, HttpUrl
from typing import Optional, List, Literal
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from enum import Enum


# Optional: Define enums for categorical fields
class {ModelName}Status(str, Enum):
    """Status enum for {ModelName}."""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class {ModelName}CreateSchema(BaseModel):
    """
    Schema for creating a {ModelName}.
    
    This schema defines the data contract for API requests.
    All validation rules are enforced here.
    """

    # Required string field with length constraints
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Display name",
        examples=["Example Name"]
    )

    # Email field with built-in validation
    email: EmailStr = Field(
        ...,
        description="Email address"
    )

    # Optional string field
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional description"
    )

    # Integer with range constraints
    quantity: int = Field(
        ...,
        ge=1,
        le=999,
        description="Quantity (1-999)"
    )

    # Decimal for currency (recommended over float)
    price: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Price in USD"
    )

    # Date field
    start_date: date = Field(
        ...,
        description="Start date"
    )

    # Enum field
    status: {ModelName}Status = Field(
        default={ModelName}Status.PENDING,
        description="Current status"
    )

    # List field with constraints
    tags: List[str] = Field(
        default_factory=list,
        max_length=10,
        description="Associated tags"
    )

    # Literal type (inline enum)
    priority: Literal['low', 'medium', 'high'] = Field(
        default='medium',
        description="Priority level"
    )


    # Field Validators
    # ---------------

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name format."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @field_validator('tags')
    @classmethod
    def validate_unique_tags(cls, v: List[str]) -> List[str]:
        """Ensure tags are unique."""
        if len(v) != len(set(v)):
            raise ValueError('Duplicate tags not allowed')
        return [tag.lower() for tag in v]


    # Model Validators (cross-field validation)
    # ----------------------------------------

    @model_validator(mode='after')
    def validate_business_rules(self):
        """Validate business rules across fields."""
        # Example: Ensure high-priority items have descriptions
        if self.priority == 'high' and not self.description:
            raise ValueError('High priority items must have description')
        
        return self


    # Configuration
    # ------------

    model_config = {
        # Strip whitespace from strings
        'str_strip_whitespace': True,
        
        # Validate on assignment
        'validate_assignment': True,
        
        # JSON schema examples
        'json_schema_extra': {
            'examples': [{
                'name': 'Example {ModelName}',
                'email': 'example@company.com',
                'description': 'An example description',
                'quantity': 5,
                'price': '99.99',
                'start_date': '2024-01-01',
                'status': 'active',
                'tags': ['tag1', 'tag2'],
                'priority': 'medium'
            }]
        }
    }


class {ModelName}UpdateSchema(BaseModel):
    """
    Schema for updating a {ModelName}.
    
    All fields are optional for partial updates.
    """
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    description: Optional[str] = Field(None, max_length=500)
    quantity: Optional[int] = Field(None, ge=1, le=999)
    price: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    status: Optional[{ModelName}Status] = None
    tags: Optional[List[str]] = Field(None, max_length=10)
    priority: Optional[Literal['low', 'medium', 'high']] = None

    model_config = {
        'str_strip_whitespace': True,
        'validate_assignment': True
    }


class {ModelName}ResponseSchema(BaseModel):
    """
    Schema for {ModelName} responses.
    
    Includes all fields plus auto-generated ones (id, timestamps).
    """
    
    id: UUID
    name: str
    email: str
    description: Optional[str]
    quantity: int
    price: Decimal
    start_date: date
    status: str
    tags: List[str]
    priority: str
    
    # Auto-generated fields
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        # Enable ORM mode for SQLModel compatibility
        'from_attributes': True
    }


# Usage Example
# -------------

if __name__ == '__main__':
    # Valid data
    data = {
        'name': 'Test Item',
        'email': 'test@example.com',
        'quantity': 10,
        'price': '49.99',
        'start_date': '2024-01-01',
        'status': 'active',
        'tags': ['electronics', 'featured']
    }
    
    # Create instance
    item = {ModelName}CreateSchema(**data)
    print(f"Created: {item.model_dump_json()}")
    
    # Validation will raise errors for invalid data
    try:
        invalid_data = {**data, 'quantity': 0}  # Invalid quantity
        {ModelName}CreateSchema(**invalid_data)
    except ValidationError as e:
        print(f"Validation error: {e.errors()}")

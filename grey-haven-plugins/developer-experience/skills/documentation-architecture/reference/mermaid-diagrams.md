# Mermaid Diagram Templates for Architecture Documentation

Comprehensive guide to Mermaid diagram types for visualizing system architecture, data flows, and interactions.

## Why Mermaid?

- **Version Controlled**: Diagrams in code, reviewable in PRs
- **Always Up-to-Date**: Easy to update alongside code changes
- **No Image Files**: Rendered dynamically in documentation
- **GitHub Native**: Renders in README.md and issues
- **Interactive**: Clickable links, zooming

## System Architecture Diagrams

### Basic Architecture

```mermaid
graph TB
    subgraph "Frontend"
        UI[React UI]
    end
    
    subgraph "Backend"
        API[FastAPI]
        DB[(PostgreSQL)]
    end
    
    UI --> API
    API --> DB
```

### Multi-Tier Architecture

```mermaid
graph TB
    subgraph "Client"
        Browser[Web Browser]
        Mobile[Mobile App]
    end
    
    subgraph "Edge (Cloudflare)"
        Gateway[API Gateway]
        Cache[KV Cache]
    end
    
    subgraph "Application"
        Frontend[TanStack Start]
        Backend[FastAPI]
    end
    
    subgraph "Data"
        DB[(PostgreSQL)]
        Redis[(Redis)]
        R2[(Object Storage)]
    end
    
    Browser --> Gateway
    Mobile --> Gateway
    Gateway --> Frontend
    Gateway --> Backend
    Gateway --> Cache
    Backend --> DB
    Backend --> Redis
    Backend --> R2
```

### Microservices Architecture

```mermaid
graph LR
    Gateway[API Gateway]
    
    subgraph "Services"
        Auth[Auth Service]
        Users[User Service]
        Orders[Order Service]
        Payments[Payment Service]
    end
    
    subgraph "Data"
        AuthDB[(Auth DB)]
        UserDB[(User DB)]
        OrderDB[(Order DB)]
    end
    
    Gateway --> Auth
    Gateway --> Users
    Gateway --> Orders
    Gateway --> Payments
    
    Auth --> AuthDB
    Users --> UserDB
    Orders --> OrderDB
    Payments -.Stripe.-> External[External API]
```

## Sequence Diagrams

### Authentication Flow

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Gateway
    participant Auth
    participant DB
    
    User->>Browser: Enter credentials
    Browser->>Gateway: POST /auth/login
    Gateway->>Auth: Validate credentials
    Auth->>DB: Query user
    DB-->>Auth: User record
    
    alt Valid
        Auth->>Auth: Generate JWT
        Auth-->>Gateway: {token, user}
        Gateway-->>Browser: 200 OK
        Browser-->>User: Redirect
    else Invalid
        Auth-->>Gateway: 401
        Gateway-->>Browser: Error
        Browser-->>User: Show error
    end
```

### API Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Backend
    participant DB
    participant Cache
    
    Client->>Gateway: GET /users/123
    Gateway->>Gateway: Validate JWT
    Gateway->>Cache: Check cache
    
    alt Cache Hit
        Cache-->>Gateway: User data
        Gateway-->>Client: 200 OK (cached)
    else Cache Miss
        Gateway->>Backend: Forward request
        Backend->>DB: Query user
        DB-->>Backend: User data
        Backend-->>Gateway: Response
        Gateway->>Cache: Store in cache
        Gateway-->>Client: 200 OK
    end
```

### Payment Processing

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant PaymentSvc
    participant Stripe
    participant DB
    
    Client->>API: POST /orders
    API->>PaymentSvc: Process payment
    PaymentSvc->>Stripe: Create payment intent
    Stripe-->>PaymentSvc: Payment intent
    PaymentSvc-->>API: Intent created
    API-->>Client: {client_secret}
    
    Client->>Stripe: Confirm payment
    Stripe->>PaymentSvc: Webhook: payment.succeeded
    PaymentSvc->>DB: Update order status
    PaymentSvc->>API: Notify completion
    API->>Client: Send confirmation email
```

## Data Flow Diagrams

### Order Processing Flow

```mermaid
flowchart LR
    Start[User Creates Order] --> Validate[Validate Data]
    Validate --> Stock{Check Stock}
    
    Stock -->|Insufficient| Error[Return Error]
    Stock -->|Available| Reserve[Reserve Items]
    
    Reserve --> Payment[Process Payment]
    Payment -->|Failed| Release[Release Items]
    Release --> Error
    
    Payment -->|Success| Create[Create Order]
    Create --> Queue[Queue Email]
    Queue --> Cache[Invalidate Cache]
    Cache --> Success[Return Order]
    
    Success --> Async[Async: Send Email]
```

### Data Transformation Pipeline

```mermaid
flowchart TD
    Raw[Raw Data] --> Extract[Extract]
    Extract --> Transform[Transform]
    Transform --> Validate{Validate}
    
    Validate -->|Invalid| Log[Log Error]
    Validate -->|Valid| Enrich[Enrich Data]
    
    Enrich --> Normalize[Normalize]
    Normalize --> Store[(Store in DB)]
    Store --> Index[Update Search Index]
    Index --> Cache[Update Cache]
```

## Entity Relationship Diagrams

### Multi-Tenant E-Commerce

```mermaid
erDiagram
    TENANT ||--o{ USER : has
    TENANT ||--o{ ORDER : has
    TENANT ||--o{ PRODUCT : has
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : included_in
    
    TENANT {
        uuid id PK
        string name
        string subdomain UK
        timestamp created_at
    }
    
    USER {
        uuid id PK
        uuid tenant_id FK
        string email UK
        string role
    }
    
    PRODUCT {
        uuid id PK
        uuid tenant_id FK
        string name
        decimal price
        int stock
    }
    
    ORDER {
        uuid id PK
        uuid tenant_id FK
        uuid user_id FK
        decimal total
        string status
    }
    
    ORDER_ITEM {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal unit_price
    }
```

### User Authentication Schema

```mermaid
erDiagram
    USER ||--o{ SESSION : has
    USER ||--o{ API_KEY : has
    USER ||--o{ OAUTH_TOKEN : has
    USER }|--|| USER_PROFILE : has
    
    USER {
        uuid id PK
        string email UK
        string hashed_password
        bool email_verified
    }
    
    SESSION {
        uuid id PK
        uuid user_id FK
        string token UK
        timestamp expires_at
    }
    
    API_KEY {
        uuid id PK
        uuid user_id FK
        string key_hash UK
        string name
        timestamp last_used
    }
```

## State Diagrams

### Order State Machine

```mermaid
stateDiagram-v2
    [*] --> Pending: Order Created
    Pending --> Processing: Payment Confirmed
    Pending --> Cancelled: Payment Failed
    
    Processing --> Shipped: Fulfillment Complete
    Processing --> Cancelled: Out of Stock
    
    Shipped --> Delivered: Tracking Confirmed
    Shipped --> Returned: Customer Return
    
    Delivered --> Returned: Return Requested
    Returned --> Refunded: Return Approved
    
    Cancelled --> [*]
    Delivered --> [*]
    Refunded --> [*]
```

### User Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Invited: User Invited
    Invited --> Active: Accept Invitation
    Invited --> Expired: 7 Days Passed
    
    Active --> Suspended: Policy Violation
    Active --> Inactive: 90 Days No Login
    
    Suspended --> Active: Appeal Approved
    Inactive --> Active: User Logs In
    
    Active --> Deleted: User Deletes Account
    Suspended --> Deleted: Admin Deletes
    
    Expired --> [*]
    Deleted --> [*]
```

## Deployment Diagrams

### CI/CD Pipeline

```mermaid
graph LR
    Dev[Feature Branch] -->|PR| CI[GitHub Actions]
    CI -->|Tests| Tests{Tests Pass?}
    
    Tests -->|No| Fail[❌ Fail]
    Tests -->|Yes| Build[Build]
    
    Build --> Stage[Deploy to Staging]
    Stage -->|Smoke Tests| SmokeTest{Pass?}
    
    SmokeTest -->|No| Fail
    SmokeTest -->|Yes| Approve{Manual Approve?}
    
    Approve -->|No| Wait[Wait]
    Approve -->|Yes| Canary[Canary Deploy 10%]
    
    Canary -->|Monitor| Monitor{Healthy?}
    Monitor -->|No| Rollback[Rollback]
    Monitor -->|Yes| Prod[Deploy 100%]
```

### Multi-Region Deployment

```mermaid
graph TB
    subgraph "Region: US-East"
        USWorker[Cloudflare Workers]
        USDB[(Primary DB)]
    end
    
    subgraph "Region: Europe"
        EUWorker[Cloudflare Workers]
        EUDB[(Read Replica)]
    end
    
    subgraph "Region: Asia"
        AsiaWorker[Cloudflare Workers]
        AsiaDB[(Read Replica)]
    end
    
    subgraph "Global"
        DNS[Global DNS]
        CDN[Cloudflare CDN]
    end
    
    DNS --> USWorker
    DNS --> EUWorker
    DNS --> AsiaWorker
    
    CDN --> USWorker
    CDN --> EUWorker
    CDN --> AsiaWorker
    
    USDB -.replication.-> EUDB
    USDB -.replication.-> AsiaDB
```

## Class Diagrams (TypeScript/Python)

### Service Architecture

```mermaid
classDiagram
    class OrderService {
        -repository: OrderRepository
        -payment: PaymentService
        +createOrder(data) Order
        +getOrder(id) Order
        +cancelOrder(id) void
    }
    
    class OrderRepository {
        -db: Database
        +save(order) Order
        +findById(id) Order
        +findByUser(userId) Order[]
    }
    
    class PaymentService {
        -stripe: StripeClient
        +processPayment(amount) PaymentResult
        +refund(paymentId) void
    }
    
    class Order {
        +id: string
        +userId: string
        +total: number
        +status: OrderStatus
    }
    
    OrderService --> OrderRepository
    OrderService --> PaymentService
    OrderRepository --> Order
```

## Best Practices

1. **Keep Diagrams Simple**: One concept per diagram
2. **Use Subgraphs**: Group related components
3. **Consistent Naming**: Use same names as code
4. **Color Coding**: Use colors sparingly for emphasis
5. **Labels**: Add descriptive labels to edges
6. **Legend**: Include legend for complex diagrams
7. **Direction**: LR (left-right) or TB (top-bottom) based on flow
8. **Update Regularly**: Keep in sync with code changes

## Rendering in Documentation

### GitHub Markdown

````markdown
```mermaid
graph TB
    A[Start] --> B[Process]
    B --> C[End]
```
````

### Docusaurus

Install plugin:
```bash
npm install @docusaurus/theme-mermaid
```

### MkDocs

Install plugin:
```bash
pip install mkdocs-mermaid2-plugin
```

## Common Patterns

### Request/Response Flow
Use sequence diagrams with alt/opt for error handling

### Data Relationships
Use ER diagrams with proper cardinality (||--o{)

### State Transitions
Use state diagrams for order status, user lifecycle

### System Overview
---

Related: [openapi-patterns.md](openapi-patterns.md) | [documentation-standards.md](documentation-standards.md) | [Return to INDEX](INDEX.md)

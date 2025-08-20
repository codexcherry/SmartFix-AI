# SmartFix-AI Detailed Architecture

## System Overview

SmartFix-AI is built as a microservices-based architecture with clear separation of concerns, enabling scalability, maintainability, and extensibility.

### High-Level Architecture

```mermaid
flowchart TD
    %% Client Layer
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile App] 
        C[API Clients]
    end
    
    %% Presentation Layer
    subgraph "Presentation Layer"
        D[React Frontend]
        E[API Gateway]
    end
    
    %% Input Processing
    subgraph "Input Layer"
        A1["Text Query"] 
        A2["Voice Input"] 
        A3["Image Upload"] 
        A4["Log Files"]
        B1["Input Preprocessing"]
    end
    
    %% Application Layer
    subgraph "Application Layer"
        F[FastAPI Backend]
        G[Brain Core System]
        H[Virtual Assistant]
    end
    
    %% Processing Components
    subgraph "Processing Layer"
        C1["Speech-to-Text<br/>(Hugging Face)"]
        C2["Image Analysis<br/>(Gemini Vision)"]
        C3["Log Parsing<br/>(Gemini API)"]
        C4["Web Search<br/>(SerpAPI)"]
    end
    
    %% AI Reasoning Engine
    subgraph "AI Reasoning Engine"
        D1["Fusion Layer"]
        E1["Root Cause Analysis<br/>(Gemini API)"]
        F1["Solution Ranking<br/>(Hugging Face)"]
    end
    
    %% Service Layer
    subgraph "Service Layer"
        I[AI Services]
        J[External APIs]
        K[Device Analytics]
    end
    
    %% Output Components
    subgraph "Output Layer"
        G1["UI Display"]
        G2["SMS/WhatsApp<br/>(Twilio)"]
        G3["Voice Response"]
    end
    
    %% Data Layer
    subgraph "Data Layer"
        L[Primary Database]
        M[Brain Memory DB]
        N[File Storage]
        H1["JSON Database"]
    end
    
    %% Client to Presentation connections
    A --> D
    B --> E
    C --> E
    
    %% Presentation to Application connections
    D --> F
    E --> F
    
    %% Input flow
    A --> A1
    B --> A2
    C --> A3
    D --> A4
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    %% Application layer connections
    F --> G
    F --> H
    B1 --> F
    
    %% Processing flow
    B1 --> C1
    B1 --> C2
    B1 --> C3
    B1 --> C4
    
    %% AI Reasoning flow
    C1 --> D1
    C2 --> D1
    C3 --> D1
    C4 --> D1
    D1 --> E1
    E1 --> F1
    
    %% Service layer connections
    G --> I
    G --> J
    H --> I
    K --> J
    F1 --> I
    I --> C1
    I --> C2
    I --> C3
    J --> C4
    
    %% Output connections
    F1 --> G1
    F1 --> G2
    F1 --> G3
    G1 --> D
    G2 --> J
    G3 --> D
    
    %% Data layer connections
    F --> L
    G --> M
    I --> N
    F1 --> H1
    H1 --> D1
    M --> G
    L --> F
    N --> I
    
    %% Brain Core integration
    G --> E1
    G --> D1
    H --> F1
    
    %% Cross-layer data flow
    K --> M
    H1 --> M
    
    %% Styling with grey tones and black background
    classDef clientLayer fill:#4a4a4a,stroke:#666,stroke-width:2px,color:#fff
    classDef presentationLayer fill:#5a5a5a,stroke:#777,stroke-width:2px,color:#fff
    classDef inputLayer fill:#3a3a3a,stroke:#555,stroke-width:2px,color:#fff
    classDef applicationLayer fill:#6a6a6a,stroke:#888,stroke-width:2px,color:#fff
    classDef processingLayer fill:#454545,stroke:#666,stroke-width:2px,color:#fff
    classDef reasoningLayer fill:#555555,stroke:#777,stroke-width:2px,color:#fff
    classDef serviceLayer fill:#404040,stroke:#666,stroke-width:2px,color:#fff
    classDef outputLayer fill:#505050,stroke:#777,stroke-width:2px,color:#fff
    classDef dataLayer fill:#353535,stroke:#555,stroke-width:2px,color:#fff
    
    %% Set black background for the entire diagram
    %%{init: {'theme':'base', 'themeVariables': {'primaryColor': '#333', 'primaryTextColor': '#fff', 'primaryBorderColor': '#666', 'lineColor': '#777', 'background': '#000000'}}}%%
    
    class A,B,C clientLayer
    class D,E presentationLayer
    class A1,A2,A3,A4,B1 inputLayer
    class F,G,H applicationLayer
    class C1,C2,C3,C4 processingLayer
    class D1,E1,F1 reasoningLayer
    class I,J,K serviceLayer
    class G1,G2,G3 outputLayer
    class L,M,N,H1 dataLayer
```

## Core Components

### Brain Core System

The intelligent orchestrator that coordinates all AI processing:

```python
class BrainCore:
    def __init__(self):
        self.brain_memory = BrainMemory()
        self.hf_service = HuggingFaceService()
        self.gemini_service = GeminiService()
        self.serp_service = SerpAPIService()
        self.ocr_service = OCRService()
```

**Key Responsibilities:**
- Input Processing: Converts all input types to text
- Memory Management: Stores and retrieves solutions
- AI Coordination: Manages multiple AI models
- Learning Engine: Improves from user feedback
- Solution Ranking: Prioritizes solutions by confidence

### AI Services Layer

#### HuggingFace Service
- Speech-to-text conversion
- Text analysis and intent classification
- Entity extraction

#### Gemini Service
- Advanced problem analysis
- Solution generation
- Contextual understanding

#### OCR Service
- Image text extraction
- Error code detection
- Pattern recognition

#### SerpAPI Service
- Web search for solutions
- Real-time information retrieval
- External resource integration

### Virtual Assistant

Interactive chat-based troubleshooting system with:
- Natural language conversation
- Session management
- Quick actions
- Voice integration

### Device Analytics

Comprehensive system monitoring:
- Health monitoring
- Performance metrics
- Security analysis
- Hardware diagnostics

## Data Flow

### Request Processing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant BC as Brain Core
    participant AI as AI Services
    participant DB as Database

    U->>F: Submit Query
    F->>B: API Request
    B->>BC: Process Input
    BC->>AI: Analyze with AI
    AI->>BC: AI Results
    BC->>DB: Store Query
    BC->>B: Formatted Response
    B->>F: API Response
    F->>U: Display Solution
```

### AI Processing Pipeline

```mermaid
flowchart TD
    A[Input] --> B[Preprocessing]
    B --> C[Text Conversion]
    C --> D[Brain Memory Check]
    D --> E{Match Found?}
    E -->|Yes| F[Return Solution]
    E -->|No| G[AI Analysis]
    G --> H[Gemini Analysis]
    G --> I[Web Search]
    G --> J[OCR Processing]
    H --> K[Combine Results]
    I --> K
    J --> K
    K --> L[Rank Solutions]
    L --> M[Store in Memory]
    M --> N[Return Best Solution]
```

## Database Design

### Primary Database Schema

```json
{
  "queries": {
    "id": "string",
    "user_id": "string",
    "input_type": "string",
    "query_content": "object",
    "timestamp": "datetime",
    "status": "string",
    "solution": "object",
    "brain_analysis": "object"
  },
  "notifications": {
    "id": "string",
    "user_id": "string",
    "notification_type": "string",
    "message": "string",
    "to_contact": "string",
    "timestamp": "datetime",
    "status": "string"
  },
  "sessions": {
    "id": "string",
    "user_id": "string",
    "start_time": "datetime",
    "end_time": "datetime",
    "messages": "array"
  },
  "feedback": {
    "id": "string",
    "query_id": "string",
    "user_id": "string",
    "success": "boolean",
    "feedback_score": "integer",
    "timestamp": "datetime"
  }
}
```

### Brain Memory Database

```json
{
  "problems": {
    "id": "string",
    "problem_text": "string",
    "problem_type": "string",
    "device_category": "string",
    "error_codes": "array",
    "symptoms": "string",
    "solution_steps": "array",
    "confidence_score": "float",
    "success_rate": "float",
    "usage_count": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
  },
  "embeddings": {
    "id": "string",
    "problem_id": "string",
    "embedding_vector": "array",
    "created_at": "datetime"
  },
  "learning_data": {
    "id": "string",
    "query_text": "string",
    "solution_used": "string",
    "success": "boolean",
    "user_feedback": "object",
    "timestamp": "datetime"
  }
}
```

## API Design

### RESTful API Structure

```
/api/v1/
├── query/
│   ├── text          # Text-based queries
│   ├── image         # Image-based queries
│   ├── voice         # Voice-based queries
│   ├── logs          # Log file analysis
│   └── notify        # Send notifications
├── brain/
│   ├── stats         # Brain system statistics
│   ├── search        # Search brain memory
│   ├── feedback      # Submit feedback
│   └── add-solution  # Add custom solutions
├── assistant/
│   ├── chat          # Virtual assistant chat
│   ├── voice         # Voice interaction
│   ├── quick-actions # Get quick actions
│   └── sessions      # Session management
└── device/
    ├── analyze       # Device analysis
    ├── health        # Health check
    ├── performance   # Performance metrics
    └── security      # Security analysis
```

### API Response Format

```json
{
  "success": true,
  "data": {
    "query_id": "uuid",
    "solution": {
      "issue": "string",
      "possible_causes": ["array"],
      "confidence_score": 0.85,
      "recommended_steps": [
        {
          "step_number": 1,
          "description": "string"
        }
      ],
      "external_sources": [
        {
          "title": "string",
          "snippet": "string",
          "url": "string"
        }
      ]
    },
    "source": "brain_memory|ai_analysis|error",
    "query_text": "string"
  },
  "metadata": {
    "processing_time": 1.23,
    "models_used": ["gemini", "huggingface"],
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

## Security Architecture

### Authentication & Authorization

- JWT-based authentication
- Role-based access control
- API key management for external services
- Session management

### Data Protection

- Input validation using Pydantic schemas
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting

## Performance Considerations

### Caching Strategy

- Redis-based caching for frequently accessed data
- AI model result caching
- Database query result caching
- Static asset caching

### Database Optimization

- Strategic indexing on frequently queried fields
- Connection pooling
- Query optimization
- Data archiving for old records

### AI Model Optimization

- Model caching and preloading
- Batch processing for multiple inputs
- Asynchronous processing
- Resource pooling

## Scalability

### Horizontal Scaling

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX Load Balancer]
    end
    
    subgraph "Application Servers"
        A1[FastAPI Instance 1]
        A2[FastAPI Instance 2]
        A3[FastAPI Instance 3]
    end
    
    subgraph "Database Cluster"
        DB1[Primary DB]
        DB2[Replica DB 1]
        DB3[Replica DB 2]
    end
    
    subgraph "AI Services"
        AI1[AI Service 1]
        AI2[AI Service 2]
    end
    
    LB --> A1
    LB --> A2
    LB --> A3
    A1 --> DB1
    A2 --> DB1
    A3 --> DB1
    A1 --> AI1
    A2 --> AI2
    A3 --> AI1
```

### Microservices Architecture

- Service discovery and registration
- Inter-service communication
- Message queue integration
- Independent scaling of services

## Monitoring & Observability

### Logging Strategy

- Structured logging with correlation IDs
- Request/response logging
- Error tracking and alerting
- Performance metrics collection

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": await check_database_health(),
            "ai_services": await check_ai_services_health(),
            "external_apis": await check_external_apis_health()
        },
        "metrics": {
            "memory_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(),
            "disk_usage": psutil.disk_usage('/').percent
        }
    }
```

### Metrics Collection

- API response times
- AI model usage and performance
- Error rates and types
- User interaction analytics
- System resource utilization

### Alerting System

- Real-time alerting for system issues
- Performance degradation alerts
- Error rate thresholds
- Resource usage alerts

## Deployment Architecture

### Container Orchestration

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SERPAPI_KEY=${SERPAPI_KEY}
    volumes:
      - ./database:/app/database
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api/v1
    depends_on:
      - backend
    restart: unless-stopped
```

### Environment Configuration

- Development environment
- Staging environment
- Production environment
- Environment-specific configurations
- Secret management

## Future Enhancements

### Planned Features

1. **Multi-language Support**
   - Internationalization (i18n)
   - Language detection
   - Localized responses

2. **Advanced Device Integration**
   - IoT device support
   - Real-time device monitoring
   - Predictive maintenance

3. **Enhanced AI Models**
   - Custom model training
   - Model versioning
   - A/B testing for models

4. **Real-time Collaboration**
   - Multi-user sessions
   - Collaborative troubleshooting
   - Expert assistance integration

5. **Mobile Application**
   - React Native app
   - Offline capabilities
   - Push notifications

### Technical Improvements

1. **Performance Optimization**
   - GraphQL implementation
   - WebSocket for real-time updates
   - CDN integration

2. **Security Enhancements**
   - OAuth 2.0 integration
   - Two-factor authentication
   - Advanced encryption

3. **Scalability Improvements**
   - Kubernetes deployment
   - Auto-scaling
   - Global distribution

This detailed architecture provides a comprehensive technical foundation for the SmartFix-AI system, ensuring scalability, maintainability, and extensibility for future growth and enhancements.


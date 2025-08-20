# SmartFix-AI 🤖

**An Intelligent Multimodal Troubleshooting Assistant Powered by AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

SmartFix-AI is a cutting-edge intelligent troubleshooting system that combines multiple AI models to provide comprehensive device diagnostics and repair solutions. The system processes text, voice, images, and log files to deliver accurate troubleshooting guidance through an intuitive web interface.

### ✨ Key Features

- **🔍 Multimodal Input Processing**: Text, voice, images, and log files
- **🧠 Intelligent Brain Core**: AI-powered problem analysis and solution generation
- **📱 Virtual Assistant**: Interactive chat-based troubleshooting
- **📊 Device Analytics**: Comprehensive system health monitoring
- **🔔 Smart Notifications**: SMS/WhatsApp integration via Twilio
- **📈 Learning System**: Continuously improves from user feedback
- **🌐 Web Search Integration**: Real-time solution lookup
- **🎨 Modern UI**: Premium dark theme with responsive design

## 🏗️ Architecture

### System Overview

```mermaid
flowchart TD
    subgraph "Input Layer"
        A1["Text Query"] --> B
        A2["Voice Input"] --> B
        A3["Image Upload"] --> B
        A4["Log Files"] --> B
        B["Input Preprocessing"]
    end
    
    subgraph "Processing Layer"
        C1["Speech-to-Text<br/>(Hugging Face)"]
        C2["Image Analysis<br/>(Gemini Vision)"]
        C3["Log Parsing<br/>(Gemini API)"]
        C4["Web Search<br/>(SerpAPI)"]
        B --> C1
        B --> C2
        B --> C3
        B --> C4
    end
    
    subgraph "AI Reasoning Engine"
        D["Fusion Layer"]
        E["Root Cause Analysis<br/>(Gemini API)"]
        F["Solution Ranking<br/>(Hugging Face)"]
        C1 --> D
        C2 --> D
        C3 --> D
        C4 --> D
        D --> E
        E --> F
    end
    
    subgraph "Output Layer"
        G1["UI Display"]
        G2["SMS/WhatsApp<br/>(Twilio)"]
        G3["Voice Response"]
        F --> G1
        F --> G2
        F --> G3
    end
    
    subgraph "Storage"
        H["JSON Database"]
        F --> H
        H --> D
    end
```
### Core Components

#### 1. **Brain Core System** 🧠
The intelligent heart of SmartFix-AI that orchestrates all processing:

- **Input Processing**: Converts all input types to text for analysis
- **Memory Management**: Stores and retrieves solutions from brain memory
- **AI Integration**: Coordinates multiple AI models for comprehensive analysis
- **Learning Engine**: Continuously improves from user interactions
- **Solution Ranking**: Prioritizes solutions based on confidence and relevance

#### 2. **AI Services Layer** 🤖
Multiple specialized AI services working in harmony:

- **HuggingFace Service**: Speech-to-text conversion and text analysis
- **Gemini Service**: Advanced problem analysis and solution generation
- **OCR Service**: Image text extraction and error code detection
- **SerpAPI Service**: Web search for real-time solutions

#### 3. **Virtual Assistant** 💬
Interactive troubleshooting companion:

- **Chat Interface**: Natural language conversation
- **Session Management**: Maintains context across interactions
- **Quick Actions**: Predefined troubleshooting workflows
- **Voice Integration**: Speech-based interaction

#### 4. **Device Analytics** 📊
Comprehensive system monitoring:

- **Health Monitoring**: Real-time system status
- **Performance Metrics**: CPU, memory, storage analysis
- **Security Analysis**: Vulnerability assessment
- **Hardware Diagnostics**: Component health evaluation

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Docker & Docker Compose**
- **API Keys** (see Configuration section)

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/SmartFix-AI.git
cd SmartFix-AI

# Copy environment template
cp env.example .env

# Edit environment variables
nano .env

# Start the application
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HUGGINGFACE_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
export SERPAPI_KEY="your_key_here"
export TWILIO_SID="your_sid_here"
export TWILIO_AUTH_TOKEN="your_token_here"
export TWILIO_FROM_PHONE="your_phone_here"

# Run the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Access at http://localhost:3000
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AI Service API Keys
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
SERPAPI_KEY=your_serpapi_key_here

# Twilio Configuration
TWILIO_SID=your_twilio_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_FROM_PHONE=your_twilio_phone_number_here
TWILIO_TO_PHONE=your_phone_number_here

# Security
SECRET_KEY=your_secret_key_here

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### API Keys Setup

1. **HuggingFace**: Get your API key from [HuggingFace](https://huggingface.co/settings/tokens)
2. **Gemini**: Obtain API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **SerpAPI**: Sign up at [SerpAPI](https://serpapi.com/) for web search capabilities
4. **Twilio**: Create account at [Twilio](https://www.twilio.com/) for SMS/WhatsApp

## 📚 API Documentation

### Core Endpoints

#### Text Query Processing
```http
POST /api/v1/query/text
Content-Type: application/json

{
  "user_id": "user123",
  "input_type": "text",
  "text_query": "My laptop won't turn on"
}
```

#### Image Analysis
```http
POST /api/v1/query/image
Content-Type: multipart/form-data

Form Data:
- image: [file]
- text_query: "Error message shown"
- user_id: "user123"
```

#### Voice Processing
```http
POST /api/v1/query/voice
Content-Type: multipart/form-data

Form Data:
- audio: [file]
- user_id: "user123"
```

#### Log File Analysis
```http
POST /api/v1/query/logs
Content-Type: multipart/form-data

Form Data:
- log_file: [file]
- user_id: "user123"
```

### Brain System Endpoints

#### Get Brain Statistics
```http
GET /api/v1/brain/stats
```

#### Search Brain Memory
```http
POST /api/v1/brain/search
Content-Type: application/json

{
  "query": "laptop won't start",
  "device_category": "laptop"
}
```

#### Submit Feedback
```http
POST /api/v1/brain/feedback
Content-Type: application/json

{
  "query_id": "query_123",
  "success": true,
  "feedback_score": 5
}
```

### Virtual Assistant Endpoints

#### Chat Interface
```http
POST /api/v1/assistant/chat
Content-Type: application/json

{
  "query": "Help me fix my printer",
  "user_id": "user123",
  "session_id": "session_456"
}
```

#### Quick Actions
```http
GET /api/v1/assistant/quick-actions
```

### Device Analytics Endpoints

#### Full System Analysis
```http
POST /api/v1/device/analyze
```

#### Health Check
```http
GET /api/v1/device/health
```

#### Performance Metrics
```http
GET /api/v1/device/analyze/performance
```

## 🏛️ Detailed Architecture

### Backend Architecture

```
backend/
├── app/
│   ├── api/                    # API layer
│   │   ├── endpoints/          # Route handlers
│   │   └── api.py             # Router configuration
│   ├── core/                   # Core configuration
│   │   └── config.py          # Settings management
│   ├── models/                 # Data models
│   │   └── schemas.py         # Pydantic schemas
│   ├── nlp/                    # NLP processing
│   │   ├── embedding/          # Text embedding
│   │   ├── entity/            # Entity extraction
│   │   ├── generation/        # Text generation
│   │   ├── intent/            # Intent classification
│   │   ├── preprocessing/     # Text preprocessing
│   │   ├── reasoning/         # Logical reasoning
│   │   └── pipeline.py        # NLP pipeline
│   ├── services/               # Business logic
│   │   ├── brain_core.py      # Main AI orchestrator
│   │   ├── brain_memory.py    # Memory management
│   │   ├── database.py        # Data persistence
│   │   ├── device_detector.py # System analysis
│   │   ├── gemini_service.py  # Gemini AI integration
│   │   ├── huggingface_service.py # HuggingFace integration
│   │   ├── ocr_service.py     # Image processing
│   │   ├── serpapi_service.py # Web search
│   │   ├── twilio_service.py  # Notifications
│   │   └── virtual_assistant.py # Chat interface
│   ├── utils/                  # Utility functions
│   └── main.py                # Application entry point
├── database/                   # Data storage
├── requirements.txt           # Python dependencies
└── Dockerfile                # Container configuration
```

### Frontend Architecture

```
frontend/
├── public/                    # Static assets
├── src/
│   ├── components/            # React components
│   │   ├── DeviceAnalyzer.js  # System analysis UI
│   │   ├── ImageQueryForm.js  # Image upload interface
│   │   ├── LogFileForm.js     # Log file upload
│   │   ├── SolutionDisplay.js # Results display
│   │   ├── TextQueryForm.js   # Text input interface
│   │   ├── VirtualAssistant.js # Chat interface
│   │   └── VoiceQueryForm.js  # Voice input interface
│   ├── pages/                 # Page components
│   │   └── Dashboard.js       # Main dashboard
│   ├── services/              # API integration
│   │   └── api.js            # HTTP client
│   ├── App.js                # Main application
│   └── index.js              # Entry point
├── package.json              # Node.js dependencies
└── Dockerfile               # Container configuration
```

### Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant BC as Brain Core
    participant AI as AI Services
    participant DB as Database

    U->>F: Submit Query (Text/Voice/Image/Log)
    F->>B: API Request
    B->>BC: Process Input
    BC->>AI: Analyze with AI Models
    AI->>BC: AI Analysis Results
    BC->>DB: Store Query & Solution
    BC->>B: Formatted Response
    B->>F: API Response
    F->>U: Display Solution
    U->>F: Provide Feedback
    F->>B: Feedback API
    B->>BC: Learn from Feedback
    BC->>DB: Update Brain Memory
```

## 🔧 Development

### Project Structure

```
SmartFix-AI/
├── backend/                   # FastAPI backend
├── frontend/                  # React frontend
├── database/                  # Data storage
├── docs/                      # Documentation
├── docker-compose.yml         # Container orchestration
├── env.example               # Environment template
├── requirements.txt          # Python dependencies
└── setup_env.py             # Environment setup
```

### Development Workflow

1. **Feature Development**:
   ```bash
   # Create feature branch
   git checkout -b feature/new-feature
   
   # Make changes
   # Test locally
   # Commit changes
   git commit -m "Add new feature"
   
   # Push and create PR
   git push origin feature/new-feature
   ```

2. **Testing**:
   ```bash
   # Backend tests
   cd backend
   python -m pytest test_*.py
   
   # Frontend tests
   cd frontend
   npm test
   ```

3. **Code Quality**:
   ```bash
   # Python linting
   flake8 backend/
   black backend/
   
   # JavaScript linting
   cd frontend
   npm run lint
   ```

### Adding New Features

#### Backend Services
1. Create service in `backend/app/services/`
2. Add API endpoints in `backend/app/api/endpoints/`
3. Update schemas in `backend/app/models/schemas.py`
4. Add tests in `backend/test_*.py`

#### Frontend Components
1. Create component in `frontend/src/components/`
2. Add to pages in `frontend/src/pages/`
3. Update API client in `frontend/src/services/api.js`
4. Add styling and interactions

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_api_endpoints.py

# Run with coverage
python -m pytest --cov=app
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- --testNamePattern="ComponentName"
```

### API Testing

```bash
# Test API endpoints
curl -X POST http://localhost:8000/api/v1/query/text \
  -H "Content-Type: application/json" \
  -d '{"text_query": "test query", "user_id": "test"}'
```

## 🚀 Deployment

### Production Deployment

#### Using Docker Compose

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Manual Deployment

1. **Backend Deployment**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Set production environment
   export ENVIRONMENT=production
   
   # Run with Gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Frontend Deployment**:
   ```bash
   # Build production bundle
   npm run build
   
   # Serve with nginx
   nginx -s reload
   ```

### Environment Configuration

#### Production Environment Variables

```env
# Production settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Security
SECRET_KEY=your_secure_secret_key
CORS_ORIGINS=https://yourdomain.com

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

## 📊 Monitoring & Analytics

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Brain system stats
curl http://localhost:8000/api/v1/brain/stats

# Device health
curl http://localhost:8000/api/v1/device/health
```

### Logging

The application uses structured logging with different levels:

- **DEBUG**: Detailed debugging information
- **INFO**: General application flow
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **CRITICAL**: Critical system failures

### Performance Monitoring

- **Response Times**: API endpoint performance
- **Memory Usage**: System resource utilization
- **Error Rates**: Application error tracking
- **User Interactions**: Feature usage analytics

## 🙏 Acknowledgments

- **Google Gemini**: Advanced AI analysis capabilities
- **HuggingFace**: NLP and speech processing
- **Twilio**: Communication services
- **FastAPI**: High-performance web framework
- **React**: Frontend framework
- **Material-UI**: UI component library

**Made with ❤️ by the SmartFix-AI Team**

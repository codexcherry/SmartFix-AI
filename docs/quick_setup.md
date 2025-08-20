# SmartFix-AI Quick Setup Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get SmartFix-AI running on your local machine quickly.

## Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.8+** and **Node.js 16+** (for local development)
- **API Keys** (see configuration section)

## Option 1: Docker Setup (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/SmartFix-AI.git
cd SmartFix-AI
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit environment variables (at minimum, add your API keys)
nano .env
```

**Minimum required environment variables:**
```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

### 3. Start the Application

```bash
# Start all services
docker-compose up -d

# Check if services are running
docker-compose ps
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Option 2: Local Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HUGGINGFACE_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
export SERPAPI_KEY="your_key_here"

# Run the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 🔑 Getting API Keys

### 1. HuggingFace API Key
1. Go to [HuggingFace](https://huggingface.co/settings/tokens)
2. Create a new token
3. Copy the token to your `.env` file

### 2. Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### 3. SerpAPI Key
1. Sign up at [SerpAPI](https://serpapi.com/)
2. Get your API key from the dashboard
3. Add it to your `.env` file

### 4. Twilio (Optional)
1. Create account at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Add to your `.env` file for SMS/WhatsApp features

## 🧪 Testing the Setup

### 1. Test Backend API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test text query endpoint
curl -X POST http://localhost:8000/api/v1/query/text \
  -H "Content-Type: application/json" \
  -d '{"text_query": "My laptop won't turn on", "user_id": "test"}'
```

### 2. Test Frontend

1. Open http://localhost:3000 in your browser
2. Try submitting a text query
3. Check if the solution is displayed correctly

### 3. Test API Documentation

1. Visit http://localhost:8000/docs
2. Try the interactive API documentation
3. Test endpoints directly from the browser

## 🔧 Common Issues & Solutions

### Issue: Docker containers not starting

**Solution:**
```bash
# Check Docker logs
docker-compose logs

# Restart containers
docker-compose down
docker-compose up -d
```

### Issue: API keys not working

**Solution:**
1. Verify API keys are correctly set in `.env`
2. Check if services are accessible:
   ```bash
   curl -H "Authorization: Bearer YOUR_HUGGINGFACE_KEY" \
        https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h
   ```

### Issue: Frontend can't connect to backend

**Solution:**
1. Ensure backend is running on port 8000
2. Check CORS settings in backend
3. Verify `REACT_APP_API_URL` in frontend environment

### Issue: Database errors

**Solution:**
```bash
# Create database directory
mkdir -p database

# Check database permissions
ls -la database/
```

## 📊 Monitoring Your Setup

### Check Service Status

```bash
# Docker services
docker-compose ps

# Backend health
curl http://localhost:8000/health

# Brain system stats
curl http://localhost:8000/api/v1/brain/stats
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🚀 Next Steps

### 1. Explore Features

- Try different input types (text, voice, image, logs)
- Test the virtual assistant
- Use device analytics
- Send notifications

### 2. Customize Configuration

- Modify AI model settings
- Adjust confidence thresholds
- Configure notification preferences
- Customize UI theme

### 3. Development

- Check out the [Development Guide](../README.md#development)
- Review the [API Documentation](api_reference.md)
- Explore the [Architecture](detailed_architecture.md)

### 4. Production Deployment

- Review [Deployment Section](../README.md#deployment)
- Set up monitoring and logging
- Configure security settings
- Set up CI/CD pipeline

## 📞 Getting Help

- **Documentation**: Check the [docs/](docs/) folder
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: support@smartfix-ai.com

## 🎉 Congratulations!

You've successfully set up SmartFix-AI! The system is now ready to help with troubleshooting and device diagnostics.

---

**Need more help?** Check out the [full README](../README.md) for comprehensive documentation.

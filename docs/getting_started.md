# Getting Started with SmartFix-AI

This guide will help you set up and run the SmartFix-AI multimodal troubleshooting assistant on your local machine.

## Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- API keys for the following services:
  - [Hugging Face](https://huggingface.co/settings/tokens)
  - [Google Gemini](https://ai.google.dev/)
  - [SerpAPI](https://serpapi.com/)
  - [Twilio](https://www.twilio.com/) (optional, for notifications)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartFix-AI.git
   cd SmartFix-AI
   ```

2. Create a `.env` file by copying the example:
   ```bash
   cp env.example .env
   ```

3. **Configure API Keys**: Edit the `.env` file with your actual API keys and settings. Replace the placeholder values with your real API keys:

   ```bash
   # API Keys - Replace with your actual keys
   HUGGINGFACE_API_KEY=your_actual_huggingface_api_key
   GEMINI_API_KEY=your_actual_gemini_api_key
   SERPAPI_KEY=your_actual_serpapi_key
   TWILIO_SID=your_actual_twilio_sid
   TWILIO_AUTH_TOKEN=your_actual_twilio_auth_token
   TWILIO_FROM_PHONE=your_actual_twilio_phone_number
   TWILIO_TO_PHONE=your_actual_phone_number
   
   # App Settings
   SECRET_KEY=your_actual_secret_key
   
   # Frontend Settings
   REACT_APP_API_URL=http://localhost:8000/api/v1
   ```

### API Key Setup Instructions

#### 1. Hugging Face API Key
- Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
- Click "New token"
- Give it a name (e.g., "SmartFix-AI")
- Select "Read" role
- Copy the generated token and paste it in your `.env` file

#### 2. Google Gemini API Key
- Visit [Google AI Studio](https://ai.google.dev/)
- Sign in with your Google account
- Go to "Get API key"
- Create a new API key
- Copy the key and paste it in your `.env` file

#### 3. SerpAPI Key
- Go to [SerpAPI](https://serpapi.com/)
- Sign up for an account
- Navigate to your dashboard
- Copy your API key and paste it in your `.env` file

#### 4. Twilio (Optional - for SMS notifications)
- Sign up at [Twilio](https://www.twilio.com/)
- Get your Account SID and Auth Token from the dashboard
- Get a Twilio phone number
- Add these to your `.env` file

### Security Best Practices

⚠️ **Important Security Notes:**
- **Never commit your `.env` file to version control**
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Use strong, unique API keys for each service
- Regularly rotate your API keys
- Keep your API keys secure and don't share them publicly

## Running the Application

### Using Docker Compose (Recommended)

1. Start the application:
   ```bash
   docker-compose up
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the frontend development server:
   ```bash
   npm start
   ```

## Usage

1. Open your browser and go to http://localhost:3000
2. Use one of the input methods to submit a troubleshooting query:
   - Text: Type your issue description
   - Image: Upload a screenshot or photo of the problem
   - Voice: Record a voice description of the issue
   - Log File: Upload system or application logs

3. The AI will process your query and provide:
   - Issue identification
   - Possible causes
   - Step-by-step troubleshooting instructions
   - External resources for further help

4. You can send the solution to your phone via SMS or WhatsApp (if configured)

# SmartFix-AI Architecture

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

## Component Details

### Input Layer
- **Text Query**: Direct text input from the user interface
- **Voice Input**: Audio recordings converted to text
- **Image Upload**: Screenshots of errors or device issues
- **Log Files**: System or application logs for analysis

### Processing Layer
- **Speech-to-Text**: Converts voice inputs to text using Hugging Face models
- **Image Analysis**: Extracts information from images using Gemini Vision
- **Log Parsing**: Analyzes log files to identify errors and patterns
- **Web Search**: Retrieves relevant solutions from the internet using SerpAPI

### AI Reasoning Engine
- **Fusion Layer**: Combines all inputs into a unified representation
- **Root Cause Analysis**: Identifies the likely cause of the issue using Gemini API
- **Solution Ranking**: Ranks possible solutions based on relevance and effectiveness

### Output Layer
- **UI Display**: Presents solutions through an interactive user interface
- **SMS/WhatsApp**: Sends notifications and updates via Twilio
- **Voice Response**: Provides audio feedback for hands-free operation

### Storage
- **JSON Database**: Stores user queries, solutions, and feedback for future reference

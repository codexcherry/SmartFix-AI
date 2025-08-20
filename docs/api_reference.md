# SmartFix-AI API Reference

This document provides details on the available API endpoints for the SmartFix-AI backend.

## Base URL

All API endpoints are prefixed with: `/api/v1`

## Authentication

Currently, the API does not require authentication. This will be implemented in future versions.

## Endpoints

### Text Query

Process a text-based troubleshooting query.

- **URL**: `/query/text`
- **Method**: `POST`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
  "user_id": "user123",
  "input_type": "text",
  "text_query": "My TV screen is flickering"
}
```

**Response**:
```json
{
  "query_id": "550e8400-e29b-41d4-a716-446655440000",
  "solution": {
    "issue": "TV screen flickering",
    "possible_causes": [
      "Loose HDMI connection",
      "Outdated firmware"
    ],
    "confidence_score": 0.85,
    "recommended_steps": [
      {
        "step_number": 1,
        "description": "Check HDMI cable connections"
      },
      {
        "step_number": 2,
        "description": "Update TV firmware"
      }
    ],
    "external_sources": [
      {
        "title": "Fix TV flickering issues",
        "snippet": "Common solutions for TV screen flickering problems...",
        "url": "https://example.com/fix"
      }
    ]
  }
}
```

### Image Query

Process an image-based troubleshooting query.

- **URL**: `/query/image`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

**Form Fields**:
- `image`: The image file (required)
- `text_query`: Additional text description (optional)
- `user_id`: User identifier (optional, defaults to "anonymous")

**Response**: Same format as Text Query

### Voice Query

Process a voice-based troubleshooting query.

- **URL**: `/query/voice`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

**Form Fields**:
- `audio`: The audio file (required)
- `user_id`: User identifier (optional, defaults to "anonymous")

**Response**:
```json
{
  "query_id": "550e8400-e29b-41d4-a716-446655440000",
  "solution": {
    "transcribed_text": "My TV screen is flickering",
    "issue": "TV screen flickering",
    "possible_causes": [
      "Loose HDMI connection",
      "Outdated firmware"
    ],
    "confidence_score": 0.85,
    "recommended_steps": [
      {
        "step_number": 1,
        "description": "Check HDMI cable connections"
      },
      {
        "step_number": 2,
        "description": "Update TV firmware"
      }
    ],
    "external_sources": [
      {
        "title": "Fix TV flickering issues",
        "snippet": "Common solutions for TV screen flickering problems...",
        "url": "https://example.com/fix"
      }
    ]
  }
}
```

### Log File Query

Process a log file for troubleshooting.

- **URL**: `/query/logs`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

**Form Fields**:
- `log_file`: The log file (required)
- `user_id`: User identifier (optional, defaults to "anonymous")

**Response**: Same format as Text Query

### Send Notification

Send a notification via SMS or WhatsApp.

- **URL**: `/query/notify`
- **Method**: `POST`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
  "user_id": "user123",
  "notification_type": "sms",
  "message": "Your TV issue has been diagnosed: Loose HDMI connection",
  "to_contact": "+1234567890"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Notification sent successfully",
  "notification_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Get User History

Get troubleshooting history for a specific user.

- **URL**: `/query/history/{user_id}`
- **Method**: `GET`

**Response**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123",
    "input_type": "text",
    "query_content": {
      "text": "My TV screen is flickering"
    },
    "solution": {
      "issue": "TV screen flickering",
      "possible_causes": [
        "Loose HDMI connection",
        "Outdated firmware"
      ],
      "confidence_score": 0.85,
      "recommended_steps": [
        {
          "step_number": 1,
          "description": "Check HDMI cable connections"
        },
        {
          "step_number": 2,
          "description": "Update TV firmware"
        }
      ]
    },
    "timestamp": "2025-08-19T22:10:00",
    "status": "completed"
  }
]
```

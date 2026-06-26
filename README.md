# Personal Assistant Voice Agent

## Overview

A FastAPI-based backend service for a personal assistant voice agent integrated with Vapi AI. This project demonstrates how to build a structured, scalable API that handles todo lists, reminders, and calendar events through voice commands processed by artificial intelligence. The application follows clean architecture principles and implements industry best practices for building production-ready APIs.

## Features

- **Todo Management**: Create, list, complete, and delete todo items with descriptions and completion status tracking
- **Reminders**: Set and manage reminders with customizable importance levels for better task prioritization
- **Calendar**: Schedule and track events with detailed start and end times for better time management
- **Call Initiation**: Trigger outbound calls via Vapi AI API for direct customer communication
- **Vapi AI Integration**: Process natural language voice commands and convert them into structured API calls
- **Clean Architecture**: Follows industry best practices with proper separation of concerns across multiple layers
- **Type-Safe Database**: SQLAlchemy ORM with Pydantic validation for data integrity
- **Async Support**: Built with async/await for handling high-concurrency requests efficiently
- **Auto Documentation**: Built-in interactive API documentation with Swagger UI

## Getting Started

### Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.9 or higher** - The project is compatible with Python 3.9+
- **Pip package manager** - For installing Python dependencies
- **Vapi AI account** - Required for voice processing and call functionality (optional for basic features)

### Installation & Setup

Follow these steps to set up and run the application on your local machine:

**Step 1: Clone or Download the Repository**
```bash
git clone https://github.com/abhi-0404/personal_assistant_voice_agent.git
cd personal_assistant_voice_agent
```

**Step 2: Install Required Dependencies**
```bash
pip install -r requirements.txt
```

This will install all required packages:
- FastAPI 0.115.12
- SQLAlchemy 2.0.41
- Pydantic 2.11.4
- Uvicorn 0.34.2
- Requests 2.31.0

**Step 3: Configure Environment Variables**
```bash
# Copy the example environment file to .env
cp .env.example .env
```

Then edit the `.env` file and add your Vapi API key:
```
VAPI_API_KEY=your_actual_api_key_here
VAPI_API_URL=https://api.vapi.ai
```

**Step 4: Run the Application**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-restart when you modify code (useful for development).

**Step 5: Access the Application**

Open your browser and navigate to:
- **Interactive API Documentation**: `http://localhost:8000/docs`
- **Alternative Documentation**: `http://localhost:8000/redoc`
- **API Base URL**: `http://localhost:8000`

## Vapi AI Integration

This service is designed to work seamlessly with Vapi AI's voice assistant platform. Vapi AI handles all speech processing, natural language understanding, and text-to-speech conversion, while this backend manages the business logic and data persistence.

### How It Works

The integration follows this workflow:

1. **Voice Input**: User speaks a command to the voice assistant
2. **Speech Processing**: Vapi AI converts speech to text and understands the user's intent
3. **Tool Call**: Vapi sends a structured HTTP request to our API with the identified function and parameters
4. **Processing**: Our backend validates the request, executes the business logic, and interacts with the database
5. **Response**: Our API returns the operation result with the tool call ID
6. **Speech Output**: Vapi AI converts the response to natural speech and plays it to the user

### Supported Voice Commands

Users can interact with the application using natural language commands:

- **Todo Management**: "Add a new todo to buy groceries" or "Show me all my todos" or "Complete my grocery shopping task"
- **Reminders**: "Remind me to call mom tomorrow at 5 PM" or "Set a high priority reminder to submit the report"
- **Calendar Events**: "Schedule a meeting with the team on Friday from 2 to 3 PM" or "What events do I have next week?"
- **Phone Calls**: "Call customer John at +1-202-555-0123" or "Initiate an outbound call"

## Project Architecture

The application follows a **Clean Layered Architecture** pattern:

```
┌─────────────────────────────────────┐
│      API Routes Layer               │
│  (HTTP Endpoints & Request Entry)   │
├─────────────────────────────────────┤
│      Service Layer                  │
│  (Business Logic & Operations)      │
├─────────────────────────────────────┤
│      Repository Layer               │
│  (Data Access & Database Queries)   │
├─────────────────────────────────────┤
│      Database Layer                 │
│  (SQLite Persistence)               │
└─────────────────────────────────────┘
```

This architecture ensures:
- **Separation of Concerns**: Each layer has a single responsibility
- **Testability**: Layers can be tested independently with mocked dependencies
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new features following the same pattern

## Database Schema

The application uses SQLite with the following tables:

### Todos Table
```
id (Primary Key)
title (String) - Required
description (String) - Optional
completed (Boolean) - Default: False
```

### Reminders Table
```
id (Primary Key)
reminder_text (String) - Required
importance (String) - Priority level (High, Medium, Low)
```

### Calendar Events Table
```
id (Primary Key)
title (String) - Required
description (String) - Optional
event_from (DateTime) - Start time
event_to (DateTime) - End time
```

## Configuration Management

The application uses environment variables for configuration. All sensitive information like API keys should be stored in a `.env` file:

```
VAPI_API_KEY=your_vapi_api_key
VAPI_API_URL=https://api.vapi.ai
```

**Important**: Never commit the `.env` file to version control. Add it to `.gitignore`.

## Technology Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| **FastAPI** | Modern web framework for building APIs | 0.115.12 |
| **SQLAlchemy** | SQL toolkit and ORM for database operations | 2.0.41 |
| **Pydantic** | Data validation and settings management | 2.11.4 |
| **Uvicorn** | ASGI server for running the application | 0.34.2 |
| **SQLite** | Lightweight file-based database | Built-in |
| **Requests** | HTTP library for external API calls | 2.31.0 |
| **Vapi AI** | Voice processing and NLU platform | Third-party |

## API Documentation

The application provides comprehensive API documentation through Swagger UI. Navigate to `http://localhost:8000/docs` to:

- View all available endpoints
- Test endpoints interactively
- See request and response schemas
- Understand error responses

### Main Endpoints

**Todo Operations**:
- `POST /create_todo/` - Create a new todo item
- `POST /get_todos/` - Retrieve all todos
- `POST /complete_todo/` - Mark a todo as completed
- `POST /delete_todo/` - Delete a todo item

**Reminder Operations**:
- `POST /create_reminder/` - Create a new reminder
- `POST /get_reminders/` - Retrieve all reminders
- `POST /delete_reminder/` - Delete a reminder

**Calendar Operations**:
- `POST /create_event/` - Schedule a new event
- `POST /get_events/` - Retrieve all events
- `POST /delete_event/` - Delete an event

**Call Operations**:
- `POST /make_call/` - Initiate an outbound call

## Error Handling

The application implements comprehensive error handling with appropriate HTTP status codes:

- **200 OK**: Successful operation completed
- **400 Bad Request**: Invalid request format or missing tool call
- **404 Not Found**: Requested resource does not exist
- **422 Unprocessable Entity**: Request validation failed (invalid data types or values)
- **500 Internal Server Error**: Unexpected server error

All errors include descriptive messages to help debug issues.

## Logging

The application includes comprehensive logging at all layers:

- **Application Lifecycle**: Startup and shutdown events
- **Database Operations**: Create, update, delete operations
- **API Requests**: Validation and processing
- **Errors**: Detailed error messages with context

Logs include timestamps and are formatted for easy debugging.

## Async Architecture

The application is built with async/await to handle concurrent requests efficiently:

- All route handlers are async functions
- Services implement async methods
- Repository operations are async
- Database sessions use async generators for proper cleanup

This enables the application to handle multiple concurrent requests without blocking.

## Testing

For testing the API:

1. **Manual Testing**: Use Swagger UI at `/docs`
2. **Tool Testing**: Use curl or Postman
3. **Automated Testing**: Create pytest tests for each layer

Example test request:
```bash
curl -X POST http://localhost:8000/create_todo/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "toolCalls": [{
        "id": "call_123",
        "function": {
          "name": "createTodo",
          "arguments": {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
          }
        }
      }]
    }
  }'
```

## Project Structure

```
personal_assistant_voice_agent/
├── src/
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   ├── routes/             # API endpoint definitions
│   │   │   ├── todo.py
│   │   │   ├── reminder.py
│   │   │   ├── calendar_event.py
│   │   │   └── call.py
│   │   └── dependencies.py     # Dependency injection setup
│   ├── services/               # Business logic layer
│   │   ├── todo_service.py
│   │   ├── reminder_service.py
│   │   ├── calendar_event_service.py
│   │   └── call_service.py
│   ├── repositories/           # Data access layer
│   │   ├── base_repository.py
│   │   ├── todo_repository.py
│   │   ├── reminder_repository.py
│   │   └── calendar_event_repository.py
│   ├── models/
│   │   ├── domain/             # Pydantic DTOs
│   │   ├── entities/           # SQLAlchemy models
│   │   ├── base.py
│   │   └── database.py
│   ├── config/
│   │   └── settings.py         # Configuration management
│   └── utils/
│       └── helpers.py          # Utility functions
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── interview.md               # Interview preparation guide
└── interview_questions.md     # Interview Q&A
```

## Design Patterns Used

The project implements several industry-standard design patterns:

- **Clean Architecture**: Layered approach with separation of concerns
- **Generic Repository Pattern**: Reusable CRUD operations for all models
- **Dependency Injection**: Loose coupling and improved testability
- **Data Transfer Objects (DTO)**: Separate models for input/output
- **Service Locator**: FastAPI's dependency injection system

## Performance Considerations

- **Async Operations**: Non-blocking I/O for better concurrency
- **Database Indexing**: Indexed columns for faster queries
- **Connection Pooling**: Efficient database connection management
- **Error Handling**: Early validation prevents unnecessary processing

## Learning Resources

This project demonstrates:
- Building structured APIs with FastAPI
- Implementing clean architecture principles
- Integrating third-party AI services
- Data persistence with SQLAlchemy
- Dependency injection patterns
- Async programming in Python

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


---

Developed by [Abhishek Kumar](https://www.abhisheklive.tech/). Building intelligent voice-powered applications.

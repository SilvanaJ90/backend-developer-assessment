# Technical Evaluation – Backend Developer (Python)

<p align="center">
  <img width="460" height="450" src="h">
</p>

---

### 📑 Table of Contents

1. [Project Planning](#project-planning)  
2. [Project Development](#project-development)  
3. [How to Start It](#how-to-start-it)  
4. [Video](#video)  
5. [Demo](#demo)  
6. [Languages and Tools](#languages-and-tools)  
7. [Authors](#authors)  


---


## Problem
Design and implement a clean, maintainable, and well-documented RESTful API to manage chat message workflows — including validation, processing, storage, and retrieval.  
The goal is to evaluate backend development skills in **Python**, applying clean architecture principles, error handling, testing, and documentation best practices.


---
## 📋 Project Planning

### Project Description
This project consists of a **RESTful API** built with **Python and Flask** that receives, processes, and stores chat messages.  
It includes validation, simple inappropriate-content filtering, metadata generation, and message retrieval by session.

### General Objective
Build a simple and maintainable message-processing API that follows backend development best practices.

### Specific Objectives
- Implement a **POST endpoint** `/api/messages` to receive and validate messages.  
- Implement a **GET endpoint** `/api/messages/{session_id}` to retrieve messages by session, with optional filters.  
- Apply a processing pipeline for validation and metadata creation.  
- Separate concerns into **controllers, services, and repositories**.  
- Include **unit and integration tests** using Pytest.  
- Provide **comprehensive documentation** for the API.

### Project Requirements
- **Python Version**: 3.10+  
- **Framework**: Flask  
- **Database**: SQLite  
- **Testing**: Pytest  
- **Dependencies**: Listed in `requirements.txt`  

---

## ⚙️ Project Development

### 🛠️ Development Phases

| Phase | Description |
|-------|-------------|
| **1. API Design** | Define RESTful endpoints and message data schema. |
| **2. Validation & Processing** | Validate JSON input, filter forbidden words, and generate metadata (word count, length, timestamp). |
| **3. Database Layer** | Implement SQLite database and CRUD operations for message storage. |
| **4. Error Handling** | Create custom error responses with appropriate HTTP status codes. |
| **5. Testing** | Implement unit and integration tests with Pytest (minimum 80% coverage). |
| **6. Documentation** | Document API endpoints in README and/or Swagger UI (if using FastAPI). |



---

## 📘 Example Payload

**POST** `/api/messages`

```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hello, how can I help you today?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```
Response Example:

```{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hello, how can I help you today?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system",
    "metadata": {
      "word_count": 6,
      "character_count": 32,
      "processed_at": "2023-06-15T14:30:01Z"
    }
  }
}
```

Error Example:


```{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Invalid message format",
    "details": "The 'sender' field must be either 'user' or 'system'."
  }
}
```

---



## 🚀 How to Start It

| Step                         | Command | Description |
|------------------------------|---------|-------------|
| Clone the project            | `git clone https://github.com/your-username/backend-developer-assessment-python.git` | Clone the repository |
| Move to project folder       | `cd backend-developer-assessment-python` | Navigate into project directory |
| Create virtual environment   | `python -m venv .venv` | Create isolated Python environment |
| Activate on Windows          | `.\.venv\Scripts\Activate.ps1` | Activate environment on Windows |
| Activate on macOS/Linux      | `source .venv/bin/activate` | Activate environment on macOS/Linux |
| Install dependencies         | `pip install -r requirements.txt` | Install all required packages |
| Run development server (FastAPI) | `` | Start the API locally |
| Run tests                    | `` | Run tests with coverage report |



---

## 🎥 Video Mia
[![Video ]]()

---

## 💻 Demo
You can try the live demo here:  
👉 [View Demo]()  

---

## 🛠️ Languages and Tools

### Backend
<p align="left">
  <a href="https://www.python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  </a>
</p>


---

## 👩‍💻 Authors
[![Mia contributors](https://contrib.rocks/image?repo=SilvanaJ90/backend-developer-assessment)](https://github.com/SilvanaJ90/backend-developer-assessment/graphs/contributors)  

# Task Manager API

Task management API built with FastAPI.

## Features
- Create, update, delete, and retrieve tasks
- Assign priorities and due dates
- Mark tasks as complete
- Filter tasks by priority and completion status

## Installation

1. Clone the repository:
    ```git clone https://github.com/Joe-Whitworth/task-manager-api.git cd task-manager-api```


2. Create a virtual environment and install dependencies:
    ```python -m venv venv source venv/bin/activate # On Windows, use venv\Scripts\activate pip install -r requirements.txt```


3. Run the application:
    ```uvicorn app.main:app --reload```

## Example Requests

1. Add new task:
    ```
    curl --location 'http://127.0.0.1:8000/tasks/' \
        --header 'Content-Type: application/json' \
        --data '{
           "title": "Task name",
           "description": "Task description.",
           "priority": Task priority (1 = High, 2 = Medium, 3 = Low),
           "due_date": "2025-02-05T12:00:00"
         }'

2. Get all tasks:
    ```
    curl --location 'http://127.0.0.1:8000/tasks/' \
        --header 'Accept: application/json'

3. Delete user:
    ```
    curl --location --request DELETE 'http://127.0.0.1:8000/tasks/1/'

4. Update a task: 
    ```
    curl --location --request PUT 'http://127.0.0.1:8000/tasks/2/' \
        --header 'Content-Type: application/json' \
        --data '{
           "title": "Task title",
           "description": "Task desription.",
           "priority": Task priority (1 = High, 2 = Medium, 3 = Low),
           "due_date": "2025-02-05T12:00:00",
           "completed": true
         }'


## API Documentation

Once the server is running, access the API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests

Run unit tests with:
```pytest```


## Future Improvements

- Add user authentication 
- Implement task categories and tagging
- Introduce due date reminders via email or notifications
- Optimise database queries for better performance
- Use pagination for larger quantities



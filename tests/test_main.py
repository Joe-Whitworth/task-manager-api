import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  

client = TestClient(app)

def create_task(priority=2):
    return client.post("/tasks/", json={
        "title": "Test Task",
        "description": "This is a test",
        "priority": priority,
        "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat()
    })

# 1. CREATE TASK TESTS

def test_create_task_success():
    response = create_task(priority=2)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == 2
    assert "id" in data

def test_create_task_invalid_priority():
    response = create_task(priority=4) 
    assert response.status_code == 422  

def test_create_task_missing_title():
    response = client.post("/tasks/", json={
        "description": "No title",
        "priority": 2,
        "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat()
    })
    assert response.status_code == 422

# 2. GET TASKS TESTS

def test_get_all_tasks():
    """Test retrieving all tasks when at least one task exists."""
    create_task()  
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id():
    """Test retrieving a task by ID."""
    task_response = create_task()
    task_id = task_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}/")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_get_nonexistent_task():
    """Test retrieving a non-existent task (edge case)."""
    response = client.get("/tasks/invalid-id/")
    assert response.status_code == 404 

# 3. UPDATE TASK TESTS

def test_update_task_success():
    """Test successfully updating a task."""
    task_response = create_task()
    task_id = task_response.json()["id"]

    response = client.put(f"/tasks/{task_id}/", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_update_task_invalid_priority():
    """Test updating a task with an invalid priority (edge case)."""
    task_response = create_task()
    task_id = task_response.json()["id"]

    response = client.put(f"/tasks/{task_id}/", json={"priority": 5})
    assert response.status_code == 422  

def test_update_nonexistent_task():
    """Test updating a task that does not exist (edge case)."""
    response = client.put("/tasks/nonexistent-id/", json={"title": "Should not work"})
    assert response.status_code == 404  

# 4. DELETE TASK TESTS

def test_delete_task_success():
    task_response = create_task()
    task_id = task_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}/")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully."

def test_delete_nonexistent_task():
    response = client.delete("/tasks/nonexistent-id/")
    assert response.status_code == 404  

def test_delete_task_twice():
    task_response = create_task()
    task_id = task_response.json()["id"]

    client.delete(f"/tasks/{task_id}/")  
    response = client.delete(f"/tasks/{task_id}/")  
    assert response.status_code == 404  

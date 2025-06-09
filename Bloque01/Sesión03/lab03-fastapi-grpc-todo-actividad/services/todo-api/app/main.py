from fastapi import FastAPI
from pydantic import BaseModel
import grpc
import todo_pb2
import todo_pb2_grpc
from config import settings

app = FastAPI(root_path="/api")

class TodoCreate(BaseModel):
    title: str
    description: str

class UserCreateRequest(BaseModel):
    username: str
    email: str

channel = grpc.insecure_channel(f"{settings.GRPC_SERVER}:{settings.GRPC_PORT}")
stub = todo_pb2_grpc.TodoServiceStub(channel)

# Canal stub User
user_stub = todo_pb2_grpc.UserServiceStub(channel)

@app.post("/todos")
def create_todo(todo: TodoCreate):
    response = stub.CreateTodo(todo_pb2.CreateTodoRequest(
        title=todo.title,
        description=todo.description
    ))
    return {"id": response.id}

@app.get("/todos")
def get_todos():
    response = stub.GetTodos(todo_pb2.GetTodosRequest())
    return [{"id": t.id, "title": t.title, "description": t.description} for t in response.todos]

# endopints para users
@app.post("/create_user/")
def create_user(user: UserCreateRequest):
    request = todo_pb2.CreateUserRequest(username=user.username, email=user.email)
    response = user_stub.CreateUser(request)
    return {"id": response.id}

@app.get("/get_user/{id}")
def get_user(id: int):
    request = todo_pb2.GetUserRequest(id=id)
    response = user_stub.GetUser(request)
    return {
        "id": response.id,
        "username": response.username,
        "email": response.email
    }

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


channel = grpc.insecure_channel(f"{settings.GRPC_SERVER}:{settings.GRPC_PORT}")
stub = todo_pb2_grpc.TodoServiceStub(channel)

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
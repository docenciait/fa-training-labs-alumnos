import grpc
from concurrent import futures
from database import SessionLocal, init_db
from models import Todo
import todo_pb2
import todo_pb2_grpc

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    def CreateTodo(self, request, context):
        db = SessionLocal()
        todo = Todo(title=request.title, description=request.description)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo_pb2.CreateTodoResponse(id=todo.id)

    def GetTodos(self, request, context):
        db = SessionLocal()
        todos = db.query(Todo).all()
        todo_list = [
            todo_pb2.Todo(id=t.id, title=t.title, description=t.description) for t in todos
        ]
        return todo_pb2.GetTodosResponse(todos=todo_list)

def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
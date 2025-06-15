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
    

# UserService

class UserService(todo_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = []
        self.next_id = 1

    def CreateUser(self, request, context):
        user = {
            "id": self.next_id,
            "username": request.username,
            "email": request.email
        }
        self.users.append(user)
        self.next_id += 1
        return todo_pb2.CreateUserResponse(id=user["id"])

    def GetUser(self, request, context):
        for user in self.users:
            if user["id"] == request.id:
                return todo_pb2.GetUserResponse(**user)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('User not found')
        return todo_pb2.GetUserResponse()

def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    
    todo_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server) # Añádirmos nuevo servicio

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
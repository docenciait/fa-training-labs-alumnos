
# Actividad. Crear en todo-grpc/app/proto/todo.proto

-> Crear un contrato con protobuf que tenga las siguientes especificaciones

- Servicio
    - Nombre: TodoService
    - Procedimiento1:
        - Nombre: CreateTodo
        - Entrada: CreateTodoRequest (title, description)
        - Retorno; CreateTodoResponse (id)
    - Procedimiento2:
        - Nombre GetTodos 
        - Entrada: GetTodosRequest ()
        - Retorno; GetTodosResponse (lista todos)

# Actividad 2.

# Actividad planteada

- Crear un nuevo servicio e integrarlo en el propio todo.proto:

- Nombre servicio: UserService
- Procedimientos:
  1. CreateUser:
    - Entrada: CreateUserRequest (username, emal)
    - Salida: CreateUserResponse (id)
  2. GetUser:
    - Entrada GetUserRequest (id)
    - Salida GetUserResponse (id, username, email)

> Por simplicidad no haremos orm así que en nuestro servidor usaríamos una simulación del crud.


```python
import grpc
from concurrent import futures
import todo_pb2
import todo_pb2_grpc

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    # Implementación actual del servicio de TODOs con SQLAlchemy
    ...

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
                return todo_pb2.GetUserResponse(
                    id=user["id"],
                    username=user["username"],
                    email=user["email"]
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('User not found')
        return todo_pb2.GetUserResponse()


```
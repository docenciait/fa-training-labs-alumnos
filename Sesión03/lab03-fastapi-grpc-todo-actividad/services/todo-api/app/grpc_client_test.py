import grpc
import todo_pb2
import todo_pb2_grpc

def run():
    # Conectar al servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = todo_pb2_grpc.TodoServiceStub(channel)

    # Crear un nuevo TODO
    # create_response = stub.CreateTodo(todo_pb2.CreateTodoRequest(
    #     title="Tarea de prueba",
    #     description="Esta es una tarea creada desde el cliente de prueba"
    # ))
    # print(f"Todo creado con ID: {create_response.id}")

    # Obtener todos los TODOs
    get_response = stub.GetTodos(todo_pb2.GetTodosRequest())
    for todo in get_response.todos:
        print(f"Todo ID: {todo.id}, Título: {todo.title}, Descripción: {todo.description}")

if __name__ == '__main__':
    run()

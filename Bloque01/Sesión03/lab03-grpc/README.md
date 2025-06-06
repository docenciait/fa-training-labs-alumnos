
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

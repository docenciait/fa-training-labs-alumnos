## 🎯 Enunciado del problema

Construiremos un microservicio de productos con **Arquitectura Hexagonal** en FastAPI. Este servicio permitirá:

* Crear un producto
* Listar todos los productos

Aplicaremos una separación rigurosa entre dominio, puertos, infraestructura y adaptadores de entrada (FastAPI).

---

## 📐 Diagrama de Arquitectura Hexagonal

```mermaid
flowchart TD
    subgraph Domain
      Product[Entidad: Product] --> Event[Evento: ProductCreated]
    end

    subgraph Application
      ServicePort[Puerto Entrada: ProductServicePort] --> AppService[Servicio Aplicación: ProductApplicationService]
      AppService --> RepoPort[Puerto Salida: ProductRepositoryPort]
    end

    subgraph Infrastructure
      MariaDBRepo[MariaDBProductRepository] --> DB[Base de datos MariaDB]
    end

    subgraph Interfaces
      FastAPI[FastAPI Router] --> ServicePort
    end

    RepoPort --> MariaDBRepo
    FastAPI --> AppService
```

# 🏢 LAB 1 - Monolito Inicial: Usuarios, Pedidos, Pagos

## 🎯 Enunciado

Este laboratorio parte de un sistema monolítico que incluye:

- **Usuarios** (`Users`): Registro, Login.
- **Pedidos** (`Orders`): Crear y listar pedidos.
- **Pagos** (`Payments`): Realizar pagos sobre pedidos.

Todo el sistema está acoplado en una única aplicación FastAPI y una sola base de datos **MariaDB**.

## ⚡ Stack

- Python 3.12
- FastAPI
- Pydantic v2
- MariaDB 11.2
- Docker Compose
- Raw SQL (`pymysql`)

## Estructura

```bash
lab1-monolito-orm/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── items.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── item_service.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud_item.py
│   └── core/
│       ├── __init__.py
│       └── config.py
├── tests/
│   ├── __init__.py
│   └── test_items.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── requirements.txt
└── README.md

```

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/tuorg/lab1-monolito-inicial.git
cd lab1-monolito-inicial

# Levantar contenedores
make up

# Inicializar base de datos
make db-init

# Test rápido
make test-curl

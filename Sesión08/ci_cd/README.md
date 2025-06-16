
# 🛠 CI/CD para Proyectos FastAPI con Microservicios y Arquitectura Hexagonal

---

##  Objetivo General

Diseñar e implementar un pipeline CI/CD profesional que:

* Automatizar pruebas, linting y análisis estático.
* Construir imágenes Docker y publicarlas.
* Despliegue automático de microservicios FastAPI (con arquitectura hexagonal) en un entorno controlado (Minikube, Kubernetes, Docker Swarm, o nube).
* Implementación de validaciones de calidad y seguridad (OWASP, dependencias, escaneo de contenedores).

---



## 🧱 Estructura del proyecto

```
cqrs_product/
├── app/
│   ├── domain/
│   │   └── entities/product.py
│   ├── application/
│   │   ├── commands/create_product.py
│   │   ├── queries/get_product.py
│   │   ├── dtos/
│   │   │   └── product_dto.py
│   │   ├── ports/
│   │   │   └── product_repository.py
│   ├── infrastructure/
│   │   └── memory/product_repository.py
│   ├── interfaces/
│   │   └── api/routes.py
│   └── main.py
├── tests/
│   └── test_routes.py
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

---

##  Funcionalidad mínima

###  Commands (write)

* `POST /products` → crea producto

###  Queries (read)

* `GET /products/{id}` → obtiene producto
* `GET /products` → lista todos los productos

---

##  Componentes clave para CI/CD

* `ProductRepositoryPort`: puerto hexagonal
* `InMemoryProductRepository`: adaptador
* `CreateProductCommandHandler` y `GetProductQueryHandler`
* Test para flujo de creación + consulta
* Configuración de `pytest`, `mypy`, `ruff`, `bandit`, `coverage`, `Makefile`

---


---

## ⚙️ Fases del Pipeline CI/CD

### 1. 🔍 Etapa de Validación y Calidad (CI)

* **Linting** con `ruff` o `flake8`
* **Tests** con `pytest`
* **Cobertura** con `coverage`
* **Análisis estático** con `bandit`, `mypy`, `safety`
* **Formato** con `black`

```yaml
- name: Run linters
  run: |
    pip install black ruff
    black --check .
    ruff .
```

```yaml
- name: Run tests and coverage
  run: |
    pip install -r requirements.txt
    pytest --cov=app tests/
```

---

### 2. 🐳 Construcción y Publicación de Imágenes Docker

* Nombrar por commit SHA, tag o rama
* Subir a GitHub Container Registry o Docker Hub

```yaml
- name: Build Docker image
  run: docker build -t ghcr.io/org/users:${{ github.sha }} .

- name: Push Docker image
  run: |
    echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    docker push ghcr.io/org/users:${{ github.sha }}
```

---

### 3. 🚀 Despliegue Automático (CD)

#### 🔁 En entorno local (Minikube/K3s):

* GitHub Actions no puede acceder directamente a Minikube. Se puede usar un **webhook listener** o **manual trigger** post-push (por ejemplo, con Skaffold o ArgoCD local).

#### 🌐 En nube (GCP/AWS/Azure/Kubernetes con acceso remoto):

```yaml
- name: Deploy to Kubernetes
  uses: azure/setup-kubectl@v3
  with:
    version: 'v1.29.0'

- name: Set context
  run: kubectl config set-context ...

- name: Apply manifests
  run: |
    kubectl apply -f k8s/users-deployment.yaml
    kubectl rollout status deployment/users-deployment
```

---

### 4. ✅ Post-Despliegue

* Pruebas end-to-end (`pytest + httpx`)
* Escaneo OWASP ZAP o Trivy (imágenes)

```yaml
- name: Scan Docker image with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/org/users:${{ github.sha }}
```

---

## 💡 Integraciones Recomendadas

| Herramienta          | Propósito                          |
| -------------------- | ---------------------------------- |
| `black`, `ruff`      | Linting y formateo                 |
| `pytest`, `coverage` | Tests unitarios y cobertura        |
| `bandit`, `safety`   | Seguridad de código y dependencias |
| `Trivy`              | Escaneo de imágenes Docker         |
| `GitHub Actions`     | Automatización del pipeline        |
| `Skaffold`, `Tilt`   | Deploy local Kubernetes (Dev)      |
| `ArgoCD`, `Flux`     | GitOps (producción)                |

---

## 🧪 Ejemplo de GitHub Action (ci-cd.yaml)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install deps
      run: |
        pip install -r services/users/requirements.txt

    - name: Run linters and tests
      run: |
        cd services/users
        black --check .
        ruff .
        pytest --cov=app tests/

    - name: Build and push Docker image
      run: |
        docker build -t ghcr.io/org/users:${{ github.sha }} services/users
        echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
        docker push ghcr.io/org/users:${{ github.sha }}

    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/users-deployment.yaml
```

---

## 🧠 Buenas Prácticas

* Cada microservicio debe tener su propio pipeline (por ejemplo, monorepo con múltiples workflows o repos independientes).
* Usar etiquetas semánticas para versiones (`v1.2.3`)
* Escaneo regular de vulnerabilidades (`dependabot`, `trivy`)
* Separar entornos: dev, staging, production
* Automatizar rollback si falla el despliegue

---


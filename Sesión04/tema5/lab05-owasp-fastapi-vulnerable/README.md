
# 🧪 LAB 5 – Análisis de Vulnerabilidades OWASP en un Microservicio FastAPI 

| Ítem           | Detalle                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------- |
| 🕒 Duración    | 1.5 – 2 horas                                                                                |
| 🎯 Objetivo    | Detectar y mitigar vulnerabilidades OWASP Top 10 en FastAPI                                  |
| 🧠 Temas       | Seguridad, OWASP Top 10, ZAP, CORS, SQL Injection, cabeceras HTTP                            |
| ⚙️ Tecnologías | FastAPI, Docker, SQLite, OWASP ZAP, pip-audit, safety                                        |
| 📁 Repositorio | [`lab05-owasp-fastapi-vulnerable.zip`](sandbox:/mnt/data/lab05-owasp-fastapi-vulnerable.zip) |
| 🧪 Entregable  | Microservicio corregido + informe OWASP + tests + Makefile seguro                            |

---

## 1️⃣ Lanzar el entorno vulnerable

### 🔧 Requisitos

* Docker y Docker Compose
* Python 3.12 (si usas Makefile fuera del contenedor)
* OWASP ZAP instalado (GUI o CLI)

### 📦 Instalación y ejecución

```bash

# Inicializar base de datos
make init-db

# Lanzar servicio vulnerable
make run
```

Accede a [http://localhost:8000](http://localhost:8000)
Explora también: `/item/1`, `/item/' OR 1=1`

---

## 2️⃣ Ejecutar análisis de seguridad con OWASP ZAP

###  GUI interactiva

1. Abrir [OWASP ZAP](https://www.zaproxy.org/download/)
2. Iniciar escaneo activo sobre `http://localhost:8000`
3. Explora con navegador o curl antes de escanear:

   ```bash
   curl "http://localhost:8000/item/' OR 1=1 --"
   curl "http://localhost:8000/item-injection/%27%20OR%20%271%27=%271"
   ```
4. Revisa alertas en ZAP: inyección, CORS, cabeceras, etc.
5. Exporta el informe: `zap_report.html`

---



---

# Detectar vulnerabilidades y solucionar

Gracias por compartir el informe ZAP. A partir del análisis, se ha detectado una única vulnerabilidad activa con **riesgo bajo y confianza media**, específicamente:

---

## 🚨 Vulnerabilidad detectada

### ⚠️ Falta de cabecera HTTP: `X-Content-Type-Options`

| Detalle                  | Valor                                                                                                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🔎 Descripción           | El encabezado `X-Content-Type-Options` no está presente, lo que permite a navegadores realizar "MIME sniffing" y alterar el tipo de contenido interpretado. Esto puede abrir la puerta a ataques XSS. |
| 🧩 Riesgo OWASP          | A05:2021 – Security Misconfiguration                                                                                                                                                                  |
| 🧷 CWE ID                | [CWE-693](https://cwe.mitre.org/data/definitions/693.html)                                                                                                                                            |
| 🧪 Detectado en          | `GET http://localhost:8000`                                                                                                                                                                           |
| 🛠 Recomendación oficial | Añadir la cabecera: `X-Content-Type-Options: nosniff`                                                                                                                                                 |

---


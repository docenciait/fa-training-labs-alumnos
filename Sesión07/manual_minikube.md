Aquí te detallo cómo usar Minikube en Windows y lanzar un despliegue, paso a paso. Recuerda que, aunque soy un modelo de lenguaje y no tengo percepciones, he sido entrenado con la información más reciente hasta mi última actualización para darte la mejor guía posible.

### 1\. Requisitos Previos para Minikube en Windows

Antes de instalar Minikube, asegúrate de tener lo siguiente:

  * **Sistema Operativo:** Windows 10/11.

  * **Virtualización:** Minikube necesita un hypervisor (software de virtualización) para crear la máquina virtual donde correrá Kubernetes. Las opciones más comunes son:

      * **Docker Desktop (Recomendado):** Incluye un motor Docker y usa Hyper-V (Windows Pro/Enterprise) o WSL 2 (todas las versiones de Windows 10/11) como backend de virtualización. Es la opción más sencilla y moderna.
      * **Hyper-V (Windows 10 Pro/Enterprise/Education):** Si tienes estas versiones de Windows, es una excelente opción nativa. Necesitarás habilitarlo en "Activar o desactivar las características de Windows".
      * **VirtualBox:** Si tienes Windows Home o prefieres VirtualBox, puedes usarlo, pero la configuración es un poco más manual.
      * **WSL 2 (Windows Subsystem for Linux 2):** Es una alternativa popular y eficiente, especialmente si ya trabajas con Linux en Windows.

  * **`kubectl`:** La herramienta de línea de comandos de Kubernetes. Minikube la descarga automáticamente si no la tienes, pero es bueno tenerla instalada por separado para mayor control.

### 2\. Instalación de Minikube en Windows (Recomendado: Con Docker Desktop y WSL 2)

La forma más sencilla y moderna de usar Minikube en Windows es con Docker Desktop (que puede usar WSL 2 como su backend).

**Paso 1: Instalar Docker Desktop (si no lo tienes)**

1.  Descarga Docker Desktop desde su sitio web oficial: [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)
2.  Sigue las instrucciones de instalación. Asegúrate de que WSL 2 esté habilitado y configurado correctamente durante la instalación si te lo pide (Docker Desktop lo gestiona bastante bien). Reinicia tu equipo si es necesario.
3.  Una vez instalado, abre Docker Desktop y asegúrate de que esté funcionando.

**Paso 2: Descargar Minikube**

1.  Abre PowerShell o CMD como **administrador**.

2.  Descarga Minikube usando `curl` o un navegador y muévelo a tu `PATH` (por ejemplo, a `C:\minikube` y añade `C:\minikube` a tus variables de entorno PATH, o simplemente colócalo en `C:\Windows\System32` para acceso global).

    La forma más sencilla es usar `winget` (si lo tienes, viene con versiones recientes de Windows):

    ```powershell
    winget install minikube
    ```

    O descarga el ejecutable directamente:

    ```powers_shell
    Invoke-WebRequest -OutFile minikube.exe https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe
    Move-Item minikube.exe C:\minikube\minikube.exe # Mueve a una carpeta en tu PATH
    ```

    Si no tienes `C:\minikube` en tu PATH, puedes añadirlo o simplemente ejecutar `minikube.exe` desde la carpeta donde lo descargaste.

**Paso 3: Instalar `kubectl` (si no lo tienes)**

Minikube puede descargarlo por ti, pero si quieres controlarlo:

1.  Abre PowerShell o CMD como **administrador**.
2.  Descarga `kubectl`:
    ```powershell
    curl.exe -LO "https://dl.k8s.io/release/v1.29.0/bin/windows/amd64/kubectl.exe" # Cambia v1.29.0 por la versión deseada
    Move-Item kubectl.exe C:\minikube\kubectl.exe # Mueve a la misma carpeta que minikube
    ```
    Asegúrate de que `C:\minikube` (o la carpeta donde los guardaste) esté en tu variable de entorno `Path` para poder ejecutar `minikube` y `kubectl` desde cualquier ubicación.

### 3\. Iniciar Minikube

Ahora que tienes los componentes, puedes iniciar tu clúster de Kubernetes local.

1.  Abre **PowerShell o CMD (no necesariamente como administrador para este paso, a menos que tengas problemas de permisos con el driver)**.

2.  Inicia Minikube, especificando el driver si no quieres usar el predeterminado (que suele ser `docker` si lo tienes):

      * **Con Docker Desktop (recomendado):**
        ```bash
        minikube start --driver=docker
        ```
      * **Con Hyper-V (si Docker Desktop no es tu opción o tienes Pro/Enterprise):**
        ```bash
        minikube start --driver=hyperv
        ```
        (Asegúrate de que Hyper-V esté habilitado en "Activar o desactivar las características de Windows").
      * **Con VirtualBox (si no tienes Docker o Hyper-V):**
        ```bash
        minikube start --driver=virtualbox
        ```
        (Asegúrate de tener VirtualBox instalado).

    El comando `minikube start` descargará las imágenes necesarias, creará la VM (o el contenedor Docker), y configurará tu `kubectl` para apuntar a este nuevo clúster. Esto puede tardar unos minutos la primera vez.

3.  Verifica el estado de Minikube:

    ```bash
    minikube status
    ```

    Debería mostrar algo como:

    ```
    minikube
    type: Control Plane
    host: Running
    kubelet: Running
    apiserver: Running
    kubeconfig: Configured
    ```

4.  Verifica que `kubectl` esté apuntando a Minikube:

    ```bash
    kubectl cluster-info
    kubectl get nodes
    ```

    Deberías ver un nodo llamado `minikube`.

### 4\. Lanzar un Despliegue (Deployment) en Minikube

Ahora que Minikube está funcionando, vamos a lanzar un despliegue de una aplicación simple.

**Paso 1: Crear el archivo YAML del Deployment**

Vamos a crear un `Deployment` para una aplicación Nginx. Crea un archivo llamado `nginx-deployment.yaml` en tu directorio de trabajo (por ejemplo, `C:\kube-apps`):

```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2 # Queremos 2 réplicas (Pods) de Nginx
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx-container
        image: nginx:latest # Usaremos la imagen oficial de Nginx
        ports:
        - containerPort: 80 # Nginx expone el puerto 80
```

**Paso 2: Aplicar el Deployment**

En tu terminal (PowerShell o CMD), navega al directorio donde guardaste `nginx-deployment.yaml` y aplica el despliegue:

```bash
kubectl apply -f nginx-deployment.yaml
```

Deberías ver una salida como: `deployment.apps/nginx-deployment created`

**Paso 3: Verificar el Deployment y los Pods**

Comprueba si el `Deployment` y los `Pods` se han creado correctamente:

```bash
kubectl get deployments
kubectl get pods
```

Deberías ver:

  * `nginx-deployment` en el listado de `deployments`.
  * Dos `Pods` (con nombres generados automáticamente como `nginx-deployment-xxxxx-yyyyy`) en estado `Running`.

### 5\. Exponer el Despliegue con un Servicio (Service)

Los Pods tienen IPs internas al clúster que cambian. Para acceder a tu aplicación desde fuera del clúster (o para que otras aplicaciones dentro del clúster puedan accederla de forma estable), necesitas un `Service`.

**Paso 1: Crear el archivo YAML del Service**

Crea un archivo llamado `nginx-service.yaml` en el mismo directorio:

```yaml
# nginx-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx # Debe coincidir con la etiqueta 'app' de los Pods de Nginx
  ports:
    - protocol: TCP
      port: 80         # Puerto del Service
      targetPort: 80   # Puerto del contenedor (el puerto 80 de Nginx)
  type: LoadBalancer   # Tipo de Service: Minikube lo expone en una IP accesible
```

**Paso 2: Aplicar el Service**

En tu terminal, aplica el servicio:

```bash
kubectl apply -f nginx-service.yaml
```

Deberías ver una salida como: `service/nginx-service created`

**Paso 3: Acceder a la Aplicación**

Minikube te permite acceder a los `Services` de tipo `LoadBalancer` (o `NodePort`) fácilmente:

```bash
minikube service nginx-service
```

Este comando abrirá automáticamente tu navegador web con la URL donde tu aplicación Nginx está expuesta. Deberías ver la página de bienvenida de Nginx.

### 6\. Detener y Eliminar Minikube

Cuando hayas terminado de trabajar con Minikube, puedes detenerlo o eliminarlo para liberar recursos.

  * **Detener Minikube (mantiene el estado del clúster):**

    ```bash
    minikube stop
    ```

  * **Eliminar Minikube (borra el clúster y la VM/contenedor):**

    ```bash
    minikube delete
    ```

### Consejos Adicionales:

  * **Minikube Dashboard:** Puedes abrir el Dashboard de Kubernetes para una interfaz gráfica:
    ```bash
    minikube dashboard
    ```
  * **Contexto de `kubectl`:** Asegúrate de que `kubectl` esté siempre apuntando al clúster de Minikube. Minikube lo configura automáticamente, pero si trabajas con otros clústeres, puedes cambiar el contexto:
    ```bash
    kubectl config use-context minikube
    ```
  * **Troubleshooting:** Si encuentras problemas, el mensaje de error suele ser muy descriptivo. Busca en la documentación de Minikube o en foros como Stack Overflow. Los problemas de virtualización o permisos suelen ser los más comunes.
  * **Resources:** Si Minikube tiene problemas para iniciarse o tu clúster parece lento, puedes asignar más recursos (CPU, memoria) a la VM/contenedor de Minikube:
    ```bash
    minikube start --driver=docker --memory=4096mb --cpus=2
    ```
    (Haz esto *antes* de iniciar Minikube por primera vez o después de un `minikube delete`).

---

¡Genial! Tus archivos `Deployment.yaml` y `Service.yaml` para tu aplicación FastAPI **lucen correctos y bien estructurados**.

Vamos a revisar los puntos clave de cada uno y luego te explico cómo usarlos y qué tener en cuenta, especialmente con la imagen local.

---

### Tu `fastapi-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: fastapi-k8s-app # Nombre de tu imagen local
        imagePullPolicy: Never # Crucial: indica a Kubernetes que no intente descargarla de un registro
        ports:
          - containerPort: 8000 # El puerto que tu aplicación FastAPI escucha dentro del contenedor
```

**Análisis:**
* **`image: fastapi-k8s-app`**: Este es el nombre de tu imagen Docker. Al usar `imagePullPolicy: Never`, estás indicando que esta imagen debe existir ya en el demonio Docker de Minikube.
* **`containerPort: 8000`**: Esto significa que tu aplicación FastAPI dentro del contenedor está configurada para escuchar en el puerto `8000`. Esto es fundamental y debe coincidir con cómo inicias tu FastAPI (ej., `uvicorn main:app --host 0.0.0.0 --port 8000`).
* **`replicas: 1`**: Solo tendrás una instancia (Pod) de tu aplicación. Puedes cambiarlo a `2` o más si quieres probar el escalado.

---

### Tu `fastapi-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi # Debe coincidir con la etiqueta 'app' de tu Deployment
  type: NodePort # Expondrá el servicio directamente en un puerto del nodo Minikube
  ports:
    - protocol: TCP
      port: 80      # El puerto del Service (el puerto "interno" del clúster para acceder a tu app)
      targetPort: 8000 # El puerto del contenedor al que el Service enviará el tráfico (debe coincidir con containerPort del Deployment)
      nodePort: 30080 # El puerto específico en el nodo Minikube que se abrirá (debe ser entre 30000-32767)
```

**Análisis:**
* **`selector: app: fastapi`**: Esto es **clave**. Es lo que permite que el Service encuentre y dirija el tráfico a los Pods creados por tu `fastapi-deployment` (ya que ambos tienen la etiqueta `app: fastapi`).
* **`type: NodePort`**: Es una buena elección para desarrollo local con Minikube. Abre un puerto fijo (`nodePort`) en la IP de la máquina virtual de Minikube, permitiéndote acceder a tu aplicación desde tu máquina Windows.
* **`port: 80`**: Este es el puerto interno del Service dentro del clúster. Si otro Pod dentro del clúster quisiera hablar con tu FastAPI, lo haría a `fastapi-service:80`.
* **`targetPort: 8000`**: Esto es **fundamental**. Significa que cuando el Service reciba tráfico en su `port: 80`, lo reenviará al puerto `8000` de los contenedores que coincidan con el `selector`. **Este `targetPort` debe ser el mismo que el `containerPort` de tu Deployment.** Lo tienes correctamente configurado.
* **`nodePort: 30080`**: Este es el puerto por el que accederás a tu aplicación desde tu máquina host (Windows). Es un puerto directamente abierto en la VM de Minikube.

---

### Pasos para Desplegar y Acceder a tu FastAPI en Minikube

Asumiendo que Minikube ya está corriendo (`minikube start`) y tus archivos `.yaml` están guardados (ej., en `C:\fastapi-app`):

1.  **Asegúrate de que la imagen `fastapi-k8s-app` esté en el demonio Docker de Minikube.**
    Dado que usas `imagePullPolicy: Never`, Minikube no intentará descargar la imagen. Debes haberla construido *directamente en el entorno Docker de Minikube*.

    Para ello, en tu terminal (PowerShell o CMD):
    * **Configura tu entorno Docker para Minikube:**
        ```powershell
        minikube docker-env | Invoke-Expression
        ```
        (Si estás en Bash/Zsh, sería `eval $(minikube docker-env)`).
        Esto cambia las variables de entorno de tu terminal para que los comandos `docker` se dirijan al demonio Docker que corre dentro de la VM de Minikube.
    * **Construye tu imagen (¡desde el directorio de tu Dockerfile de FastAPI!):**
        ```bash
        docker build -t fastapi-k8s-app .
        ```
        Asegúrate de que estás en el directorio donde tienes tu `Dockerfile` para la aplicación FastAPI.

2.  **Aplica el Deployment:**
    Navega al directorio donde guardaste `fastapi-deployment.yaml` y `fastapi-service.yaml`.
    ```bash
    cd C:\fastapi-app # O donde sea que estén tus archivos
    kubectl apply -f fastapi-deployment.yaml
    ```
    Deberías ver: `deployment.apps/fastapi-deployment created`.

3.  **Aplica el Service:**
    ```bash
    kubectl apply -f fastapi-service.yaml
    ```
    Deberías ver: `service/fastapi-service created`.

4.  **Verifica el estado de los recursos:**
    ```bash
    kubectl get deployments
    kubectl get pods
    kubectl get services
    ```
    Asegúrate de que tu Pod de FastAPI esté en estado `Running` y tu Service esté listado.

5.  **Accede a tu aplicación FastAPI:**
    Tienes dos formas, ambas válidas:

    * **Opción 1 (Recomendada con `NodePort`): Usar `minikube service`**
        ```bash
        minikube service fastapi-service
        ```
        Minikube detectará que tienes un `NodePort` y abrirá automáticamente tu navegador a la URL y puerto correctos (que será algo como `http://<IP_de_Minikube>:30080`).

    * **Opción 2: Acceder directamente por IP y `nodePort`**
        Primero, obtén la IP de tu clúster Minikube:
        ```bash
        minikube ip
        ```
        Esto te devolverá una dirección IP (ej., `192.168.49.2`).
        Luego, puedes acceder a tu aplicación desde tu navegador o Postman/curl usando esa IP y el `nodePort` que definiste:
        ```
        http://<IP_DE_MINIKUBE>:30080
        ```
        Por ejemplo: `http://192.168.49.2:30080`

---

### Solución de Problemas Comunes

* **Pod en estado `Pending` o `ErrImagePull`**:
    * **`imagePullPolicy: Never`**: Lo más probable es que la imagen `fastapi-k8s-app` no se haya construido correctamente en el demonio Docker de Minikube. Asegúrate de ejecutar `minikube docker-env | Invoke-Expression` *antes* de `docker build -t fastapi-k8s-app .` y que el `docker build` se complete sin errores.
    * **Nombre de imagen incorrecto**: Revisa que el nombre (`fastapi-k8s-app`) sea idéntico en el `docker build` y en el `Deployment.yaml`.
* **Pod en estado `CrashLoopBackOff`**:
    * Esto significa que tu aplicación dentro del contenedor se está iniciando y luego fallando.
    * **Revisa los logs del Pod**: Usa `kubectl logs <nombre_de_tu_pod_fastapi>` (obtén el nombre completo con `kubectl get pods`). Esto te dará la salida de tu aplicación y probablemente el error.
    * **`containerPort` incorrecto**: Asegúrate de que tu aplicación FastAPI esté realmente escuchando en el puerto `8000` dentro del contenedor, y que `containerPort: 8000` esté bien escrito en el `Deployment`.
* **No puedo acceder a la aplicación desde el navegador**:
    * Asegúrate de que el Pod esté `Running`.
    * Verifica que `targetPort: 8000` en el Service coincide con `containerPort: 8000` en el Deployment.
    * Confirma que el `selector: app: fastapi` en el Service coincide con `labels: app: fastapi` en el `template.metadata` del Deployment. ¡Una falta de coincidencia aquí y el Service no sabrá a dónde enviar el tráfico!

¡Con estos pasos y tus YAMLs, deberías tener tu aplicación FastAPI funcionando en Minikube!
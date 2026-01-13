# 📋 PLAN DE DESARROLLO - Sprint 3 ML Microservices

## 🎯 Información del Proyecto

**Proyecto:** Sistema de Clasificación de Imágenes con Microservicios  
**Sprint:** 3  
**Tecnologías:** FastAPI, TensorFlow, Streamlit, Redis, PostgreSQL, Docker  
**Objetivo:** Implementar sistema completo de ML en producción con arquitectura de microservicios

---

## 📊 Estado del Proyecto

**Versiones de Librerías:**
- Mantenemos versiones actuales (2022) por estabilidad
- Solo actualizamos UI a versiones modernas (compatibilidad garantizada)

**Estimación Total:** 22-33 horas  
**Fecha Inicio:** 2026-01-13  

---

## 🗂️ ÉPICAS Y TAREAS DETALLADAS

### **ÉPICA 0: Setup Inicial del Ambiente** 🔧
**ID:** `EPIC-0`  
**Prioridad:** CRÍTICA  
**Estimación:** 30 minutos  
**Prerequisito:** Ninguno  
**Branch:** `feature/epic-0-setup`

#### Tareas:

**[EPIC-0-T1] Crear red Docker compartida**
- **ID Tarea:** `EPIC-0-T1`
- **Archivo(s):** N/A (comando Docker)
- **Descripción:** Crear la red `shared_network` para comunicación entre contenedores
- **Implementación:**
  ```bash
  docker network create shared_network
  docker network ls | grep shared_network
  ```
- **Validación:** La red aparece listada sin errores
- **Commit:** `[EPIC-0-T1] Crear red Docker shared_network`

---

**[EPIC-0-T2] Configurar variables de entorno**
- **ID Tarea:** `EPIC-0-T2`
- **Archivo(s):** `.env`, `api/.env`
- **Descripción:** Copiar archivos `.env.original` a `.env` en raíz y carpeta api
- **Implementación:**
  ```bash
  cp .env.original .env
  cd api && cp .env.original .env && cd ..
  ```
- **Variables requeridas:**
  - `POSTGRES_DB`: Nombre de base de datos
  - `POSTGRES_USER`: Usuario PostgreSQL
  - `POSTGRES_PASSWORD`: Password PostgreSQL
  - `DATABASE_HOST`: Host de base de datos (db)
  - `SECRET_KEY`: Clave secreta JWT
  - `REDIS_IP`: IP de Redis (redis)
- **Validación:** Archivos `.env` existen y tienen valores válidos
- **Commit:** `[EPIC-0-T2] Configurar variables de entorno para todos los servicios`

---

**[EPIC-0-T3] Actualizar requirements de UI**
- **ID Tarea:** `EPIC-0-T3`
- **Archivo(s):** `ui/requirements.txt`
- **Descripción:** Actualizar librerías de UI a versiones modernas (son compatibles)
- **Cambios:**
  ```python
  streamlit==1.40.0
  requests==2.32.3
  Pillow==11.0.0
  pytest==8.3.4
  ```
- **Validación:** Build de UI exitoso
- **Commit:** `[EPIC-0-T3] Actualizar dependencias de UI a versiones modernas`

---

### **ÉPICA 1: Infraestructura Docker** 🐳
**ID:** `EPIC-1`  
**Prioridad:** CRÍTICA  
**Estimación:** 45 minutos  
**Prerequisito:** ÉPICA 0 completada  
**Branch:** `feature/epic-1-infrastructure`

#### Tareas:

**[EPIC-1-T1] Implementar Dockerfile.populate**
- **ID Tarea:** `EPIC-1-T1`
- **Archivo(s):** `api/Dockerfile.populate`
- **Descripción:** Crear Dockerfile para poblar la base de datos inicial
- **Implementación:**
  ```dockerfile
  FROM python:3.8.13
  
  ENV PYTHONPATH=$PYTHONPATH:/src/
  
  COPY ./requirements.txt /src/requirements.txt
  WORKDIR /src
  RUN pip install --upgrade pip && pip install -r requirements.txt
  
  COPY ./ /src/
  
  CMD ["python", "populate_db.py"]
  ```
- **Validación:** Build exitoso sin errores, script se ejecuta correctamente
- **Commit:** `[EPIC-1-T1] Implementar Dockerfile.populate para inicialización de BD`

---

**[EPIC-1-T2] Validar configuración docker-compose**
- **ID Tarea:** `EPIC-1-T2`
- **Archivo(s):** `docker-compose.yml`, `api/docker-compose.yml`
- **Descripción:** Verificar configuración de servicios y dependencias
- **Verificaciones:**
  - ✅ Servicio `db` (PostgreSQL) → Puerto 5432
  - ✅ Servicio `redis` → Puerto 6379
  - ✅ Servicio `model` → Depende de redis
  - ✅ Servicio `api` → Depende de redis, model, db → Puerto 8000
  - ✅ Servicio `ui` → Depende de api → Puerto 9090
  - ✅ Volúmenes compartidos correctamente
  - ✅ Red `shared_network` en todos los servicios
- **Validación:** `docker-compose config` sin errores
- **Commit:** `[EPIC-1-T2] Validar y documentar configuración docker-compose`

---

### **ÉPICA 2: Servicio ML (Model)** 🤖
**ID:** `EPIC-2`  
**Prioridad:** ALTA  
**Estimación:** 3-4 horas  
**Prerequisito:** ÉPICA 1 completada  
**Branch:** `feature/epic-2-ml-service`

#### Tareas:

**[EPIC-2-T1] Conectar Redis en ml_service.py**
- **ID Tarea:** `EPIC-2-T1`
- **Archivo(s):** `model/ml_service.py` (líneas 12-15)
- **Descripción:** Inicializar conexión a Redis usando settings
- **Implementación:**
  ```python
  db = redis.Redis(
      host=settings.REDIS_IP,
      port=settings.REDIS_PORT,
      db=settings.REDIS_DB_ID
  )
  ```
- **Testing:** Verificar conexión con `db.ping()`
- **Validación:** Conexión establecida sin excepciones
- **Commit:** `[EPIC-2-T1] Conectar servicio ML a Redis`

---

**[EPIC-2-T2] Cargar modelo ResNet50**
- **ID Tarea:** `EPIC-2-T2`
- **Archivo(s):** `model/ml_service.py` (líneas 17-21)
- **Descripción:** Cargar modelo preentrenado de TensorFlow
- **Implementación:**
  ```python
  model = ResNet50(weights='imagenet')
  ```
- **Notas:** Primera ejecución descarga ~100MB, puede tomar 1-2 minutos
- **Validación:** Modelo cargado, sin errores de TensorFlow
- **Commit:** `[EPIC-2-T2] Cargar modelo ResNet50 preentrenado`

---

**[EPIC-2-T3] Implementar función predict()**
- **ID Tarea:** `EPIC-2-T3`
- **Archivo(s):** `model/ml_service.py` (líneas 24-53)
- **Descripción:** Cargar imagen, preprocesar y obtener predicción
- **Pasos de implementación:**
  1. Construir path: `img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)`
  2. Cargar imagen: `img = image.load_img(img_path, target_size=(224, 224))`
  3. Convertir a array: `x = image.img_to_array(img)`
  4. Expandir dimensiones: `x = np.expand_dims(x, axis=0)`
  5. Preprocesar: `x = preprocess_input(x)`
  6. Predecir: `preds = model.predict(x)`
  7. Decodificar: `decoded = decode_predictions(preds, top=1)[0][0]`
  8. Extraer: `_, class_name, pred_probability = decoded`
  9. Redondear: `pred_probability = round(float(pred_probability), 4)`
  10. Retornar: `return class_name, pred_probability`
- **Validación:** Retorna tupla (str, float) correctamente con dog.jpeg
- **Commit:** `[EPIC-2-T3] Implementar función predict() con ResNet50`

---

**[EPIC-2-T4] Implementar función classify_process()**
- **ID Tarea:** `EPIC-2-T4`
- **Archivo(s):** `model/ml_service.py` (líneas 56-97)
- **Descripción:** Loop infinito procesando jobs desde Redis
- **Pasos de implementación:**
  1. Obtener job: `queue_name, job_data = db.brpop(settings.REDIS_QUEUE)`
  2. Decodificar: `job = json.loads(job_data)`
  3. Extraer datos: `job_id = job["id"]`, `image_name = job["image_name"]`
  4. Predecir: `class_name, score = predict(image_name)`
  5. Crear output: `output = {"prediction": class_name, "score": score}`
  6. Serializar: `output_json = json.dumps(output)`
  7. Guardar: `db.set(job_id, output_json)`
  8. Sleep: `time.sleep(settings.SERVER_SLEEP)`
- **Manejo de errores:** Try-catch para imágenes inválidas o errores de modelo
- **Validación:** Procesa jobs continuamente, resultados en Redis correctos
- **Commit:** `[EPIC-2-T4] Implementar loop de procesamiento classify_process()`

---

**[EPIC-2-T5] Ejecutar tests del modelo**
- **ID Tarea:** `EPIC-2-T5`
- **Archivo(s):** `model/tests/test_model.py`
- **Descripción:** Validar que tests unitarios pasan
- **Comando:** `cd model && docker build -t model_test --progress=plain --target test .`
- **Validación:** Todos los tests pasan (100%)
- **Commit:** `[EPIC-2-T5] Validar tests unitarios del servicio ML`

---

### **ÉPICA 3: API FastAPI** 🚀
**ID:** `EPIC-3`  
**Prioridad:** ALTA  
**Estimación:** 4-5 horas  
**Prerequisito:** ÉPICA 2 completada  
**Branch:** `feature/epic-3-api`

#### Tareas:

**[EPIC-3-T1] Implementar allowed_file() en utils.py**
- **ID Tarea:** `EPIC-3-T1`
- **Archivo(s):** `api/app/utils.py` (líneas 5-25)
- **Descripción:** Validar extensiones de archivo permitidas
- **Implementación:**
  ```python
  ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
  
  def allowed_file(filename):
      """
      Checks if the format for the file received is acceptable.
      Accepts only image files: .png, .jpg, .jpeg, .gif
      
      Parameters
      ----------
      filename : str
          Filename from werkzeug.datastructures.FileStorage file.
      
      Returns
      -------
      bool
          True if the file is an image, False otherwise.
      """
      if not filename or '.' not in filename:
          return False
      
      file_ext = os.path.splitext(filename)[1].lower()
      return file_ext in ALLOWED_EXTENSIONS
  ```
- **Validación:** 
  - Retorna True para .png, .jpg, .jpeg, .gif (case insensitive)
  - Retorna False para .txt, .pdf, etc.
- **Commit:** `[EPIC-3-T1] Implementar validación de extensiones de archivo`

---

**[EPIC-3-T2] Implementar get_file_hash() en utils.py**
- **ID Tarea:** `EPIC-3-T2`
- **Archivo(s):** `api/app/utils.py` (líneas 28-53)
- **Descripción:** Generar hash MD5 del contenido del archivo
- **Implementación:**
  ```python
  async def get_file_hash(file):
      """
      Returns a new filename based on the file content using MD5 hashing.
      
      Parameters
      ----------
      file : werkzeug.datastructures.FileStorage
          File sent by user.
      
      Returns
      -------
      str
          New filename based in md5 file hash with original extension.
      """
      # Read file content and generate md5 hash
      file_content = await file.read()
      file_hash = hashlib.md5(file_content).hexdigest()
      
      # Return file pointer to the beginning
      await file.seek(0)
      
      # Add original file extension
      file_extension = os.path.splitext(file.filename)[1].lower()
      
      return f"{file_hash}{file_extension}"
  ```
- **Validación:** 
  - Retorna hash MD5 + extensión original
  - File pointer se resetea correctamente
  - Mismo archivo genera mismo hash
- **Commit:** `[EPIC-3-T2] Implementar generación de hash MD5 para archivos`

---

**[EPIC-3-T3] Configurar Redis en model/services.py**
- **ID Tarea:** `EPIC-3-T3`
- **Archivo(s):** `api/app/model/services.py` (línea 9)
- **Descripción:** Inicializar conexión Redis para API
- **Implementación:**
  ```python
  import redis
  from app import settings
  
  # Connect to Redis
  db = redis.Redis(
      host=settings.REDIS_IP,
      port=settings.REDIS_PORT,
      db=settings.REDIS_DB_ID,
      decode_responses=False
  )
  ```
- **Validación:** Conexión establecida sin errores
- **Commit:** `[EPIC-3-T3] Configurar conexión Redis en API`

---

**[EPIC-3-T4] Implementar model_predict() en model/services.py**
- **ID Tarea:** `EPIC-3-T4`
- **Archivo(s):** `api/app/model/services.py` (líneas 15-58)
- **Descripción:** Enviar job a Redis y esperar resultado
- **Pasos de implementación:**
  ```python
  import json
  import time
  import uuid
  
  async def model_predict(image_name):
      """
      Sends image to ML service via Redis and waits for prediction result.
      
      Parameters
      ----------
      image_name : str
          Filename of the image to predict.
      
      Returns
      -------
      prediction : str
          Predicted class name.
      score : float
          Confidence score of prediction.
      """
      # Generate unique job ID
      job_id = str(uuid.uuid4())
      
      # Create job dictionary
      job_data = {
          "id": job_id,
          "image_name": image_name
      }
      
      # Serialize to JSON
      job_json = json.dumps(job_data)
      
      # Push to Redis queue
      db.lpush(settings.REDIS_QUEUE, job_json)
      
      # Poll for result with timeout
      timeout = 60  # seconds
      start_time = time.time()
      
      while True:
          # Check if result is available
          result = db.get(job_id)
          
          if result:
              # Deserialize result
              result_data = json.loads(result)
              prediction = result_data["prediction"]
              score = result_data["score"]
              
              # Clean up
              db.delete(job_id)
              
              return prediction, score
          
          # Check timeout
          if time.time() - start_time > timeout:
              raise TimeoutError(f"Model prediction timeout for job {job_id}")
          
          # Wait before next check
          time.sleep(settings.API_SLEEP)
  ```
- **Validación:** Retorna tupla (prediction: str, score: float)
- **Commit:** `[EPIC-3-T4] Implementar comunicación API-Model vía Redis`

---

**[EPIC-3-T5] Implementar endpoint predict() en model/router.py**
- **ID Tarea:** `EPIC-3-T5`
- **Archivo(s):** `api/app/model/router.py` (líneas 16-33)
- **Descripción:** Endpoint completo para clasificación de imágenes
- **Pasos de implementación:**
  ```python
  @router.post("/predict")
  async def predict(file: UploadFile, current_user=Depends(get_current_user)):
      rpse = {"success": False, "prediction": None, "score": None, "image_file_name": None}
      
      try:
          # 1. Check if file was sent and is valid
          if not file or not file.filename:
              raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="No file provided"
              )
          
          # 2. Check if file is an image
          if not utils.allowed_file(file.filename):
              raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="File type not allowed. Only .png, .jpg, .jpeg, .gif"
              )
          
          # 3. Generate hash and save file
          hashed_filename = await utils.get_file_hash(file)
          file_path = os.path.join(config.UPLOAD_FOLDER, hashed_filename)
          
          # Only save if file doesn't exist (avoid duplicates)
          if not os.path.exists(file_path):
              with open(file_path, "wb") as f:
                  file_content = await file.read()
                  f.write(file_content)
          
          # 4. Send to model service
          prediction, score = await model_predict(hashed_filename)
          
          # 5. Build response
          rpse["success"] = True
          rpse["prediction"] = prediction
          rpse["score"] = float(score)
          rpse["image_file_name"] = hashed_filename
          
      except HTTPException:
          raise
      except Exception as e:
          raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Error processing image: {str(e)}"
          )
      
      return PredictResponse(**rpse)
  ```
- **Validación:** 
  - Retorna PredictResponse válido
  - Archivos duplicados no se reescriben
  - Errores retornan códigos HTTP apropiados
- **Commit:** `[EPIC-3-T5] Implementar endpoint POST /model/predict`

---

**[EPIC-3-T6] Implementar create_user_registration() en user/router.py**
- **ID Tarea:** `EPIC-3-T6`
- **Archivo(s):** `api/app/user/router.py` (líneas 13-26)
- **Descripción:** Endpoint para registro de nuevos usuarios
- **Implementación:**
  ```python
  @router.post("/", status_code=status.HTTP_201_CREATED)
  async def create_user_registration(
      request: schema.User, database: Session = Depends(db.get_db)
  ):
      # 1. Verify email doesn't exist
      user = await validator.verify_email_exist(request.email, database)
      
      # 2. If email exists, raise 400 error
      if user:
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail="Email already registered"
          )
      
      # 3. Create new user
      new_user = await services.new_user_register(request, database)
      
      # 4. Return new user object
      return new_user
  ```
- **Validación:** 
  - Registra usuario nuevo exitosamente
  - Retorna 400 si email ya existe
  - Password se hashea automáticamente
- **Commit:** `[EPIC-3-T6] Implementar endpoint POST /user/ para registro`

---

**[EPIC-3-T7] Ejecutar tests de API**
- **ID Tarea:** `EPIC-3-T7`
- **Archivo(s):** `api/tests/*.py`
- **Descripción:** Validar que todos los tests unitarios pasan
- **Comando:** `cd api && docker build -t fastapi_test --progress=plain --target test .`
- **Tests incluidos:**
  - `test_router_model.py`
  - `test_router_user.py`
  - `test_router_feedback.py`
  - `test_utils.py`
- **Validación:** Todos los tests pasan (100%)
- **Commit:** `[EPIC-3-T7] Validar tests unitarios de API`

---

### **ÉPICA 4: Interfaz de Usuario (UI)** 🎨
**ID:** `EPIC-4`  
**Prioridad:** MEDIA  
**Estimación:** 2-3 horas  
**Prerequisito:** ÉPICA 3 completada  
**Branch:** `feature/epic-4-ui`

#### Tareas:

**[EPIC-4-T1] Implementar función login()**
- **ID Tarea:** `EPIC-4-T1`
- **Archivo(s):** `ui/app/image_classifier_app.py` (líneas 9-34)
- **Descripción:** Autenticar usuario y obtener JWT token
- **Implementación:**
  ```python
  def login(username: str, password: str) -> Optional[str]:
      """
      Calls the login endpoint of the API to authenticate the user.
      
      Args:
          username (str): email of the user
          password (str): password of the user
      
      Returns:
          Optional[str]: token if login is successful, None otherwise
      """
      try:
          # 1. Construct API endpoint URL
          url = f"{API_BASE_URL}/login"
          
          # 2. Set up headers
          headers = {
              "accept": "application/json",
              "Content-Type": "application/x-www-form-urlencoded",
          }
          
          # 3. Prepare data payload
          data = {
              "grant_type": "",
              "username": username,
              "password": password,
              "scope": "",
              "client_id": "",
              "client_secret": "",
          }
          
          # 4. Send API request
          response = requests.post(url, headers=headers, data=data)
          
          # 5. Check response status
          if response.status_code == 200:
              # 6. Extract token from JSON
              return response.json()["access_token"]
          
      except Exception as e:
          st.error(f"Login error: {str(e)}")
      
      # 7. Return None if failed
      return None
  ```
- **Validación:** Retorna token válido con credenciales correctas
- **Commit:** `[EPIC-4-T1] Implementar función login() en UI`

---

**[EPIC-4-T2] Implementar función predict()**
- **ID Tarea:** `EPIC-4-T2`
- **Archivo(s):** `ui/app/image_classifier_app.py` (líneas 37-57)
- **Descripción:** Enviar imagen a API para clasificación
- **Implementación:**
  ```python
  def predict(token: str, uploaded_file: Image) -> requests.Response:
      """
      Calls the predict endpoint of the API to classify the uploaded image.
      
      Args:
          token (str): token to authenticate the user
          uploaded_file (Image): image to classify
      
      Returns:
          requests.Response: response from the API
      """
      # 1. Construct API endpoint URL
      url = f"{API_BASE_URL}/model/predict"
      
      # 2. Add token to headers
      headers = {"Authorization": f"Bearer {token}"}
      
      # 3. Create file dictionary with file data
      files = {
          "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
      }
      
      # 4. Make POST request
      response = requests.post(url, headers=headers, files=files)
      
      # 5. Return response
      return response
  ```
- **Validación:** Retorna response con status 200 y JSON válido
- **Commit:** `[EPIC-4-T2] Implementar función predict() en UI`

---

**[EPIC-4-T3] Implementar función send_feedback()**
- **ID Tarea:** `EPIC-4-T3`
- **Archivo(s):** `ui/app/image_classifier_app.py` (líneas 60-85)
- **Descripción:** Enviar feedback sobre predicción a API
- **Implementación:**
  ```python
  def send_feedback(
      token: str, feedback: str, score: float, prediction: str, image_file_name: str
  ) -> requests.Response:
      """
      Calls the feedback endpoint of the API to send feedback.
      
      Args:
          token (str): token to authenticate the user
          feedback (str): string with feedback
          score (float): confidence score of the prediction
          prediction (str): predicted class
          image_file_name (str): name of the image file
      
      Returns:
          requests.Response: response from the API
      """
      # 1. Construct API endpoint URL
      url = f"{API_BASE_URL}/feedback/"
      
      # 2. Add token to headers
      headers = {
          "Authorization": f"Bearer {token}",
          "Content-Type": "application/json"
      }
      
      # 3. Create feedback data dictionary
      data = {
          "feedback": feedback,
          "score": score,
          "predicted_class": prediction,
          "image_file_name": image_file_name
      }
      
      # 4. Make POST request
      response = requests.post(url, headers=headers, json=data)
      
      # 5. Return response
      return response
  ```
- **Validación:** Retorna 201 cuando feedback se guarda exitosamente
- **Commit:** `[EPIC-4-T3] Implementar función send_feedback() en UI`

---

**[EPIC-4-T4] Ejecutar tests de UI**
- **ID Tarea:** `EPIC-4-T4`
- **Archivo(s):** `ui/tests/test_image_classifier_app.py`
- **Descripción:** Validar tests unitarios de UI
- **Comando:** `cd ui && docker build -t ui_test --progress=plain --target test .`
- **Validación:** Tests pasan
- **Commit:** `[EPIC-4-T4] Validar tests unitarios de UI`

---

### **ÉPICA 5: Testing de Integración** ✅
**ID:** `EPIC-5`  
**Prioridad:** ALTA  
**Estimación:** 1-2 horas  
**Prerequisito:** ÉPICAS 2, 3, 4 completadas  
**Branch:** `feature/epic-5-integration`

#### Tareas:

**[EPIC-5-T1] Poblar base de datos**
- **ID Tarea:** `EPIC-5-T1`
- **Archivo(s):** `api/populate_db.py`
- **Descripción:** Ejecutar script de población de BD
- **Comandos:**
  ```bash
  cd api
  docker-compose up --build -d
  docker-compose logs app
  ```
- **Validación:** Usuario admin@example.com existe en BD
- **Commit:** `[EPIC-5-T1] Poblar base de datos con usuario admin`

---

**[EPIC-5-T2] Levantar sistema completo**
- **ID Tarea:** `EPIC-5-T2`
- **Archivo(s):** `docker-compose.yml`
- **Descripción:** Iniciar todos los servicios
- **Comandos:**
  ```bash
  docker-compose up --build -d
  docker-compose ps
  ```
- **Validación:** Todos los contenedores en estado `Up`
- **Commit:** `[EPIC-5-T2] Validar sistema completo funcional`

---

**[EPIC-5-T3] Ejecutar tests de integración E2E**
- **ID Tarea:** `EPIC-5-T3`
- **Archivo(s):** `tests/test_integration.py`
- **Descripción:** Ejecutar tests end-to-end
- **Comandos:**
  ```bash
  pip install -r tests/requirements.txt
  python tests/test_integration.py
  ```
- **Tests incluidos:**
  - Login exitoso
  - Clasificación de imagen
  - Endpoints de feedback
- **Validación:** 2 tests pasan (OK)
- **Commit:** `[EPIC-5-T3] Validar tests de integración E2E`

---

### **ÉPICA 6: Testing de Estrés con Locust** 📈
**ID:** `EPIC-6`  
**Prioridad:** MEDIA  
**Estimación:** 3-4 horas  
**Prerequisito:** ÉPICA 5 completada  
**Branch:** `feature/epic-6-stress-testing`

#### Tareas:

**[EPIC-6-T1] Verificar implementación de login en locustfile**
- **ID Tarea:** `EPIC-6-T1`
- **Archivo(s):** `stress_test/locustfile.py` (líneas 9-41)
- **Descripción:** Ya está implementado, verificar funcionalidad
- **Validación:** Función retorna token válido
- **Commit:** `[EPIC-6-T1] Verificar función login en Locust`

---

**[EPIC-6-T2] Implementar test para endpoint index**
- **ID Tarea:** `EPIC-6-T2`
- **Archivo(s):** `stress_test/locustfile.py`
- **Descripción:** Agregar task para endpoint raíz
- **Implementación:**
  ```python
  @task(2)
  def index(self):
      """Test index endpoint with higher frequency"""
      self.client.get("/")
  ```
- **Validación:** Task definido y ejecuta correctamente
- **Commit:** `[EPIC-6-T2] Agregar test de endpoint index en Locust`

---

**[EPIC-6-T3] Optimizar test de endpoint predict**
- **ID Tarea:** `EPIC-6-T3`
- **Archivo(s):** `stress_test/locustfile.py` (líneas 51-62)
- **Descripción:** Mejorar implementación existente
- **Mejoras:**
  - Usar `self.client` en lugar de URL hardcoded
  - Cachear token para evitar login repetido
  - Mejor manejo de errores
- **Implementación:**
  ```python
  def on_start(self):
      """Called once when user starts - login and cache token"""
      self.token = login("admin@example.com", "admin")
  
  @task(1)
  def predict(self):
      """Test predict endpoint"""
      if not self.token:
          return
      
      files = {"file": ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg")}
      headers = {"Authorization": f"Bearer {self.token}"}
      
      self.client.post("/model/predict", headers=headers, files=files)
  ```
- **Validación:** Test ejecuta sin errores repetidos de autenticación
- **Commit:** `[EPIC-6-T3] Optimizar test de predict en Locust`

---

**[EPIC-6-T4] Ejecutar escenarios de stress testing**
- **ID Tarea:** `EPIC-6-T4`
- **Archivo(s):** N/A (ejecución Locust)
- **Descripción:** Ejecutar 6 escenarios diferentes y recopilar métricas
- **Escenarios:**
  1. 10 usuarios, 1 modelo → 5 min
  2. 10 usuarios, 2 modelos → 5 min
  3. 25 usuarios, 1 modelo → 5 min
  4. 25 usuarios, 2 modelos → 5 min
  5. 50 usuarios, 2 modelos → 5 min
  6. 50 usuarios, 3 modelos → 5 min
- **Métricas a recopilar:**
  - RPS (requests por segundo)
  - Response time (median, p95, p99)
  - Failure rate
  - CPU/Memory usage
- **Validación:** Datos recopilados en CSV y screenshots
- **Commit:** `[EPIC-6-T4] Recopilar resultados de stress testing`

---

**[EPIC-6-T5] Crear reporte de stress testing**
- **ID Tarea:** `EPIC-6-T5`
- **Archivo(s):** `docs/STRESS_TEST_REPORT.md`
- **Descripción:** Documento con análisis de performance
- **Contenido requerido:**
  - Descripción del hardware servidor
  - Tabla comparativa de 6 escenarios
  - Gráficos de Locust (screenshots)
  - Análisis de resultados
  - Conclusiones sobre escalabilidad
  - Recomendaciones
- **Validación:** Reporte completo en español
- **Commit:** `[EPIC-6-T5] Crear reporte de stress testing`

---

### **ÉPICA 7: [OPCIONAL] Batch Processing** ⚡
**ID:** `EPIC-7`  
**Prioridad:** BAJA (Opcional)  
**Estimación:** 4-6 horas  
**Prerequisito:** ÉPICA 6 completada  
**Branch:** `feature/epic-7-batch-processing`

#### Tareas:

**[EPIC-7-T1] Diseñar arquitectura de batch processing**
- **ID Tarea:** `EPIC-7-T1`
- **Archivo(s):** `docs/BATCH_PROCESSING_DESIGN.md`
- **Descripción:** Documentar decisiones de diseño
- **Decisiones:**
  - Tamaño de batch: 8 imágenes (configurable)
  - Timeout: 1 segundo máximo para formar batch
  - Estrategia: Híbrida (tamaño O tiempo, lo que ocurra primero)
- **Validación:** Documento de diseño aprobado
- **Commit:** `[EPIC-7-T1] Documentar arquitectura de batch processing`

---

**[EPIC-7-T2] Agregar configuración de batch en settings**
- **ID Tarea:** `EPIC-7-T2`
- **Archivo(s):** `model/settings.py`
- **Descripción:** Agregar variables de configuración
- **Implementación:**
  ```python
  # Batch processing settings
  BATCH_SIZE = int(os.getenv("BATCH_SIZE", 8))
  BATCH_TIMEOUT = float(os.getenv("BATCH_TIMEOUT", 1.0))  # seconds
  ENABLE_BATCH = os.getenv("ENABLE_BATCH", "true").lower() == "true"
  ```
- **Validación:** Settings cargados correctamente
- **Commit:** `[EPIC-7-T2] Agregar configuración para batch processing`

---

**[EPIC-7-T3] Modificar predict() para soportar batch**
- **ID Tarea:** `EPIC-7-T3`
- **Archivo(s):** `model/ml_service.py`
- **Descripción:** Adaptar función para procesar múltiples imágenes
- **Implementación:**
  ```python
  def predict_batch(image_names):
      """
      Load multiple images and run batch prediction.
      
      Parameters
      ----------
      image_names : list[str]
          List of image filenames.
      
      Returns
      -------
      results : list[tuple(str, float)]
          List of (class_name, probability) for each image.
      """
      images = []
      
      # Load all images
      for image_name in image_names:
          img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
          img = image.load_img(img_path, target_size=(224, 224))
          x = image.img_to_array(img)
          images.append(x)
      
      # Stack into batch
      batch = np.vstack([np.expand_dims(img, axis=0) for img in images])
      batch = preprocess_input(batch)
      
      # Single prediction call for entire batch
      predictions = model.predict(batch)
      
      # Decode each prediction
      results = []
      for i, preds in enumerate(predictions):
          decoded = decode_predictions(np.expand_dims(preds, axis=0), top=1)[0][0]
          _, class_name, pred_probability = decoded
          results.append((class_name, round(float(pred_probability), 4)))
      
      return results
  ```
- **Validación:** Procesa batch correctamente, resultados idénticos a versión individual
- **Commit:** `[EPIC-7-T3] Implementar predict_batch() para múltiples imágenes`

---

**[EPIC-7-T4] Modificar classify_process() para acumular jobs**
- **ID Tarea:** `EPIC-7-T4`
- **Archivo(s):** `model/ml_service.py`
- **Descripción:** Implementar lógica de acumulación de jobs
- **Implementación:**
  ```python
  def classify_process():
      """
      Loop indefinitely processing jobs in batches.
      """
      jobs_batch = []
      last_process_time = time.time()
      
      while True:
          # Try to get a job with short timeout
          job_data = db.brpop(settings.REDIS_QUEUE, timeout=0.1)
          
          if job_data:
              queue_name, job_json = job_data
              job = json.loads(job_json)
              jobs_batch.append(job)
          
          # Check if we should process the batch
          current_time = time.time()
          should_process = (
              len(jobs_batch) >= settings.BATCH_SIZE or
              (jobs_batch and (current_time - last_process_time) >= settings.BATCH_TIMEOUT)
          )
          
          if should_process and jobs_batch:
              try:
                  # Extract image names and job IDs
                  image_names = [job["image_name"] for job in jobs_batch]
                  job_ids = [job["id"] for job in jobs_batch]
                  
                  # Process batch
                  results = predict_batch(image_names)
                  
                  # Store individual results
                  for job_id, (class_name, score) in zip(job_ids, results):
                      output = {"prediction": class_name, "score": score}
                      db.set(job_id, json.dumps(output))
                  
                  print(f"Processed batch of {len(jobs_batch)} images")
                  
              except Exception as e:
                  print(f"Error processing batch: {e}")
              
              finally:
                  # Reset batch
                  jobs_batch = []
                  last_process_time = time.time()
          
          # Small sleep to avoid busy waiting
          if not jobs_batch:
              time.sleep(settings.SERVER_SLEEP)
  ```
- **Validación:** Jobs se procesan en batches correctamente
- **Commit:** `[EPIC-7-T4] Implementar acumulación y procesamiento por lotes`

---

**[EPIC-7-T5] Comparar performance con/sin batching**
- **ID Tarea:** `EPIC-7-T5`
- **Archivo(s):** N/A (ejecución Locust)
- **Descripción:** Ejecutar mismos escenarios con batch activado
- **Escenarios:**
  - 50 usuarios, 2 modelos, sin batch (baseline)
  - 50 usuarios, 2 modelos, batch size 4
  - 50 usuarios, 2 modelos, batch size 8
  - 50 usuarios, 2 modelos, batch size 16
- **Métricas:** Throughput, latencia p50/p95/p99
- **Validación:** Datos comparativos recopilados
- **Commit:** `[EPIC-7-T5] Recopilar métricas de batch processing`

---

**[EPIC-7-T6] Actualizar reporte con resultados de batch**
- **ID Tarea:** `EPIC-7-T6`
- **Archivo(s):** `docs/STRESS_TEST_REPORT.md`
- **Descripción:** Agregar sección de batch processing
- **Contenido adicional:**
  - Explicación de batch processing
  - Comparativa de performance
  - Trade-offs (throughput vs latencia)
  - Recomendaciones de configuración
- **Validación:** Reporte actualizado y completo
- **Commit:** `[EPIC-7-T6] Documentar resultados de batch processing`

---

### **ÉPICA 8: Calidad y Documentación** 📝
**ID:** `EPIC-8`  
**Prioridad:** MEDIA  
**Estimación:** 2-3 horas  
**Prerequisito:** ÉPICA 5 completada  
**Branch:** `feature/epic-8-quality`

#### Tareas:

**[EPIC-8-T1] Formatear código con Black e isort**
- **ID Tarea:** `EPIC-8-T1`
- **Archivo(s):** Todos los archivos `.py`
- **Descripción:** Aplicar formateo automático
- **Comandos:**
  ```bash
  make format
  # o manualmente:
  black .
  isort . --recursive --profile black
  ```
- **Validación:** 
  - `black --check .` pasa sin cambios
  - `isort --check .` pasa sin cambios
- **Commit:** `[EPIC-8-T1] Formatear código con Black e isort`

---

**[EPIC-8-T2] Agregar docstrings faltantes**
- **ID Tarea:** `EPIC-8-T2`
- **Archivo(s):** Funciones implementadas sin docstrings
- **Descripción:** Documentar todas las funciones públicas
- **Estilo:** Google docstrings
- **Validación:** Todas las funciones públicas tienen docstrings
- **Commit:** `[EPIC-8-T2] Agregar docstrings a funciones implementadas`

---

**[EPIC-8-T3] Actualizar README principal**
- **ID Tarea:** `EPIC-8-T3`
- **Archivo(s):** `README.md`
- **Descripción:** Mejorar documentación principal
- **Secciones a agregar:**
  - Prerequisitos actualizados
  - Pasos de setup detallados paso a paso
  - Troubleshooting común
  - URLs de acceso
  - Credenciales por defecto
  - Comandos útiles
- **Validación:** README claro y completo
- **Commit:** `[EPIC-8-T3] Actualizar README con instrucciones completas`

---

**[EPIC-8-T4] Crear diagrama de flujo actualizado**
- **ID Tarea:** `EPIC-8-T4`
- **Archivo(s):** `docs/FLOW_DIAGRAM.png`
- **Descripción:** Diagrama de comunicación entre servicios
- **Contenido:**
  - Flujo de autenticación
  - Flujo de predicción (UI → API → Redis → Model → Redis → API → UI)
  - Flujo de feedback
- **Herramientas sugeridas:** draw.io, PlantUML, Mermaid
- **Validación:** Diagrama claro y exportado
- **Commit:** `[EPIC-8-T4] Crear diagrama de flujo de comunicación`

---

**[EPIC-8-T5] Crear .gitignore completo**
- **ID Tarea:** `EPIC-8-T5`
- **Archivo(s):** `.gitignore`
- **Descripción:** Asegurar archivos sensibles no se commiteen
- **Contenido:**
  ```gitignore
  # Environment variables
  .env
  .env.local
  .env.*.local
  
  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  *.so
  .Python
  env/
  venv/
  ENV/
  
  # Docker
  db_data/
  
  # Uploads
  uploads/
  *.jpeg
  *.jpg
  *.png
  *.gif
  
  # IDE
  .vscode/
  .idea/
  *.swp
  *.swo
  .DS_Store
  
  # Testing
  .pytest_cache/
  .coverage
  htmlcov/
  
  # Logs
  *.log
  
  # Locust
  *.csv
  locust_*.html
  ```
- **Validación:** Git no trackea archivos sensibles
- **Commit:** `[EPIC-8-T5] Agregar .gitignore completo`

---

## 📊 Resumen de Épicas

| Épica | Tareas | Prioridad | Estimación | Branch |
|-------|--------|-----------|------------|--------|
| ÉPICA 0: Setup Inicial | 3 | CRÍTICA | 30 min | `feature/epic-0-setup` |
| ÉPICA 1: Infraestructura | 2 | CRÍTICA | 45 min | `feature/epic-1-infrastructure` |
| ÉPICA 2: Servicio ML | 5 | ALTA | 3-4h | `feature/epic-2-ml-service` |
| ÉPICA 3: API FastAPI | 7 | ALTA | 4-5h | `feature/epic-3-api` |
| ÉPICA 4: UI Streamlit | 4 | MEDIA | 2-3h | `feature/epic-4-ui` |
| ÉPICA 5: Testing Integración | 3 | ALTA | 1-2h | `feature/epic-5-integration` |
| ÉPICA 6: Stress Testing | 5 | MEDIA | 3-4h | `feature/epic-6-stress-testing` |
| ÉPICA 7: Batch Processing | 6 | BAJA (Opcional) | 4-6h | `feature/epic-7-batch-processing` |
| ÉPICA 8: Calidad/Docs | 5 | MEDIA | 2-3h | `feature/epic-8-quality` |

**Total de Tareas:** 40  
**Tiempo Total:** 22-33 horas (con batch processing)

---

## 🎯 Flujo de Trabajo Git

### Convención de Commits:
```
[EPIC-X-TX] Descripción breve de la tarea

Descripción más detallada si es necesario.
- Cambios específicos
- Archivos modificados

Refs: EPIC-X-TX
```

### Ejemplo:
```
[EPIC-2-T3] Implementar función predict() con ResNet50

Implementa la lógica de predicción de imágenes:
- Carga y preprocesamiento de imágenes
- Inferencia con modelo ResNet50
- Decodificación de resultados
- Manejo de errores

Archivos modificados:
- model/ml_service.py (líneas 24-53)

Refs: EPIC-2-T3
```

### Workflow:
1. Crear branch para épica: `git checkout -b feature/epic-X-nombre`
2. Implementar tarea
3. Commit con formato: `git commit -m "[EPIC-X-TX] Descripción"`
4. Repetir para cada tarea
5. Merge a `develop` al completar épica
6. Merge a `main` al completar hito importante

---

## 📅 Cronograma Sugerido

### Semana 1:
- **Día 1 (4-5h):** ÉPICA 0, 1, 2
- **Día 2 (4-5h):** ÉPICA 3
- **Día 3 (3-4h):** ÉPICA 4, 5
- **Día 4 (3-4h):** ÉPICA 6

### Semana 2 (Opcional):
- **Día 5-6 (4-6h):** ÉPICA 7 (Batch Processing)
- **Día 7 (2-3h):** ÉPICA 8

---

## ✅ Criterios de Completitud

### Por Tarea:
- [ ] Código implementado según especificación
- [ ] Commit realizado con formato correcto
- [ ] Testing manual pasado (ver TESTING_PLAN.md)
- [ ] Sin errores en logs

### Por Épica:
- [ ] Todas las tareas completadas
- [ ] Tests unitarios pasando (si aplica)
- [ ] Testing manual de épica completo
- [ ] Branch mergeado a develop

### Proyecto Completo:
- [ ] Todas las épicas completadas
- [ ] Tests de integración E2E pasando
- [ ] Stress testing ejecutado y reportado
- [ ] Documentación actualizada
- [ ] Código formateado
- [ ] Sistema funcional end-to-end

---

## 📞 Soporte

Si encuentras problemas durante el desarrollo:

1. Revisar logs: `docker-compose logs -f [service]`
2. Verificar tests: Ejecutar tests de la épica correspondiente
3. Consultar TESTING_PLAN.md para debugging
4. Revisar AGENTS.md para convenciones de código

---

**Última actualización:** 2026-01-13  
**Versión:** 1.0

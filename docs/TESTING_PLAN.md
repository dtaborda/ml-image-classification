# 🧪 PLAN DE TESTING - Sprint 3 ML Microservices

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Testing por Épica](#testing-por-épica)
3. [Testing Automático](#testing-automático)
4. [Troubleshooting](#troubleshooting)
5. [Checklist Final](#checklist-final)

---

## Introducción

Este documento contiene la guía completa de testing manual y automático para cada épica del proyecto. Ejecuta estos tests después de completar cada épica antes de continuar con la siguiente.

### Herramientas Necesarias:
- ✅ Docker Desktop (corriendo)
- ✅ Navegador web (Chrome/Firefox recomendado)
- ✅ Terminal/Consola
- ✅ Python 3.8+ (para tests locales)
- ✅ Cliente HTTP: Postman/Insomnia o curl (opcional)
- ✅ Editor de texto

### 📝 Notas Importantes:

**Nombres de Contenedores (Docker Compose v2):**
Docker Compose v2 genera nombres con el formato: `<directorio>-<servicio>-<número>`

Ejemplos:
- `redis` → `assignment-redis-1`
- `ml_service` → `ml_service` (permanece igual)
- `db` → `assignment-db-1`

**Encontrar nombres dinámicamente:**
```bash
# Listar contenedores del proyecto
docker ps --filter "name=assignment"

# Encontrar contenedor específico
docker ps --filter "name=redis" --format "{{.Names}}"
```

**TTY Issues:**
Si ves el error "the input device is not a TTY", omite las flags `-it`:
```bash
# ❌ Puede fallar en algunos entornos
docker exec -it redis redis-cli ping

# ✅ Funciona siempre
docker exec assignment-redis-1 redis-cli ping
```

---

## Testing por Épica

### 🔧 ÉPICA 0: Setup Inicial del Ambiente

**Cuándo ejecutar:** Después de completar ÉPICA 0  
**Duración estimada:** 5 minutos  
**Prerequisitos:** Docker instalado y corriendo

#### Test Manual:

**Test 1: Verificar red Docker**
```bash
docker network ls | grep shared_network
```
✅ **Resultado esperado:** Línea con "shared_network" aparece
```
NETWORK ID     NAME              DRIVER    SCOPE
abc123def456   shared_network    bridge    local
```

**Test 2: Verificar archivos .env**
```bash
# En directorio raíz del proyecto
ls -la .env
ls -la api/.env
```
✅ **Resultado esperado:** Ambos archivos existen
```
-rw-r--r--  1 user  staff  142 Jan 13 10:00 .env
-rw-r--r--  1 user  staff  142 Jan 13 10:00 api/.env
```

**Test 3: Verificar contenido de .env**
```bash
cat .env
```
✅ **Resultado esperado:** Contiene variables requeridas:
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- DATABASE_HOST
- SECRET_KEY

**Test 4: Verificar actualización de ui/requirements.txt**
```bash
cat ui/requirements.txt
```
✅ **Resultado esperado:**
```
streamlit==1.40.0
requests==2.32.3
Pillow==11.0.0
pytest==8.3.4
```

#### Criterios de Éxito:
- [✅] Red shared_network creada
- [✅] Archivos .env en su lugar
- [✅] Variables de entorno configuradas
- [✅] Requirements de UI actualizados

---

### 🐳 ÉPICA 1: Infraestructura Docker

**Cuándo ejecutar:** Después de completar ÉPICA 1  
**Duración estimada:** 10 minutos  
**Prerequisitos:** ÉPICA 0 completada

#### Test Manual:

**Test 1: Validar Dockerfile.populate**
```bash
cd api
docker build -f Dockerfile.populate -t test_populate .
```
✅ **Resultado esperado:** Build exitoso sin errores
```
Successfully built abc123def456
Successfully tagged test_populate:latest
```

**Test 2: Verificar docker-compose config**
```bash
cd ..  # Volver a raíz
docker-compose config
```
✅ **Resultado esperado:** YAML válido sin errores, muestra configuración completa

**Test 3: Verificar servicios definidos**
```bash
docker-compose config --services
```
✅ **Resultado esperado:**
```
api
db
model
redis
ui
```

**Test 4: Validar puertos**
```bash
# Comando corregido: grep solo en la sección de ports (no volumes)
docker-compose config | grep -A 5 "ports:" | grep -E "(published|target)" | grep -v "volumes" | head -15
```
✅ **Resultado esperado:** (Formato Docker Compose v2)
```
        published: "8000"
        target: 5000
        published: "5432"
        target: 5432
        published: "9090"
        target: 9090
```

**Interpretación:**
- API: `8000` (host) → `5000` (container) = `8000:5000`
- DB: `5432` (host) → `5432` (container) = `5432:5432`
- UI: `9090` (host) → `9090` (container) = `9090:9090`

⚠️ **Nota:** Si ves `target: /src/uploads` o paths de archivos, esos son volúmenes, no puertos. Ignóralos.

**Nota sobre warnings:**
```
WARN: the attribute `version` is obsolete
```
⚠️ Este warning es normal en Docker Compose v2 y puede ignorarse.

**Test 5: Test build de todos los servicios**
```bash
docker-compose build
```
✅ **Resultado esperado:** Todos los servicios construyen exitosamente

⏱️ **Nota importante:** Puede tomar 5-10 minutos la primera vez:
- Descarga TensorFlow 2.13.0 (~500MB en Apple Silicon)
- Descarga base images de Python
- Instala todas las dependencias

⚠️ **Para Apple Silicon (M1/M2/M3):**
Si ves errores relacionados con TensorFlow 2.8.0 o Pillow 11.0.0:
- Esto ya fue corregido en commits recientes
- Ver `docs/COMPATIBILITY_NOTES.md` para detalles
- Las versiones actualizadas son compatibles (TF 2.13.0, Pillow 10.4.0)

#### Criterios de Éxito:
- [ ] Dockerfile.populate construye sin errores
- [ ] docker-compose.yml es válido
- [ ] Todos los servicios se construyen correctamente
- [ ] Puertos configurados correctamente

---

### 🤖 ÉPICA 2: Servicio ML (Model)

**Cuándo ejecutar:** Después de completar ÉPICA 2  
**Duración estimada:** 15 minutos  
**Prerequisitos:** ÉPICA 1 completada

#### Test Manual:

**Test 1: Levantar servicios necesarios**
```bash
docker-compose up -d redis model
docker-compose ps
```
✅ **Resultado esperado:** Ambos servicios en estado "Up"
```
NAME         STATUS    PORTS
redis        Up        6379/tcp
ml_service   Up
```

**Test 2: Verificar logs del modelo**
```bash
docker-compose logs model
```
✅ **Resultado esperado:**
- "Launching ML service..." aparece
- No hay errores de TensorFlow
- No hay errores de conexión Redis
- Puede aparecer mensaje de descarga de modelo (primera vez)

**Test 3: Verificar conexión Redis**
```bash
# Docker Compose v2 genera nombres como: <directorio>-<servicio>-<número>
# Método 1: Usar el nombre completo
docker exec assignment-redis-1 redis-cli ping

# Método 2: Encontrar el nombre dinámicamente
docker ps --filter "name=redis" --format "{{.Names}}" | xargs -I {} docker exec {} redis-cli ping
```
✅ **Resultado esperado:**
```
PONG
```

**Nota:** Si el comando con `-it` falla con "the input device is not a TTY", omite esas flags.

**Test 4: Test interactivo de predicción (Opcional)**
```bash
# Copiar imagen de prueba al volumen
cp api/tests/dog.jpeg uploads/

# Entrar al contenedor del modelo
docker exec -it ml_service python

# En el intérprete Python:
>>> from ml_service import predict
>>> result = predict("dog.jpeg")
>>> print(result)
>>> exit()
```
✅ **Resultado esperado:** Tupla con nombre de clase y probabilidad
```python
('golden_retriever', 0.8234)
```

**Test 5: Test de comunicación Redis**
```bash
# Opción A: Comandos directos (sin TTY)
docker exec assignment-redis-1 redis-cli LPUSH service_queue '{"id":"test123","image_name":"dog.jpeg"}'
sleep 3
docker exec assignment-redis-1 redis-cli GET test123

# Opción B: Modo interactivo (si tu terminal lo soporta)
docker exec -it assignment-redis-1 redis-cli
# Dentro de redis-cli:
127.0.0.1:6379> LPUSH service_queue '{"id":"test123","image_name":"dog.jpeg"}'
127.0.0.1:6379> GET test123
# Esperar 2-3 segundos
127.0.0.1:6379> GET test123
127.0.0.1:6379> exit
```
✅ **Resultado esperado:** Segunda vez retorna JSON con prediction y score
```json
{"prediction":"golden_retriever","score":0.8234}
```

**Test 6: Verificar modelo descargó correctamente**
```bash
docker-compose logs model | grep -i "model"
```
✅ **Resultado esperado:** Sin errores de carga de modelo

#### Test Automático:

**Test de unidad del modelo**
```bash
cd model
docker build -t model_test --progress=plain --target test .
```

**⚠️ Si falla con "TLS handshake timeout" (problema de red con Docker Hub):**
```bash
# Workaround: Ejecutar tests en el contenedor corriendo
docker exec ml_service pytest -v /src/tests
```

✅ **Resultado esperado:**
```
============================= test session starts ==============================
tests/test_model.py::test_predict PASSED                                [100%]

============================== 1 passed in 4.86s ===============================
```

**Nota:** El tiempo puede variar (4-18 segundos) dependiendo de si es la primera predicción.

#### Criterios de Éxito:
- [ ] Contenedores corriendo estables
- [ ] Modelo ResNet50 cargado exitosamente
- [ ] Predicciones funcionan correctamente
- [ ] Redis recibe y procesa jobs
- [ ] Tests unitarios pasan

---

### 🚀 ÉPICA 3: API FastAPI

**Cuándo ejecutar:** Después de completar ÉPICA 3  
**Duración estimada:** 20 minutos  
**Prerequisitos:** ÉPICA 2 completada

#### Test Manual:

**Test 1: Poblar base de datos**
```bash
cd api
docker-compose up --build -d
docker-compose logs app
```
✅ **Resultado esperado:**
- Container ejecuta sin errores
- Logs muestran creación de usuario admin

**Test 2: Levantar sistema completo**
```bash
cd ..  # Volver a raíz
docker-compose up -d
docker-compose ps
```
✅ **Resultado esperado:** Todos los servicios "Up"
```
NAME         STATUS    PORTS
ml_api       Up        0.0.0.0:8000->5000/tcp
ml_service   Up
ml_ui        Up        0.0.0.0:9090->9090/tcp
postgres_db  Up        0.0.0.0:5432->5432/tcp
redis        Up        6379/tcp
```

**Test 3: Verificar API responde**
```bash
curl http://localhost:8000/docs
```
✅ **Resultado esperado:** HTML de Swagger UI retornado

**Test 4: Testing en Swagger UI**

1. **Abrir navegador:**
   - URL: http://localhost:8000/docs
   - ✅ Interfaz de FastAPI carga correctamente

2. **Login:**
   - Endpoint: `POST /login`
   - Click "Try it out"
   - Llenar:
     - username: `admin@example.com`
     - password: `admin`
   - Click "Execute"
   - ✅ Response 200 con JSON:
     ```json
     {
       "access_token": "eyJ...",
       "token_type": "bearer"
     }
     ```
   - **COPIAR el access_token**

3. **Autorizar:**
   - Click botón "Authorize" (🔓) arriba a la derecha
   - Pegar: `Bearer <tu_token_aqui>`
   - Click "Authorize"
   - ✅ Botón cambia a "Authorized" (🔒)

4. **Crear usuario nuevo:**
   - Endpoint: `POST /user/`
   - Try it out
   - Request body:
     ```json
     {
       "name": "Test User",
       "email": "test@test.com",
       "password": "test123"
     }
     ```
   - Execute
   - ✅ Response 201 con usuario creado
   - ✅ Password NO aparece en respuesta (seguridad)

5. **Intentar crear usuario duplicado:**
   - Mismo endpoint, mismo email
   - ✅ Response 400: "Email already registered"

6. **Test de predicción:**
   - Endpoint: `POST /model/predict`
   - Try it out
   - Click "Choose File" → Seleccionar `api/tests/dog.jpeg`
   - Execute
   - ⏱️ Esperar 3-5 segundos
   - ✅ Response 200:
     ```json
     {
       "success": true,
       "prediction": "golden_retriever",
       "score": 0.8234,
       "image_file_name": "a1b2c3d4e5f6.jpeg"
     }
     ```

7. **Verificar archivo guardado:**
   ```bash
   ls -la uploads/
   ```
   - ✅ Archivo con hash MD5 existe

8. **Test de predicción duplicada:**
   - Mismo archivo, mismo endpoint
   - ✅ Retorna mismo hash (no duplica archivo)

9. **Test con archivo inválido:**
   - Subir archivo .txt
   - ✅ Response 400: "File type not allowed"

10. **Enviar feedback:**
    - Endpoint: `POST /feedback/`
    - Try it out
    - Request body:
      ```json
      {
        "score": 0.8234,
        "predicted_class": "golden_retriever",
        "image_file_name": "a1b2c3d4e5f6.jpeg",
        "feedback": "La predicción fue incorrecta, es un labrador"
      }
      ```
    - Execute
    - ✅ Response 201

11. **Ver feedback enviado:**
    - Endpoint: `GET /feedback/`
    - Execute
    - ✅ Response 200 con array conteniendo el feedback

**Test 5: Test con curl (alternativo)**
```bash
# Login
TOKEN=$(curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin" | jq -r '.access_token')

# Predicción
curl -X POST "http://localhost:8000/model/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@api/tests/dog.jpeg"
```
✅ **Resultado esperado:** JSON con predicción

#### Test Automático:

**Tests unitarios de API**
```bash
cd api
docker build -t fastapi_test --progress=plain --target test .
```
✅ **Resultado esperado:**
```
============================= test session starts ==============================
tests/test_utils.py::test_allowed_file PASSED                           [ 25%]
tests/test_router_user.py::test_create_user_registration_success PASSED [ 50%]
tests/test_router_user.py::test_create_user_registration_fails PASSED   [ 75%]
tests/test_router_model.py::test_predict PASSED                         [100%]

============================== 4 passed in 2.45s ===============================
```

#### Criterios de Éxito:
- [ ] API responde en puerto 8000
- [ ] Swagger UI carga correctamente
- [ ] Login funciona y retorna token
- [ ] Autorización JWT funciona
- [ ] CRUD de usuarios funciona
- [ ] Predicción retorna resultados correctos
- [ ] Archivos se guardan con hash MD5
- [ ] Validación de tipos de archivo funciona
- [ ] Feedback se guarda en BD
- [ ] Tests unitarios pasan

---

### 🎨 ÉPICA 4: UI Streamlit

**Cuándo ejecutar:** Después de completar ÉPICA 4  
**Duración estimada:** 15 minutos  
**Prerequisitos:** ÉPICA 3 completada, sistema completo corriendo

#### Test Manual:

**Test 1: Verificar UI carga**
1. Abrir navegador
2. Ir a: http://localhost:9090
3. ✅ Página "Image Classifier" carga
4. ✅ Formulario de login visible

**Test 2: Login en UI**
1. Username: `admin@example.com`
2. Password: `admin`
3. Click "Login"
4. ✅ Mensaje: "Login successful!"
5. ✅ Aparece uploader de imagen
6. ✅ Formulario de login desaparece

**Test 3: Login con credenciales incorrectas**
1. Refrescar página (F5)
2. Username: `wrong@email.com`
3. Password: `wrongpass`
4. Click "Login"
5. ✅ Mensaje: "Login failed. Please check your credentials."
6. ✅ NO aparece uploader

**Test 4: Upload de imagen**
1. Login exitoso
2. Click "Browse files"
3. Seleccionar imagen (dog.jpeg o cualquier .jpg/.png)
4. ✅ Imagen se muestra en pantalla
5. ✅ Preview con tamaño 300px de ancho

**Test 5: Clasificación de imagen**
1. Después de subir imagen
2. Click botón "Classify"
3. ⏱️ Esperar 3-5 segundos
4. ✅ Aparece:
   - **Prediction:** nombre_clase (ej: "golden_retriever")
   - **Score:** número decimal (ej: 0.8234)
5. ✅ Aparece sección "Feedback"

**Test 6: Clasificar sin subir imagen**
1. Login exitoso
2. Click "Classify" SIN subir imagen
3. ✅ Warning: "Please upload an image before classifying."

**Test 7: Envío de feedback**
1. Después de clasificar exitosamente
2. En textarea de feedback escribir: "La predicción es incorrecta"
3. Click "Send Feedback"
4. ✅ Mensaje: "Thanks for your feedback!"

**Test 8: Feedback sin texto**
1. Después de clasificar
2. Dejar textarea vacío
3. Click "Send Feedback"
4. ✅ Warning: "Please provide feedback before sending."

**Test 9: Verificar feedback en API**
1. Ir a http://localhost:8000/docs
2. Login y autorizar
3. GET /feedback/
4. ✅ Feedback enviado desde UI aparece en la lista

**Test 10: Test con diferentes formatos**
1. Subir imagen .jpg → ✅ Funciona
2. Subir imagen .png → ✅ Funciona
3. Subir imagen .gif → ✅ Funciona
4. Intentar subir .txt → ✅ Streamlit rechaza (por configuración)

**Test 11: Persistencia de sesión**
1. Clasificar imagen exitosamente
2. Refrescar página (F5)
3. ✅ Vuelve a pedir login (sesión no persiste por diseño)

**Test 12: Múltiples clasificaciones**
1. Login
2. Subir imagen 1, clasificar
3. Subir imagen 2 diferente, clasificar
4. ✅ Ambas clasificaciones funcionan
5. ✅ Resultados actualizados correctamente

#### Test Automático:

**Tests unitarios de UI**
```bash
cd ui
docker build -t ui_test --progress=plain --target test .
```
✅ **Resultado esperado:** Tests pasan

#### Criterios de Éxito:
- [ ] UI carga en puerto 9090
- [ ] Login funciona con credenciales correctas
- [ ] Login falla con credenciales incorrectas
- [ ] Upload de imágenes funciona
- [ ] Preview de imagen se muestra
- [ ] Clasificación retorna resultados
- [ ] Feedback se envía correctamente
- [ ] Validaciones de campos funcionan
- [ ] UI es responsive y usable

---

### ✅ ÉPICA 5: Testing de Integración

**Cuándo ejecutar:** Después de completar ÉPICA 5  
**Duración estimada:** 10 minutos  
**Prerequisitos:** ÉPICAS 2, 3, 4 completadas

#### Test Automático E2E:

**Setup:**
```bash
# Instalar dependencias
pip install -r tests/requirements.txt
```

**Ejecución:**
```bash
# Asegurar que sistema está corriendo
docker-compose ps

# Ejecutar tests
python tests/test_integration.py
```

✅ **Resultado esperado:**
```
..
----------------------------------------------------------------------
Ran 2 tests in 5.299s

OK
```

**Si hay fallos, verificar:**
```bash
# ¿API está corriendo?
curl http://localhost:8000/

# ¿Usuario admin existe?
docker-compose exec api python -c "from app.db import get_db; from app.user.models import User; db = next(get_db()); print(db.query(User).filter(User.email=='admin@example.com').first())"

# Ver logs
docker-compose logs api
docker-compose logs model
```

#### Test Manual Complementario:

**Test de flujo completo con curl:**
```bash
# 1. Login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin"

# 2. Copiar token y usar en predicción
TOKEN="<pegar_token_aqui>"

curl -X POST "http://localhost:8000/model/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@tests/dog.jpeg"

# 3. Enviar feedback
curl -X POST "http://localhost:8000/feedback/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback": "Test feedback",
    "score": 0.85,
    "predicted_class": "golden_retriever",
    "image_file_name": "test.jpeg"
  }'
```

✅ **Resultado esperado:** Todos los requests retornan códigos 200/201

#### Criterios de Éxito:
- [ ] Tests automáticos E2E pasan (2/2)
- [ ] Flujo completo funciona via curl
- [ ] Todos los servicios comunicándose correctamente
- [ ] No hay errores en logs

---

### 📈 ÉPICA 6: Testing de Estrés con Locust

**Cuándo ejecutar:** Después de completar ÉPICA 6  
**Duración estimada:** 60 minutos (6 escenarios)  
**Prerequisitos:** ÉPICA 5 completada, sistema corriendo

#### Setup:

**Instalación:**
```bash
pip install locust
locust --version
```

**Preparación:**
```bash
cd stress_test
ls dog.jpeg  # Verificar imagen existe
```

#### Test Manual:

**Test 1: Lanzar Locust**
```bash
locust -f locustfile.py --host=http://localhost:8000
```
✅ **Resultado esperado:**
```
[2026-01-13 10:00:00,000] INFO/locust.main: Starting web interface at http://0.0.0.0:8089
```

**Test 2: Configurar prueba inicial**
1. Abrir navegador: http://localhost:8089
2. Configurar:
   - Number of users: **10**
   - Ramp up: **1** user/second
   - Host: `http://localhost:8000`
3. Click "Start swarming"
4. ✅ Simulación inicia sin errores

**Test 3: Monitorear métricas**
En interfaz de Locust observar:
- **Statistics tab:**
  - Requests/s (RPS)
  - Response times (50%, 95%, 99%)
  - Failures (debe ser 0%)
- **Charts tab:**
  - Gráfico de RPS en tiempo real
  - Gráfico de response times
- **Failures tab:**
  - ✅ Debe estar vacío

**Test 4: Escenario 1 - Baseline (10 usuarios, 1 modelo)**
```bash
# Ya corriendo desde Test 2
# Dejar correr 5 minutos
```
📊 **Métricas esperadas:**
- RPS: 2-5 req/s
- Response time median: 1000-2000ms
- Response time 95%: 2000-3000ms
- Failure rate: 0%

**Exportar datos:**
1. Click "Download Data" tab
2. Descargar:
   - statistics.csv
   - statistics_history.csv
3. Screenshots de gráficos

**Test 5: Escenario 2 - Escalado (10 usuarios, 2 modelos)**
```bash
# En otra terminal
docker-compose up --scale model=2 -d

# Verificar
docker-compose ps | grep model
# Debe mostrar 2 instancias
```

En Locust UI:
1. Click "Stop"
2. Click "New test"
3. Misma configuración (10 usuarios, 1/s)
4. Correr 5 minutos

📊 **Métricas esperadas:**
- RPS: 4-8 req/s (mejora ~2x)
- Response time median: 800-1500ms (mejora)
- Failure rate: 0%

**Test 6: Escenario 3-6 - Carga progresiva**

| Escenario | Usuarios | Modelos | Duración |
|-----------|----------|---------|----------|
| 3 | 25 | 1 | 5 min |
| 4 | 25 | 2 | 5 min |
| 5 | 50 | 2 | 5 min |
| 6 | 50 | 3 | 5 min |

Para cada escenario:
1. Escalar modelos: `docker-compose up --scale model=N -d`
2. Stop + New test en Locust
3. Configurar usuarios
4. Correr 5 minutos
5. Exportar datos y screenshots

**Test 7: Monitoreo de recursos**
```bash
# En otra terminal durante tests
docker stats

# Observar:
# - CPU% de cada contenedor
# - Memory usage
```

📊 **Anotar métricas de recursos:**
- CPU usage de model container(s)
- CPU usage de api container
- Memory usage

**Test 8: Test de estabilidad (opcional)**
```bash
# Escenario largo: 50 usuarios, 3 modelos, 30 minutos
```
✅ **Objetivo:** Verificar que no hay memory leaks o degradación

#### Formato de Reporte:

Crear archivo `docs/STRESS_TEST_REPORT.md` con:

```markdown
# Reporte de Stress Testing

## Hardware Utilizado
- CPU: [especificar]
- RAM: [especificar]
- OS: [especificar]
- Docker: [versión]

## Resultados

### Tabla Comparativa

| Escenario | Usuarios | Modelos | RPS | RT p50 (ms) | RT p95 (ms) | Failures |
|-----------|----------|---------|-----|-------------|-------------|----------|
| 1 | 10 | 1 | X | X | X | X% |
| 2 | 10 | 2 | X | X | X | X% |
| ... | ... | ... | ... | ... | ... | ... |

### Gráficos
[Screenshots de Locust]

## Análisis
[Interpretación de resultados]

## Conclusiones
[Recomendaciones]
```

#### Criterios de Éxito:
- [ ] Locust ejecuta sin crashes
- [ ] 6 escenarios completados
- [ ] Datos exportados para cada escenario
- [ ] Screenshots capturados
- [ ] Se observa mejora con más instancias
- [ ] Failure rate < 5%
- [ ] Reporte creado

---

### ⚡ ÉPICA 7: Batch Processing (Opcional)

**Cuándo ejecutar:** Después de completar ÉPICA 7  
**Duración estimada:** 30 minutos  
**Prerequisitos:** ÉPICA 6 completada, batch implementado

#### Test Manual:

**Test 1: Verificar configuración batch**
```bash
cat model/settings.py | grep -A 3 "BATCH"
```
✅ **Resultado esperado:**
```python
BATCH_SIZE = 8
BATCH_TIMEOUT = 1.0
ENABLE_BATCH = true
```

**Test 2: Activar batch processing**
```bash
# Si usa variables de entorno
export ENABLE_BATCH=true
export BATCH_SIZE=8

# Reiniciar servicio
docker-compose restart model
```

**Test 3: Verificar logs de batch**
```bash
docker-compose logs -f model | grep -i batch
```
✅ **Resultado esperado:**
```
Processing batch of 4 images in 0.8s
Processing batch of 8 images in 1.2s
```

**Test 4: Test funcional - predicciones siguen correctas**
1. Ir a UI: http://localhost:9090
2. Login
3. Clasificar varias imágenes
4. ✅ Resultados siguen siendo correctos
5. ✅ No hay diferencia en calidad de predicciones

**Test 5: Comparativa con Locust**

**Sin batch:**
```bash
# Desactivar batch
export ENABLE_BATCH=false
docker-compose restart model

# Locust: 50 usuarios, 2 modelos, 5 min
locust -f locustfile.py --host=http://localhost:8000
```
📊 Anotar métricas baseline

**Con batch (tamaño 4):**
```bash
export ENABLE_BATCH=true
export BATCH_SIZE=4
docker-compose restart model

# Locust: mismo escenario
```
📊 Anotar métricas

**Con batch (tamaño 8):**
```bash
export BATCH_SIZE=8
docker-compose restart model
```
📊 Anotar métricas

**Con batch (tamaño 16):**
```bash
export BATCH_SIZE=16
docker-compose restart model
```
📊 Anotar métricas

**Test 6: Análisis de trade-offs**

Comparar:
- **Throughput:** Imágenes procesadas/segundo
- **Latencia p50:** Tiempo de respuesta mediano
- **Latencia p95/p99:** Peor caso

📊 **Esperado:**
- Throughput: ⬆️ +30-50% con batch
- Latencia p50: ➡️ Similar
- Latencia p95/p99: ⬆️ Aumenta ligeramente (trade-off)

#### Actualizar Reporte:

Agregar a `docs/STRESS_TEST_REPORT.md`:

```markdown
## Batch Processing

### Configuración
- Tamaño de batch: 8
- Timeout: 1.0s
- Estrategia: Híbrida

### Resultados Comparativos

| Configuración | Throughput (img/s) | Latencia p50 (ms) | Latencia p95 (ms) |
|---------------|-------------------|-------------------|-------------------|
| Sin batch | X | X | X |
| Batch size 4 | X | X | X |
| Batch size 8 | X | X | X |
| Batch size 16 | X | X | X |

### Análisis
[Explicar trade-offs]

### Recomendaciones
Configuración óptima: batch size = X porque...
```

#### Criterios de Éxito:
- [ ] Batch processing funciona correctamente
- [ ] Logs muestran procesamiento por lotes
- [ ] Calidad de predicciones se mantiene
- [ ] Throughput mejora significativamente
- [ ] Trade-offs documentados
- [ ] Reporte actualizado

---

### 📝 ÉPICA 8: Calidad y Documentación

**Cuándo ejecutar:** Después de completar ÉPICA 8  
**Duración estimada:** 10 minutos  
**Prerequisitos:** ÉPICA 5 completada

#### Test Manual:

**Test 1: Verificar formateo de código**
```bash
# Ejecutar formateo
make format

# Verificar que no hay cambios pendientes
black --check .
isort --check . --profile black
```
✅ **Resultado esperado:**
```
All done! ✨ 🍰 ✨
XX files would be left unchanged.
```

**Test 2: Validar docstrings**
```bash
# Verificar funciones implementadas tienen docstrings
grep -r "def " api/app/utils.py
grep -A 5 "def allowed_file" api/app/utils.py
```
✅ **Resultado esperado:** Cada función tiene docstring estilo Google

**Test 3: Verificar README actualizado**
```bash
cat README.md
```
✅ **Debe contener:**
- [ ] Sección de prerequisitos
- [ ] Pasos de setup claros
- [ ] URLs de acceso
- [ ] Credenciales por defecto
- [ ] Sección de troubleshooting

**Test 4: Verificar .gitignore**
```bash
cat .gitignore
```
✅ **Debe incluir:**
- .env
- __pycache__/
- uploads/
- db_data/
- *.pyc
- .pytest_cache/

**Test 5: Verificar que archivos sensibles no están trackeados**
```bash
git status
```
✅ **NO debe aparecer:**
- .env
- Archivos en uploads/
- __pycache__/
- db_data/

#### Criterios de Éxito:
- [ ] Código formateado con Black
- [ ] Imports ordenados con isort
- [ ] Docstrings presentes
- [ ] README completo y claro
- [ ] .gitignore protege archivos sensibles
- [ ] Diagrama de flujo creado (si aplica)

---

## Testing Automático

### Resumen de Comandos de Tests

**Tests Unitarios por Servicio:**
```bash
# API
cd api && docker build -t fastapi_test --target test .

# Model
cd model && docker build -t model_test --target test .

# UI
cd ui && docker build -t ui_test --target test .
```

**Tests de Integración:**
```bash
pip install -r tests/requirements.txt
python tests/test_integration.py
```

**Todos los tests en secuencia:**
```bash
# Script automatizado
./run_all_tests.sh  # (crear este script)
```

### Script run_all_tests.sh

```bash
#!/bin/bash

echo "🧪 Ejecutando todos los tests..."

echo "\n📦 Tests API..."
cd api && docker build -t fastapi_test --target test . || exit 1

echo "\n🤖 Tests Model..."
cd ../model && docker build -t model_test --target test . || exit 1

echo "\n🎨 Tests UI..."
cd ../ui && docker build -t ui_test --target test . || exit 1

echo "\n✅ Tests Integración..."
cd .. && python tests/test_integration.py || exit 1

echo "\n✨ ¡Todos los tests pasaron!"
```

---

## Troubleshooting

### Problema: TLS handshake timeout con Docker Hub
```bash
ERROR: failed to do request: Head "https://registry-1.docker.io/...": net/http: TLS handshake timeout
```
**Causa:** Problema de red temporal o timeout al conectarse a Docker Hub.

**Solución 1: Reintentar más tarde**
```bash
# Esperar unos minutos y reintentar
docker build -t model_test --target test .
```

**Solución 2: Usar contenedor corriendo (Recomendado)**
```bash
# Si ya construiste la imagen con docker-compose build
docker exec ml_service pytest -v /src/tests
```

**Solución 3: Aumentar timeout de Docker**
```bash
# Editar Docker Desktop → Preferences → Docker Engine
# Agregar en el JSON:
{
  "max-download-attempts": 5,
  "max-concurrent-downloads": 1
}
# Luego restart Docker Desktop
```

**Solución 4: Usar proxy/VPN si el problema persiste**

### Problema: Contenedor no existe (Docker Compose v2)
```bash
Error: No such container: redis
Error: No such container: model
```
**Causa:** Docker Compose v2 genera nombres como `<directorio>-<servicio>-<número>`

**Solución:**
```bash
# Encontrar el nombre real
docker ps --filter "name=redis" --format "{{.Names}}"

# Usar el nombre completo
docker exec assignment-redis-1 redis-cli ping

# O encontrar dinámicamente
docker ps --filter "name=redis" --format "{{.Names}}" | xargs -I {} docker exec {} redis-cli ping
```

### Problema: Error TTY "the input device is not a TTY"
```bash
Error: the input device is not a TTY
```
**Causa:** Algunos entornos no soportan modo interactivo (-it).

**Solución:**
```bash
# Quitar flags -it
docker exec assignment-redis-1 redis-cli ping
# En lugar de:
docker exec -it assignment-redis-1 redis-cli ping
```

### Problema: Red Docker no existe
```bash
Error: network shared_network not found
```
**Solución:**
```bash
docker network create shared_network
```

### Problema: Puerto ya en uso
```bash
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```
**Solución:**
```bash
# Encontrar proceso usando el puerto
lsof -i :8000

# Matar proceso o cambiar puerto en docker-compose.yml
```

### Problema: TensorFlow 2.8.0 no compatible con Apple Silicon
```bash
ERROR: Could not find a version that satisfies the requirement tensorflow==2.8.0
```
**Causa:** TensorFlow 2.8.0 no tiene binarios para arquitectura ARM64 (M1/M2/M3)

**Solución:**
```bash
# Ya corregido en model/requirements.txt
# Actualizado a tensorflow==2.13.0 que soporta Apple Silicon
# Si ves este error, hacer git pull para obtener la versión actualizada
git pull origin main
docker-compose build model --no-cache
```
Ver `docs/COMPATIBILITY_NOTES.md` para más detalles.

### Problema: Pillow 11.0.0 no compatible con Python 3.8
```bash
ERROR: Could not find a version that satisfies the requirement Pillow==11.0.0
```
**Causa:** Pillow 11.0+ requiere Python 3.9+, proyecto usa Python 3.8.13

**Solución:**
```bash
# Ya corregido en model/requirements.txt y ui/requirements.txt
# Actualizado a Pillow==10.4.0 (última versión compatible con Python 3.8)
git pull origin main
docker-compose build --no-cache
```

### Problema: Modelo no descarga
```bash
Error downloading ResNet50 weights
```
**Solución:**
```bash
# Verificar conexión internet
# Reintentar build
docker-compose build model --no-cache

# Si persiste, verificar que TensorFlow instaló correctamente
docker run --rm ml_service python -c "import tensorflow as tf; print(tf.__version__)"
```

### Problema: Redis connection refused
```bash
redis.exceptions.ConnectionError: Connection refused
```
**Solución:**
```bash
# Verificar Redis corriendo
docker-compose ps redis

# Verificar configuración de red
docker-compose config | grep networks
```

### Problema: Tests fallan con import errors
```bash
ModuleNotFoundError: No module named 'fastapi'
```
**Solución:**
```bash
# Asegurar que tests corren en Docker
cd api && docker build -t fastapi_test --target test .

# NO ejecutar pytest directamente fuera de Docker
```

### Problema: UI no carga
```bash
This site can't be reached
```
**Solución:**
```bash
# Verificar contenedor corriendo
docker-compose ps ui

# Ver logs
docker-compose logs ui

# Verificar puerto correcto
curl http://localhost:9090
```

### Problema: Predicciones muy lentas
```bash
Request timeout después de 60 segundos
```
**Solución:**
```bash
# Ver logs del modelo
docker-compose logs model

# Verificar CPU/Memory
docker stats

# En Apple Silicon, TensorFlow 2.13 es optimizado pero puede ser lento
# la primera predicción (carga del modelo)

# Considerar:
# 1. Aumentar timeout en api/app/model/services.py
# 2. Implementar ÉPICA 7 (batch processing) para mejor throughput
# 3. Escalar servicio: docker-compose up --scale model=2
```

### Problema: Warning sobre version en docker-compose
```bash
WARN: the attribute `version` is obsolete
```
**Causa:** Docker Compose v2 deprecó el campo `version:`

**Solución:**
```bash
# Este es solo un warning, NO afecta funcionalidad
# Puede ignorarse de forma segura
# Si deseas eliminarlo, quitar línea 1 de docker-compose.yml:
# version: "3.2"  <- Eliminar esta línea
```

### Problema: Puertos en formato diferente al esperado
```bash
# Ves: published: "8000" / target: 5000
# En lugar de: 8000:5000
```
**Causa:** Docker Compose v2 usa formato YAML expandido

**Solución:**
```bash
# Esto es correcto y equivalente:
# published: "8000" + target: 5000 = 8000:5000
# No requiere corrección
# Ver docs/COMPATIBILITY_NOTES.md sección "Verificación de Puertos"
```

---

## Checklist Final

Antes de considerar el proyecto completo:

### Funcionalidad
- [ ] Sistema se levanta con `docker-compose up -d` sin errores
- [ ] Login funciona en UI y API
- [ ] Clasificación de imágenes retorna resultados correctos
- [ ] Feedback se guarda en base de datos
- [ ] Tests unitarios pasan (api, model, ui)
- [ ] Tests de integración pasan (2/2)
- [ ] Stress testing ejecutado sin crashes

### Performance
- [ ] API responde en < 3 segundos
- [ ] Predicciones completan en < 5 segundos
- [ ] Sistema maneja 10+ usuarios concurrentes
- [ ] No hay memory leaks en tests largos

### Código
- [ ] No hay TODOs pendientes
- [ ] Código formateado con Black e isort
- [ ] Docstrings presentes
- [ ] No hay credenciales hardcodeadas
- [ ] Logs informativos implementados

### Documentación
- [ ] README actualizado
- [ ] Reporte de stress testing completo
- [ ] Screenshots incluidos
- [ ] Instrucciones claras de setup
- [ ] Troubleshooting documentado

### Git
- [ ] .gitignore protege archivos sensibles
- [ ] Commits siguen formato [EPIC-X-TX]
- [ ] Branches organizados por épica
- [ ] Historia de commits clara

### Opcional (Batch Processing)
- [ ] Batch processing implementado
- [ ] Comparativa de performance documentada
- [ ] Reporte incluye sección de batch

---

**Última actualización:** 2026-01-13  
**Versión:** 1.0

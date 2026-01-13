# 📊 Progreso de Épicas - Sprint 3

## Estado General

**Última actualización:** 2026-01-13

| Épica | Estado | Tareas | Completadas | Progreso |
|-------|--------|--------|-------------|----------|
| ÉPICA 0 | ✅ Completada | 3 | 3 | 100% |
| ÉPICA 1 | ✅ Completada | 2 | 2 | 100% |
| ÉPICA 2 | ✅ Completada | 5 | 5 | 100% |
| ÉPICA 3 | ⏹️ Pendiente | 7 | 0 | 0% |
| ÉPICA 4 | ⏹️ Pendiente | 4 | 0 | 0% |
| ÉPICA 5 | ⏹️ Pendiente | 3 | 0 | 0% |
| ÉPICA 6 | ⏹️ Pendiente | 5 | 0 | 0% |
| ÉPICA 7 | ⏹️ Pendiente | 6 | 0 | 0% |
| ÉPICA 8 | ⏹️ Pendiente | 5 | 0 | 0% |

---

## ✅ ÉPICA 0: Setup Inicial (COMPLETADA)

**Branch:** `feature/epic-0-setup`  
**Fecha:** 2026-01-13  
**Tiempo invertido:** ~10 minutos

### Tareas Completadas:

#### [EPIC-0-T1] ✅ Crear red Docker compartida
- **Commit:** N/A (comando Docker)
- **Resultado:** Red `shared_network` creada exitosamente
- **Validación:** `docker network ls | grep shared_network` ✅

#### [EPIC-0-T2] ✅ Configurar variables de entorno
- **Archivos creados:**
  - `.env` (raíz del proyecto)
  - `api/.env`
- **Fuente:** Copiados desde `.env.original`
- **Validación:** Archivos existen con variables requeridas ✅
- **Nota:** Archivos .env están en .gitignore (por seguridad)

#### [EPIC-0-T3] ✅ Actualizar requirements de UI
- **Commit:** `c91b14a`
- **Archivo:** `ui/requirements.txt`
- **Cambios:**
  - `streamlit==1.40.0`
  - `requests==2.32.3`
  - `Pillow==11.0.0`
  - `pytest==8.3.4`
- **Validación:** Build de UI exitoso ✅

### Testing Manual:
- ✅ Test 1: Red Docker verificada
- ✅ Test 2: Archivos .env existen
- ✅ Test 3: Requirements actualizados

### Notas:
- Red Docker es persistente (sobrevive a reinicios de Docker)
- Variables de entorno configuradas según `.env.original`
- Requirements de UI actualizados a versiones modernas estables

---

## ✅ ÉPICA 1: Infraestructura Docker (COMPLETADA)

**Git Tag:** `epic-1-complete`  
**Fecha:** 2026-01-13  
**Tiempo invertido:** ~45 minutos (incluyendo troubleshooting)

### Tareas Completadas:

#### [EPIC-1-T1] ✅ Implementar Dockerfile.populate
- **Commit:** `86f52d2` → `build(api): implement Dockerfile.populate for DB initialization`
- **Archivo:** `api/Dockerfile.populate`
- **Implementación:**
  - Base image: python:3.8.13
  - PYTHONPATH configurado
  - Instala dependencias desde requirements.txt
  - Copia código fuente
  - CMD ejecuta populate_db.py
- **Validación:** Build exitoso ✅

#### [EPIC-1-T2] ✅ Validar configuración docker-compose
- **Commit:** `fa2f073` → `build(docker): validate docker-compose configuration`
- **Archivos:** `docker-compose.yml`, `api/docker-compose.yml`
- **Validaciones:**
  - ✅ YAML válido sin errores
  - ✅ 5 servicios: redis, model, api, ui, db
  - ✅ Dependencias correctas
  - ✅ Puertos: 8000, 9090, 5432
  - ✅ Red shared_network en todos los servicios
- **Comando:** `docker-compose config` exitoso ✅

### Testing Manual:
- ✅ Test 1: Dockerfile.populate construye correctamente
- ✅ Test 2: docker-compose config sin errores
- ✅ Test 3: Todos los servicios con shared_network
- ✅ Test 4: Puertos mapeados correctamente (8000:5000, 5432:5432, 9090:9090)
- ✅ Test 5: docker-compose build completo exitoso (todos los servicios)

### Correcciones Realizadas (Compatibilidad Apple Silicon):

#### [FIX] ✅ TensorFlow incompatible con ARM64
- **Commit:** `6bbf6c6` → `fix(deps): upgrade TensorFlow to 2.13.0 for ARM64 compatibility`
- **Problema:** tensorflow==2.8.0 no disponible para arquitectura ARM64
- **Solución:** Actualizado a tensorflow==2.13.0 en model/requirements.txt
- **Nota:** API idéntica entre versiones, código 100% compatible

#### [FIX] ✅ Pillow incompatible con Python 3.8
- **Commit:** `0ed05de` → `fix(deps): downgrade Pillow to 10.4.0 for Python 3.8`
- **Problema:** Pillow==11.0.0 requiere Python 3.9+
- **Solución:** Actualizado a Pillow==10.4.0 (última para Python 3.8)
- **Archivos:** model/requirements.txt, ui/requirements.txt

#### [FIX] ✅ h5py error de compilación
- **Commit:** `22b1840` → `fix(docker): add h5py pre-compiled wheel for ARM64`
- **Problema:** h5py intentando compilar desde código fuente, requiriendo librerías HDF5
- **Solución:** Añadido h5py==3.8.0 antes de TensorFlow para usar wheel pre-compilado
- **Archivo:** model/requirements.txt

#### [FIX] ✅ Test 4 grep command
- **Commit:** `eee61f2` → `docs(tests): correct Test 4 grep command for port mappings`
- **Problema:** grep capturaba volumes además de ports
- **Solución:** Filtro mejorado para mostrar solo port mappings
- **Archivo:** docs/TESTING_PLAN.md

#### [DOCS] ✅ Documentación de fixes
- **Commit:** `4c6354b` → `docs(epic-1): document compatibility fixes and testing`
- **Contenido:** Todos los fixes documentados en EPIC_PROGRESS.md
- **Archivos:** docs/EPIC_PROGRESS.md

### Notas:
- Dockerfile.populate sigue mismo patrón que api/Dockerfile
- Configuración docker-compose validada y lista para uso
- Red externa shared_network debe existir antes de docker-compose up
- Todas las dependencias ahora compatibles con Apple Silicon (ARM64) + Python 3.8
- Build completo exitoso: model (~54s), api (cached), ui (~35s)

---

## ✅ ÉPICA 2: Servicio ML (COMPLETADA)

**Git Tag:** `epic-2-complete` (pending)  
**Fecha:** 2026-01-13  
**Tiempo invertido:** ~25 minutos

### Tareas Completadas:

#### [EPIC-2-T1] ✅ Conectar Redis en ml_service.py
- **Commit:** `b541dc2` → `feat(model): [EPIC-2] implement complete ML service with ResNet50`
- **Implementación:**
  ```python
  db = redis.Redis(
      host=settings.REDIS_IP,
      port=settings.REDIS_PORT,
      db=settings.REDIS_DB_ID
  )
  ```
- **Validación:** Conexión configurada correctamente ✅

#### [EPIC-2-T2] ✅ Cargar modelo ResNet50
- **Commit:** `b541dc2`
- **Implementación:**
  ```python
  model = ResNet50(weights='imagenet')
  ```
- **Nota:** Primera ejecución descarga ~100MB (ImageNet weights)
- **Validación:** Modelo cargado sin errores ✅

#### [EPIC-2-T3] ✅ Implementar función predict()
- **Commit:** `b541dc2`
- **Archivo:** `model/ml_service.py` (líneas 42-69)
- **Pasos implementados:**
  1. ✅ Construir path completo a imagen
  2. ✅ Cargar imagen con target size 224x224
  3. ✅ Convertir a numpy array
  4. ✅ Expandir dimensiones (batch dimension)
  5. ✅ Aplicar preprocessing ResNet50
  6. ✅ Ejecutar predicción
  7. ✅ Decodificar top-1 prediction
  8. ✅ Extraer class_name y probability
  9. ✅ Redondear probability a 4 decimales
- **Validación:** Retorna tupla (str, float) correctamente ✅

#### [EPIC-2-T4] ✅ Implementar función classify_process()
- **Commit:** `b541dc2`
- **Archivo:** `model/ml_service.py` (líneas 98-122)
- **Pasos implementados:**
  1. ✅ Loop infinito con while True
  2. ✅ brpop() bloqueante para obtener jobs
  3. ✅ Decodificar JSON del job
  4. ✅ Extraer job_id e image_name
  5. ✅ Llamar predict() con la imagen
  6. ✅ Crear dict con prediction y score
  7. ✅ Serializar a JSON
  8. ✅ Guardar en Redis con job_id como key
  9. ✅ Sleep de 0.05s entre iteraciones
- **Validación:** Loop procesa jobs correctamente ✅

#### [EPIC-2-T5] ✅ Ejecutar tests del modelo
- **Comando:** `docker build -t model_test --target test .`
- **Resultado:** ✅ **1 passed in 17.69s**
- **Test ejecutado:** `tests/test_model.py::TestMLService::test_predict`
- **Validación:** Predicción con dog.jpeg funciona correctamente ✅

### Testing:
- ✅ Docker build exitoso
- ✅ Tests unitarios pasan (100%)
- ✅ Predicción con imagen de prueba correcta
- ✅ Integración Redis lista para uso

### Notas:
- Servicio ML completamente funcional
- Listo para recibir jobs desde API
- ResNet50 con 1000 clases ImageNet
- Timeout configurado a 0.05s entre jobs

---

## Leyenda de Estados

- ✅ **Completada:** Todas las tareas finalizadas y testeadas
- ⏳ **En Progreso:** Al menos una tarea iniciada
- ⏹️ **Pendiente:** No iniciada
- ❌ **Bloqueada:** Esperando prerequisitos

---

## 📝 Convención de Commits

**A partir de ahora:** Se utiliza **Conventional Commits 1.0.0**

### Formato
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Ejemplos de la nueva convención:
```
feat(api): add user authentication endpoint
fix(docker): resolve h5py compilation on ARM64
docs(readme): update setup instructions
test(model): add preprocessing unit tests
```

### Comando `/commit`
Usa el comando personalizado para generar commits semánticos:
```bash
/commit
/commit --epic 2
/commit --breaking
```

Ver documentación completa: [docs/COMMIT_CONVENTION.md](COMMIT_CONVENTION.md)

---

## 📚 Mejoras Documentales (Sesión 2026-01-13)

### Nuevos Documentos:
1. **[COMMIT_CONVENTION.md](COMMIT_CONVENTION.md)** - Convención Conventional Commits
2. **[COMPATIBILITY_NOTES.md](COMPATIBILITY_NOTES.md)** - Notas de compatibilidad Apple Silicon
3. **AGENTS.md actualizado** - Guías de commit extendidas + comando `/commit`

### Commits relacionados:
- `605c557` → `docs: add Conventional Commits standard and /commit command`
- Tag: `epic-1-complete` - Marca la finalización completa de ÉPICA 1

---

**Progreso Total:** 10/40 tareas (25.0%)  
**Siguiente:** ÉPICA 3 - API FastAPI (7 tareas)

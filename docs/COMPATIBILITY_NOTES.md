# 🔧 Notas de Compatibilidad

## Apple Silicon (M1/M2/M3) - ARM64

### Problema con TensorFlow 2.8.0

**Síntoma:**
```
ERROR: Could not find a version that satisfies the requirement tensorflow==2.8.0
```

**Causa:**
TensorFlow 2.8.0 fue lanzado antes del soporte oficial para Apple Silicon (ARM64). Solo las versiones 2.10.0+ tienen binarios compilados para arquitectura ARM64.

**Solución Aplicada:**
Actualizado `model/requirements.txt` a:
- `tensorflow==2.13.0` (primera versión estable con soporte ARM64 completo)
- `protobuf==3.20.3` (compatible con TF 2.13)
- `Pillow==11.0.0` (mejor soporte ARM64)
- `pytest==8.3.4` (últimas mejoras)
- `redis==5.2.0` (mejor performance)

### Compatibilidad del Código

✅ **El código existente es 100% compatible**

La API de ResNet50 no cambió entre TensorFlow 2.8 y 2.13:
- `tensorflow.keras.applications.ResNet50` - ✅ Idéntico
- `tensorflow.keras.applications.resnet50.preprocess_input` - ✅ Idéntico
- `tensorflow.keras.applications.resnet50.decode_predictions` - ✅ Idéntico
- `tensorflow.keras.preprocessing.image` - ✅ Idéntico

### Alternativa: Dockerfile.M1

Si prefieres usar el Dockerfile específico para M1:
```bash
# En docker-compose.yml, cambiar:
model:
  build:
    context: ./model
    dockerfile: ./Dockerfile.M1  # En lugar de ./Dockerfile
```

**Nota:** Para este proyecto, optamos por actualizar requirements en lugar de usar Dockerfile.M1 porque:
1. Es más simple (un solo Dockerfile)
2. TensorFlow 2.13 es más moderno y estable
3. Mejor soporte para ARM64 nativo
4. No requiere modificar docker-compose.yml

---

## Verificación de Puertos en Docker Compose

### Formato de Salida

Cuando ejecutas `docker-compose config | grep -A 2 "ports:"`, el formato moderno de Docker Compose v2 muestra:

```yaml
ports:
  - mode: ingress
    target: 5000
    published: "8000"
    protocol: tcp
```

Esto es equivalente a la notación corta: `8000:5000`

**Traducción:**
- `published: "8000"` = Puerto del host (tu máquina)
- `target: 5000` = Puerto del contenedor
- **Significa:** `8000:5000` ✅

### Puertos Configurados

| Servicio | Puerto Host | Puerto Container | Notación Corta |
|----------|-------------|------------------|----------------|
| API | 8000 | 5000 | 8000:5000 |
| DB | 5432 | 5432 | 5432:5432 |
| UI | 9090 | 9090 | 9090:9090 |

### Test Mejorado

Para validar puertos de forma más clara:

```bash
# Opción 1: Verificar published ports
docker-compose config | grep "published:" 

# Opción 2: Ver solo los servicios con sus puertos
docker-compose config | grep -B 5 "published:" | grep -E "(api:|db:|ui:|published:)"

# Opción 3: Usar docker-compose port (con servicios corriendo)
docker-compose port api 5000
docker-compose port db 5432
docker-compose port ui 9090
```

---

## Verificación de Arquitectura

Para saber si estás en Apple Silicon:

```bash
uname -m
# arm64 = Apple Silicon (M1/M2/M3)
# x86_64 = Intel
```

Para ver qué arquitectura usa una imagen Docker:

```bash
docker image inspect tensorflow/tensorflow:2.13.0 | grep Architecture
```

---

## Troubleshooting Adicional

### Si el build sigue fallando

1. **Limpiar cache de Docker:**
   ```bash
   docker-compose build --no-cache model
   ```

2. **Verificar versiones disponibles:**
   ```bash
   docker run --rm python:3.8.13 pip index versions tensorflow
   ```

3. **Verificar conectividad a PyPI:**
   ```bash
   docker run --rm python:3.8.13 pip install --dry-run tensorflow==2.13.0
   ```

### Warning sobre `version` en docker-compose.yml

```
WARN: the attribute `version` is obsolete
```

**Causa:** Docker Compose v2 deprecó el campo `version:`

**Solución (opcional):**
Eliminar la primera línea `version: "3.2"` del `docker-compose.yml`

**Nota:** Es solo un warning, no afecta funcionalidad. Lo dejamos por compatibilidad con versiones anteriores.

---

**Última actualización:** 2026-01-13  
**Probado en:** Apple Silicon (M1/M2/M3)

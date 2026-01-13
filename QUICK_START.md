# 🚀 QUICK START - Sprint 3 ML Microservices

## 📚 Documentación Disponible

Este proyecto tiene 3 documentos principales que debes consultar:

### 1. 📋 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)
**Qué contiene:**
- 9 Épicas organizadas (ÉPICA 0 a ÉPICA 8)
- 40 Tareas detalladas con ID único
- Código de implementación para cada tarea
- Estimaciones de tiempo
- Prerequisitos y dependencias
- Formato de commits para Git

**Cuándo usarlo:**
- ✅ Para saber QUÉ implementar
- ✅ Para entender CÓMO implementar cada tarea
- ✅ Para seguir el orden correcto de desarrollo

### 2. 🧪 [TESTING_PLAN.md](TESTING_PLAN.md)
**Qué contiene:**
- Guía de testing manual para cada épica
- Comandos exactos para tests automáticos
- Pasos detallados con resultados esperados
- Troubleshooting común
- Checklist final de calidad

**Cuándo usarlo:**
- ✅ Después de completar cada tarea/épica
- ✅ Cuando algo no funciona (troubleshooting)
- ✅ Para validar que todo está correcto

### 3. 📖 [AGENTS.md](AGENTS.md)
**Qué contiene:**
- Convenciones de código
- Estándares de Python (Black, isort)
- Patrones de FastAPI, SQLAlchemy, Pydantic
- Buenas prácticas de seguridad
- Code review checklist

**Cuándo usarlo:**
- ✅ Al escribir código nuevo
- ✅ Para mantener consistencia
- ✅ Durante code reviews

---

## 🎯 Flujo de Trabajo Recomendado

### Para Cada Épica:

```bash
# 1. Leer la épica en DEVELOPMENT_PLAN.md
# 2. Crear branch
git checkout -b feature/epic-X-nombre

# 3. Para cada tarea:
#    a. Leer tarea en DEVELOPMENT_PLAN.md
#    b. Implementar según especificación
#    c. Commit con formato:
git add .
git commit  # Usa la plantilla automática
# Formato: [EPIC-X-TX] Descripción breve

# 4. Después de completar TODAS las tareas de la épica:
#    a. Ir a TESTING_PLAN.md
#    b. Ejecutar "Testing por Épica" correspondiente
#    c. Verificar que todos los tests pasan

# 5. Merge a main
git checkout main
git merge feature/epic-X-nombre
```

---

## 📊 Resumen de Épicas

| # | Épica | Tareas | Tiempo | Prioridad |
|---|-------|--------|--------|-----------|
| 0 | Setup Inicial | 3 | 30min | CRÍTICA |
| 1 | Infraestructura Docker | 2 | 45min | CRÍTICA |
| 2 | Servicio ML | 5 | 3-4h | ALTA |
| 3 | API FastAPI | 7 | 4-5h | ALTA |
| 4 | UI Streamlit | 4 | 2-3h | MEDIA |
| 5 | Testing Integración | 3 | 1-2h | ALTA |
| 6 | Stress Testing | 5 | 3-4h | MEDIA |
| 7 | Batch Processing (Opcional) | 6 | 4-6h | BAJA |
| 8 | Calidad/Docs | 5 | 2-3h | MEDIA |

**Total:** 40 tareas, 22-33 horas

---

## ⚡ Inicio Rápido

### Prerequisitos:
```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Python
python3 --version  # 3.8+
```

### Empezar con ÉPICA 0:

```bash
# 1. Crear branch
git checkout -b feature/epic-0-setup

# 2. Ejecutar tareas (ver DEVELOPMENT_PLAN.md)
docker network create shared_network
cp .env.original .env
cd api && cp .env.original .env && cd ..

# 3. Testing (ver TESTING_PLAN.md - ÉPICA 0)
docker network ls | grep shared_network
ls -la .env api/.env

# 4. Commit
git add .env api/.env
git commit -m "[EPIC-0-T2] Configurar variables de entorno para todos los servicios

Archivos creados:
- .env (raíz)
- api/.env

Variables configuradas:
- POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
- DATABASE_HOST, SECRET_KEY, REDIS_IP

Refs: EPIC-0-T2"

# 5. Continuar con siguiente tarea...
```

---

## 🔍 Comandos Útiles

### Git:
```bash
# Ver status
git status

# Ver log de commits
git log --oneline --graph

# Ver branches
git branch -a

# Ver cambios
git diff
```

### Docker:
```bash
# Levantar sistema
docker-compose up -d

# Ver logs
docker-compose logs -f [servicio]

# Ver estado
docker-compose ps

# Reiniciar servicio
docker-compose restart [servicio]

# Bajar todo
docker-compose down
```

### Testing:
```bash
# Tests API
cd api && docker build -t fastapi_test --target test .

# Tests Model
cd model && docker build -t model_test --target test .

# Tests UI
cd ui && docker build -t ui_test --target test .

# Tests Integración
python tests/test_integration.py

# Formateo
make format
```

---

## 📍 Estado Actual del Proyecto

```bash
# Ver en qué commit estamos
git log -1 --oneline

# Ver archivos trackeados
git ls-files

# Ver archivos ignorados
git status --ignored
```

**Commit actual:**
```
[SETUP] Agregar planes de desarrollo, testing y configuración Git
```

**Archivos de documentación:**
- ✅ DEVELOPMENT_PLAN.md (Plan de desarrollo completo)
- ✅ TESTING_PLAN.md (Plan de testing)
- ✅ AGENTS.md (Guía de código)
- ✅ QUICK_START.md (Este archivo)
- ✅ .gitignore (Configurado)
- ✅ .gitmessage (Plantilla de commits)

**Próximo paso:** Comenzar con [ÉPICA 0] en DEVELOPMENT_PLAN.md

---

## 🆘 Ayuda

### ¿No sabes qué hacer?
1. Abre DEVELOPMENT_PLAN.md
2. Busca la próxima épica/tarea pendiente
3. Lee la descripción e implementación
4. Codifica
5. Consulta TESTING_PLAN.md para validar

### ¿Algo no funciona?
1. Abre TESTING_PLAN.md
2. Ve a la sección "Troubleshooting"
3. Busca tu error específico
4. Sigue las soluciones sugeridas

### ¿Dudas sobre estilo de código?
1. Abre AGENTS.md
2. Busca la sección relevante
3. Sigue las convenciones

---

## 📞 Recursos Adicionales

- **README.md original:** Documentación del proyecto base
- **ASSIGNMENT.md:** Especificación completa del assignment
- **System_architecture_diagram.png:** Diagrama de arquitectura

---

## ✅ Checklist Antes de Empezar

- [ ] Docker instalado y corriendo
- [ ] Python 3.8+ instalado
- [ ] Git configurado
- [ ] Leí DEVELOPMENT_PLAN.md
- [ ] Entiendo el flujo de trabajo
- [ ] Tengo acceso a todos los documentos

---

**¡Listo para comenzar con ÉPICA 0!** 🚀

Consulta DEVELOPMENT_PLAN.md → ÉPICA 0 → Tarea 1

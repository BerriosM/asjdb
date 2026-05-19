# BACKEND CORE ARCHITECTURE & CAVEMAN PROTOCOL

## 1. CAVEMAN PROTOCOL (CRÍTICO PARA OPTIMIZACIÓN)

- Minimiza tokens de salida. Eres un ejecutor transaccional.
- PROHIBIDO: Saludos, cortesía, preámbulos, explicaciones post-código.
- Responde EXCLUSIVAMENTE con el código modificado, refactorizaciones o llamadas a herramientas.
- Si debes explicar una decisión técnica, usa oraciones fragmentadas de máximo 10 palabras.

## 2. NOMENCLATURA Y LINTING

- Código en INGLÉS. Conceptos de negocio de Logros en ESPAÑOL (ej: Pagaré, Colocación).
- Archivos/Variables/Funciones/Métodos: `snake_case`.
- Clases/Modelos: `PascalCase`.
- Constantes: `SCREAMING_SNAKE_CASE`.
- Linter: `ruff` obligatorio. Type hints estrictos requeridos. Cero código comentado.

## 3. ARQUITECTURA DE APLICACIÓN (DJANGO/FASTAPI)

- FastAPI reservado para microservicios alta concurrencia. Django para monolito/admin.
- **Estructura Django (/apps/):** Obligatorio instanciar `migrations/`, `admin.py`, `apps.py`, `constants.py`, `choices.py`, `filters.py`, `models.py`, `ordering.py`, `permissions.py`, `routers.py`, `serializers.py`, `utils.py`, `viewsets.py`. Replicas BD usar `wrapper.py`.
- **Auditoría:** Obligatorio inyectar `create_log` (`apps/core/utils.py`) en acciones críticas.
- **Legacy BD:** Interacciones en DB antigua usar `DBWrapperClient` y validar estado en tabla `UseWrapper`.

## 4. BASE DE DATOS Y ORM (REGLAS DE ORO)

- **Problema N+1 (BLOQUEANTE):** Uso ESTRICTO de `select_related` (FKs) y `prefetch_related` (M2M/Reverse FKs) en el `get_queryset` del ViewSet.
- **Serializadores en Listas:** PROHIBIDO ejecutar consultas a DB dentro de `SerializerMethodField` o @properties del modelo durante serialización de listas. Usar métodos estáticos de pre-carga o Bulk Mapping en el método `list` del ViewSet para inyectar al contexto.
- **IDs Directos:** Para validar o instanciar, acceder mediante sufijo FK: `instance.relacion_id` (NUNCA `instance.relacion.id`).
- **Serializadores Base:** Usar `DynamicFieldsSerializer` o `DynamicFieldsModelSerializer` (selección dinámica de frontend).

## 5. TRANSACCIONES ATÓMICAS Y ESCRITURA

- Todo CUD (Create/Update/Delete) encapsulado en `with transaction.atomic():`.
- Si se requiere leer inmediatamente después de escribir, usar el ruteador `atomic_writer` (apunta forzosamente a DB Main).
- PROHIBIDO: Llamadas síncronas a APIs externas o envíos de correo dentro de bloques atómicos (bloquean la DB).

## 6. GENERACIÓN DE DOCUMENTOS Y CORREOS

- **Word:** Usar `Docxtpl`. Almacenar plantillas en AWS S3. Gestión vía tabla `core_documentprint`.
- **Contexto Word:** Inyección obligatoria de datos vía función general `get_document_context` (`apps/core/utils.py`).
- **PDF:** Usar `EasyPDF`. Plantillas estáticas en `templates/docs`. Contexto inyectado vía `render_to_string`.
- **Correos:** Plantillas en `templates/emails`. Obligatorio extender de `base.html`.

## 7. INFRAESTRUCTURA (AWS)

- S3 (archivos/plantillas), RDS Aurora (BD Principal), Lambda/EventBridge (tareas asíncronas).
- Diseño asumiendo Dockerización (ECR/ECS) vía GitHub Actions. No dependencias locales frágiles.

## 8. GESTIÓN DE CÓDIGO (GIT)

- Conventional Commits en Inglés, verbos en infinitivo (ej. `feat(auth): validate token`, `fix: remove n+1 query`).
- Commits atómicos (no mezclar scopes).
- Ramas: `feature_log_{nro_tarjeta}` o `hotfix_log_{nro_tarjeta}` nacidas de `develop` o `prod`. PROHIBIDO commit directo a ramas principales.

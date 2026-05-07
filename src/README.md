# AulaShare

Aplicacion web colaborativa de recursos universitarios por asignatura.

## Requisitos

- Python 3.11 o superior
- Redis disponible en local

## Instalacion rapida

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
redis-server &
flask --app run.py run --debug
```

La aplicacion queda disponible en `http://127.0.0.1:5000`.

## Variables opcionales

- `SECRET_KEY`: clave secreta de Flask
- `REDIS_URL`: por defecto `redis://localhost:6379/0`

## Estructura

- `app/auth`: usuarios, registro e inicio de sesion
- `app/subjects`: asignaturas
- `app/resources`: recursos de estudio
- `app/comments`: comentarios asincronos con HTMX
- `app/ratings`: valoraciones asincronas con HTMX

## Notas funcionales

- Un recurso pertenece a una asignatura y a un autor.
- Un usuario puede comentar y valorar recursos.
- Solo el autor puede editar o borrar sus recursos/comentarios.
- El borrado de un recurso elimina sus comentarios y valoraciones.
- Una asignatura no se puede borrar si aun tiene recursos asociados.

# Docker: contenerizar un servicio FastAPI

Los ejercicios explican proceso, variables, health checks y construcción de una imagen.
El Dockerfile final usa el servicio comentado de `02_en_marcha`.

```powershell
pip install -r 03_extras/L5_adaptacion_y_despliegue/docker/requirements.txt
docker build -f 03_extras/L5_adaptacion_y_despliegue/docker/02_en_marcha/Dockerfile -t aem4-fastapi 03_extras/L5_adaptacion_y_despliegue/docker
docker run --rm -p 8000:8000 aem4-fastapi
```

Luego consultá `http://127.0.0.1:8000/salud`.

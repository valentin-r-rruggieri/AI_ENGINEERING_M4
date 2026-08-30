# FastAPI: APIs para modelos y MCP

Ejemplos breves de rutas, validación, lifespan, asincronía y montaje de un servidor MCP.
FastAPI se inicia con Uvicorn, por eso los archivos no usan bloque `__main__`.

```powershell
pip install -r extras/L3_mcp_y_agentes/fastapi/requirements.txt
cd extras/L3_mcp_y_agentes/fastapi/00_fundamentos
uvicorn 00_ruta_basica:app --reload
```

El integrador se ejecuta desde su carpeta con `uvicorn servicio_inferencia:app --reload`.

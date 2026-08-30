# Langfuse: trazas, spans y métricas

Recorrido actualizado al SDK Python v4. Los ejemplos usan `get_client`, `observe` y
`start_as_current_observation`; no utilizan la API antigua `client.trace()`.

```powershell
pip install -r extras/L5_adaptacion_y_despliegue/langfuse/requirements.txt
$env:LANGFUSE_PUBLIC_KEY="pk-lf-..."
$env:LANGFUSE_SECRET_KEY="sk-lf-..."
$env:LANGFUSE_BASE_URL="https://cloud.langfuse.com"
python extras/L5_adaptacion_y_despliegue/langfuse/00_fundamentos/00_cliente.py
```

Las trazas de scripts cortos llaman `flush()` antes de finalizar. Terminá con
`03_en_marcha/pipeline_observable.py` y luego comparalo con `../../PI_legalmove/langfuse`.

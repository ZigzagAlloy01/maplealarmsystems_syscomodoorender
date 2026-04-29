# Render Cron Job para SYSCOM

## Archivos importantes

- `syscom_sync_core.py`: logica reusable sin interfaz.
- `syscom_sync_job.py`: entrypoint automatico para Render.
- `syscom_odoo_sync.py`: interfaz manual con `tkinter`.
- `models_syscom.txt`: lista base de modelos para el job.
- `requirements.txt`: dependencias Python.

## Que ejecuta Render

Render debe correr:

```bash
python syscom_sync_job.py
```

Ese script:

- lee modelos desde `SYSCOM_MODELS` o `SYSCOM_MODELS_FILE`
- consulta SYSCOM
- crea productos faltantes en Odoo
- sobrescribe productos existentes en Odoo
- actualiza compras y stock
- deja logs de resumen

## Variables de entorno en Render

Configura estas variables:

- `ODOO_PASSWORD`
- `SYSCOM_TOKEN`

Opcionales:

- `ODOO_URL=https://maplealarmsystems.odoo.com`
- `ODOO_DB=maplealarmsystems`
- `ODOO_USERNAME=sistemas@storemaple.com`
- `SYSCOM_MODELS_FILE=models_syscom.txt`
- `SYSCOM_MODELS`
- `SYSCOM_BASE_URL=https://developers.syscom.mx/api/v1/`
- `REQUEST_TIMEOUT=30`

Si defines `SYSCOM_MODELS`, tiene prioridad sobre el archivo. Puede ir separado por saltos de linea, comas o punto y coma.

## Configuracion recomendada en Render

Al crear el servicio:

- **Service Type**: `Cron Job`
- **Build Command**:

```bash
pip install -r requirements.txt
```

- **Start Command / Command**:

```bash
python syscom_sync_job.py
```

- **Schedule**:

```text
0 9 * * *
```

Eso significa una vez al dia a las 09:00 UTC. Ajusta la hora segun tu operacion. Render usa UTC.

## Flujo recomendado

1. Sube esta carpeta a un repo de GitHub.
2. Crea el Cron Job en Render.
3. Conecta el repo y la rama.
4. Configura las variables de entorno.
5. Lanza una ejecucion manual desde Render.
6. Revisa logs.
7. Si todo sale bien, deja activo el horario diario.

## Notas operativas

- El job automatico hace ambas cosas: crear nuevos y sobrescribir existentes.
- Si hay errores, `syscom_sync_job.py` termina con codigo distinto de cero para que Render marque la corrida como fallida.
- El archivo `modelos_no_encontrados_syscom.txt` se genera en cada corrida solo como apoyo de logs; no debe tratarse como almacenamiento persistente.
- En Render no dependas de `config.py`; el despliegue correcto es con variables de entorno.

# Ripple Radar Pro v69 — despliegue público seguro

Este paquete está preparado para subirse sin exponer la API key.

## Archivos que NO deben subirse nunca

- `.env`
- `.streamlit/secrets.toml`
- `.venv/`
- `__pycache__/`
- `*.pyc`

Ya están bloqueados en `.gitignore`.

## Streamlit Cloud

En el panel de la app:

`Settings → Secrets`

Pega:

```toml
ANTHROPIC_API_KEY = "tu_clave_anthropic"
```

Reinicia la app.

## Cloudflare Tunnel desde tu PC

Antes de abrir la app, define la variable:

```powershell
setx ANTHROPIC_API_KEY "tu_clave_anthropic"
```

Cierra y reabre PowerShell/CMD, luego ejecuta:

```powershell
EJECUTAR_RADAR.bat
```

## Verificación dentro de la app

En Diagnóstico / Configuración debe aparecer que la API key está detectada vía variable de entorno o Streamlit Secrets.

No debería aparecer ninguna clave completa, solo preview parcial.

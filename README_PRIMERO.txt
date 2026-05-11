RIPPLE RADAR PRO v69 - paquete publico con API por variable secreta
====================================================================

Contenido limpio:
- NO incluye .venv
- NO incluye __pycache__
- NO incluye .env con claves reales
- NO incluye secrets.toml real
- Incluye la base ripple_radar_advanced.sqlite
- Incluye el archivo principal v69 con BUILD visible:
  v69_2026_05_11_DEDUCTIVE_ENGINE_PROOFS

Como ejecutar en local:
1) Descomprime el ZIP en una carpeta nueva.
2) Instala dependencias si hace falta:
   REINSTALAR_DEPENDENCIAS.bat
3) Ejecuta:
   EJECUTAR_RADAR.bat
4) En la app debe aparecer el BUILD v69. Si no aparece, estas ejecutando otra copia.

API / Discovery / IA:
- Para PUBLICAR, NO subas .env con claves.
- Configura ANTHROPIC_API_KEY como variable secreta del hosting.
- La app ya lee la clave desde:
  1) variable de entorno ANTHROPIC_API_KEY
  2) Streamlit Secrets
  3) .env local si existe
  4) input manual en la UI

Para Streamlit Cloud:
1) Sube estos archivos a GitHub SIN .env.
2) En Streamlit Cloud abre tu app.
3) En Settings -> Secrets pega:
   ANTHROPIC_API_KEY = "tu_clave"
4) Guarda y reinicia la app.

Para Cloudflare Tunnel/local:
1) Define la variable en tu PC antes de ejecutar:
   setx ANTHROPIC_API_KEY "tu_clave"
2) Cierra y abre PowerShell/CMD.
3) Ejecuta EJECUTAR_RADAR.bat.

Seguridad:
- No compartas .env.
- No subas .streamlit/secrets.toml.
- .gitignore ya bloquea .env y secrets.toml.

Datos:
- La app arranca con la base incluida.
- Para que el radar gane valor, necesita pruebas buenas:
  connection_proofs, dynamic_routes, rutas A->B verificadas, wallets aprobadas y fuentes.
- Las wallets desconocidas/basura deben quedar en descartadas o watchlist, no en radar.

Reset:
- Si quieres empezar desde cero, ejecuta RESET_DATOS_RADAR.bat.

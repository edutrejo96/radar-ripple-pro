# =============================================================================
# RIPPLE RADAR PRO — ENTRYPOINT COMPATIBLE
# Este archivo mantiene el main file path antiguo de Streamlit Cloud,
# pero ejecuta la versión nueva v70 con Radar FM público.
# =============================================================================

from pathlib import Path

V70_FILE = "ripple_radar_pro_route_engine_v70_PUBLIC_RADAR_FM_STATIC_TRACKS.py"

current_dir = Path(__file__).resolve().parent
v70_path = current_dir / V70_FILE

if not v70_path.exists():
    raise FileNotFoundError(
        f"No se encontró {V70_FILE}. "
        f"Debe estar en la raíz del repositorio junto a este archivo."
    )

code = v70_path.read_text(encoding="utf-8")
exec(compile(code, str(v70_path), "exec"), globals())

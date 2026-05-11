from pathlib import Path

NEXT_FILE = "ripple_radar_pro_route_engine_v73_RADAR_FM_PATH_FIX_ROUTE_LIVE.py"

current_dir = Path(__file__).resolve().parent
next_path = current_dir / NEXT_FILE

if not next_path.exists():
    raise FileNotFoundError(f"No se encontró {NEXT_FILE} en la raíz del repositorio.")

code = next_path.read_text(encoding="utf-8")
exec(compile(code, str(next_path), "exec"), globals())

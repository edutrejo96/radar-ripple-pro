from pathlib import Path

NEXT_FILE = "ripple_radar_pro_route_engine_v74_RADAR_FM_AUTONEXT_ROUTE_LIVE.py"

current_dir = Path(__file__).resolve().parent
next_path = current_dir / NEXT_FILE

if not next_path.exists():
    raise FileNotFoundError(
        f"No se encontró {NEXT_FILE} en la raíz del repositorio. "
        f"Sube primero {NEXT_FILE} junto a este archivo v69."
    )

code = next_path.read_text(encoding="utf-8")
exec(compile(code, str(next_path), "exec"), globals())

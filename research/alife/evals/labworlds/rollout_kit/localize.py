"""Write configs_local/*.toml with this kit's absolute path in place of @KIT@.  Usage: python localize.py"""
from pathlib import Path

kit = Path(__file__).resolve().parent
out = kit / "configs_local"
out.mkdir(exist_ok=True)
for f in sorted((kit / "configs").glob("*.toml")):
    (out / f.name).write_text(f.read_text().replace("@KIT@", str(kit)))
print(f"wrote {len(list(out.glob('*.toml')))} configs to {out}")

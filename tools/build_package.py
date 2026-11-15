#!/usr/bin/env python3
"""Build a deterministic source package. This does not install a Skill or plugin."""
from pathlib import Path
import hashlib
import json
import zipfile
ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIRS = ("agents", "references", "workflows", "schemas", "templates", "examples", "scripts")
def runtime_files():
    candidates = [ROOT / "SKILL.md", ROOT / "VERSION"]
    for directory in RUNTIME_DIRS:
        candidates.extend((ROOT / directory).rglob("*"))
    result = []
    for path in candidates:
        if path.is_symlink():
            raise ValueError(f"Symlink forbidden in package: {path.relative_to(ROOT)}")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            result.append(path)
    return sorted(set(result))
def build():
    version = (ROOT / "VERSION").read_text().strip()
    target = ROOT / "build" / f"soc-ai-investigator-source-{version}.zip"
    target.parent.mkdir(exist_ok=True)
    manifest = []
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in runtime_files():
            data = path.read_bytes()
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"soc-ai-investigator/{rel}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
            manifest.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    payload = {"kind":"Skill source subset; import NOT RUN","version":version,
               "archive":target.name,"sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"files":manifest}
    (ROOT/"build/package-manifest.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
    return payload
if __name__ == "__main__":
    p = build()
    print(json.dumps({k:v for k,v in p.items() if k != "files"},ensure_ascii=False))
    print(f"Included files: {len(p['files'])}")

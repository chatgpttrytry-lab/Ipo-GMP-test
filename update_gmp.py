import json, urllib.request, pathlib, datetime

SOURCE = "https://raw.githubusercontent.com/Spectrumz00/india-ipo-gmp-data/main/data/gmp-latest.json"
OUT = pathlib.Path("data/gmp-live.json")

req = urllib.request.Request(SOURCE, headers={"User-Agent": "IPO-GMP-GitHub-Updater/1.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    obj = json.load(r)

if isinstance(obj, list):
    ipos = obj
    meta = {}
elif isinstance(obj, dict):
    ipos = obj.get("ipos") or obj.get("data") or obj.get("items") or []
    meta = obj
else:
    raise RuntimeError("Unexpected JSON format")

if not isinstance(ipos, list):
    raise RuntimeError("IPO list not found in source JSON")

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
out = {
    "generated_at": meta.get("generated_at") or now,
    "generated_display": meta.get("generated_display") or meta.get("updated_at") or now,
    "source": "gmptoday.in via Spectrumz00/india-ipo-gmp-data",
    "source_url": "https://gmptoday.in/",
    "ipos": ipos
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Updated {len(ipos)} IPO records")

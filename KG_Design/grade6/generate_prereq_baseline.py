import csv
from pathlib import Path
import re

THIS = Path(__file__).resolve().parent
SKILLS = THIS / "skills.csv"
OUT = THIS / "prerequisites.csv"

def parse_skill(s: str):
    # Expect formats like K6_A1, K6_B2, etc.
    m = re.match(r"K6_([A-Z])(\d+)", s)
    if not m:
        return None, None
    return m.group(1), int(m.group(2))

def main():
    if not SKILLS.exists():
        print(f"Missing {SKILLS}. Run build_grade6_inputs.py first.")
        return

    buckets = {}  # letter -> list of (num, skillId)
    with open(SKILLS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            sid = r["skillId"]
            letter, num = parse_skill(sid)
            if letter is None:
                continue
            buckets.setdefault(letter, []).append((num, sid))

    rels = []
    for letter, items in buckets.items():
        items.sort()
        for i in range(len(items) - 1):
            _, src = items[i]
            _, dst = items[i + 1]
            rels.append({"fromSkillId": src, "toSkillId": dst, "relationType": "PREREQUISITE_OF", "note": "baseline auto"})

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["fromSkillId","toSkillId","relationType","note"])
        writer.writeheader()
        for r in rels:
            writer.writerow(r)

    print(f"Wrote {OUT} with {len(rels)} prerequisite edges (baseline). Review and adjust.")

if __name__ == "__main__":
    main()


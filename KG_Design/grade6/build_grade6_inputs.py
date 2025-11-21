import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
K6_DIR = ROOT / "Bai_tap_Tin_6"
OUT_DIR = Path(__file__).resolve().parent

def _read_csv_rows(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def generate_skills_and_mapping():
    topic_seen = {}
    mapping_rows = []

    if not K6_DIR.exists():
        print(f"Not found: {K6_DIR}")
        return

    for csv_file in sorted(K6_DIR.glob("*.csv")):
        for row in _read_csv_rows(csv_file):
            topic_id = row.get("topic_id") or ""
            qid = row.get("q_id") or ""
            if topic_id:
                if topic_id not in topic_seen:
                    topic_seen[topic_id] = {
                        "skillId": topic_id,
                        "name": topic_id.replace("_", " "),
                        "domain": "",
                        "bloomLevel": row.get("difficulty",""),
                        "grade": "6",
                        "description": f"Auto from {csv_file.name}",
                    }
            if qid and topic_id:
                mapping_rows.append({"q_id": qid, "skillId": topic_id})

    # write skills.csv
    skills_file = OUT_DIR / "skills.csv"
    with open(skills_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["skillId","name","domain","bloomLevel","grade","description"])
        writer.writeheader()
        for meta in topic_seen.values():
            writer.writerow(meta)
    print(f"Wrote {skills_file} with {len(topic_seen)} skills")

    # write question_skill.csv
    qs_file = OUT_DIR / "question_skill.csv"
    with open(qs_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["q_id","skillId"])
        writer.writeheader()
        for r in mapping_rows:
            writer.writerow(r)
    print(f"Wrote {qs_file} with {len(mapping_rows)} mappings")

if __name__ == "__main__":
    generate_skills_and_mapping()


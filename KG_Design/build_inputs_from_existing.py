import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K6_DIR = ROOT / "Bai_tap_Tin_6"
K7_DIR = ROOT / "Bai_tap_Tin_7"
OUT_DIR = ROOT / "KG_Design" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_skills_from_questions():
    """
    Scan K6/K7 question CSVs, read topic_id, and emit skills.csv (unique).
    """
    topic_to_meta = {}

    def scan_dir(dir_path: Path, grade: int):
        for csv_file in sorted(dir_path.glob("*.csv")):
            with csv.open(csv_file, "r") as f:  # type: ignore[attr-defined]
                pass

def _read_csv_rows(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def build_skills():
    topic_seen = {}
    for grade_dir, grade in [(K6_DIR, 6), (K7_DIR, 7)]:
        if not grade_dir.exists():
            continue
        for csv_file in sorted(grade_dir.glob("*.csv")):
            for row in _read_csv_rows(csv_file):
                topic_id = row.get("topic_id") or row.get("TopicId") or row.get("topic") or ""
                if not topic_id:
                    continue
                if topic_id not in topic_seen:
                    topic_seen[topic_id] = {"skillId": topic_id, "name": topic_id.replace("_", " "), "domain": "", "bloomLevel": row.get("difficulty",""), "grade": str(grade), "description": f"Auto from {csv_file.name}"}

    out_file = OUT_DIR / "skills.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["skillId","name","domain","bloomLevel","grade","description"])
        writer.writeheader()
        for meta in topic_seen.values():
            writer.writerow(meta)
    print(f"Wrote {out_file} with {len(topic_seen)} skills")

def build_question_skill_map():
    """
    Emit question_skill.csv: q_id -> skillId
    """
    out_file = OUT_DIR / "question_skill.csv"
    with open(out_file, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=["q_id","skillId"])
        writer.writeheader()
        count = 0
        for grade_dir in [K6_DIR, K7_DIR]:
            if not grade_dir.exists():
                continue
            for csv_file in sorted(grade_dir.glob("*.csv")):
                for row in _read_csv_rows(csv_file):
                    qid = row.get("q_id") or row.get("id") or row.get("QID") or ""
                    skill = row.get("topic_id") or row.get("TopicId") or row.get("topic") or ""
                    if qid and skill:
                        writer.writerow({"q_id": qid, "skillId": skill})
                        count += 1
        print(f"Wrote {out_file} with {count} mappings")

if __name__ == "__main__":
    build_skills()
    build_question_skill_map()


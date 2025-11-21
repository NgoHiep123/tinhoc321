import csv
from pathlib import Path
import json
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
STUDENTS_JSON = ROOT / "students_grade_data.json"
SKILLS_CSV = Path(__file__).resolve().parent / "skills.csv"
OUT_CSV = Path(__file__).resolve().parent / "student_mastery.csv"

def load_students_grade6():
    with open(STUDENTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Keep only year 2023-2024 and class starting with "6/"
    students = {}
    for row in data:
        try:
            if str(row.get("year")) != "2023-2024":
                continue
            cl = str(row.get("class",""))
            if not cl.startswith("6/"):
                continue
            sid = str(row.get("student_id"))
            cn = float(row.get("cn", 0.0))
            students[sid] = cn
        except Exception:
            continue
    return students

def load_skill_ids():
    ids = []
    if not SKILLS_CSV.exists():
        return ids
    with open(SKILLS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            ids.append(r["skillId"])
    return ids

def main():
    students = load_students_grade6()
    skills = load_skill_ids()
    today = date.today().isoformat()

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["studentId","skillId","score","lastUpdated"])
        writer.writeheader()
        for sid, cn in students.items():
            score = round(min(max(cn / 10.0, 0.0), 1.0), 3)
            for skill in skills:
                writer.writerow({"studentId": sid, "skillId": skill, "score": score, "lastUpdated": today})

    print(f"Wrote {OUT_CSV} for {len(students)} students x {len(skills)} skills")

if __name__ == "__main__":
    main()


from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True, parents=True)

PREFIXES = """@prefix ex:  <https://example.org/kg/> .
@prefix edu: <https://example.org/edu#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""

def iri(kind: str, ident: str) -> str:
    ident = str(ident).strip().replace(" ", "_")
    # Use full IRI instead of prefix with / to avoid parse errors
    return f"<https://example.org/kg/{kind}/{ident}>"

def write_file(path: Path, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {path}")

def read_csv(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def export_skills():
    path = ROOT / "skills.csv"
    if not path.exists():
        return ""
    triples = [PREFIXES]
    for r in read_csv(path):
        sid = r["skillId"]
        triples.append(
            f"{iri('skill', sid)} a edu:Skill ; "
            f' edu:skillId "{sid}" ; '
            f' edu:name "{r.get("name","")}" ; '
            f' edu:grade "{r.get("grade","6")}"^^xsd:int .\n'
        )
    return "".join(triples)

def export_resources():
    path = ROOT / "resources.csv"
    if not path.exists():
        return ""
    triples = [PREFIXES]
    for r in read_csv(path):
        rid = r["resId"]
        triples.append(
            f"{iri('resource', rid)} a edu:Resource ; "
            f' edu:resId "{rid}" ; '
            f' edu:title "{r.get("title","")}" ; '
            f' edu:mediaType "{r.get("mediaType","")}" ; '
            f' edu:url "{r.get("url","")}" ; '
            f' edu:grade "{r.get("grade","6")}"^^xsd:int .\n'
        )
    return "".join(triples)

def export_resource_skill():
    rpath = ROOT / "resource_skill.csv"
    if not rpath.exists():
        return ""
    triples = [PREFIXES]
    for r in read_csv(rpath):
        rid = r["resId"]
        sid = r["skillId"]
        cov = r.get("coverage", "1.0")
        # event node to carry coverage value
        ev = f"cover_{rid}_{sid}".replace(" ", "_")
        triples.append(
            f"{iri('cover', ev)} a edu:Coverage ; "
            f" edu:resource {iri('resource', rid)} ; "
            f" edu:skill {iri('skill', sid)} ; "
            f' edu:coverage "{cov}"^^xsd:decimal .\n'
        )
    return "".join(triples)

def export_prerequisites():
    path = ROOT / "prerequisites.csv"
    if not path.exists():
        return ""
    triples = [PREFIXES]
    for r in read_csv(path):
        src = r["fromSkillId"]
        dst = r["toSkillId"]
        triples.append(f"{iri('skill', src)} edu:prerequisiteOf {iri('skill', dst)} .\n")
    return "".join(triples)

def export_question_skill():
    path = ROOT / "question_skill.csv"
    if not path.exists():
        return ""
    triples = [PREFIXES]
    for r in read_csv(path):
        q = r["q_id"]
        s = r["skillId"]
        triples.append(
            f"{iri('question', q)} a edu:Question ; edu:qId \"{q}\" .\n"
            f"{iri('question', q)} edu:measures {iri('skill', s)} .\n"
        )
    return "".join(triples)

def export_students():
    # optional: we do not parse the huge JSON here; rely on student_mastery.csv to create students
    path = ROOT / "student_mastery.csv"
    if not path.exists():
        return ""
    triples = [PREFIXES]
    seen = set()
    for r in read_csv(path):
        sid = r["studentId"]
        if sid in seen:
            continue
        seen.add(sid)
        triples.append(f"{iri('student', sid)} a edu:Student ; edu:studentId \"{sid}\" .\n")
    return "".join(triples)

def export_mastery():
    path = ROOT / "student_mastery.csv"
    if not path.exists():
        return ""
    triples = [PREFIXES]
    for r in read_csv(path):
        sid = r["studentId"]
        skill = r["skillId"]
        score = r.get("score", "0.0")
        dt = r.get("lastUpdated", "")
        ev = f"mastery_{sid}_{skill}".replace(" ", "_")
        if dt:
            triples.append(
                f"{iri('mastery', ev)} a edu:Mastery ; "
                f" edu:student {iri('student', sid)} ; "
                f" edu:skill {iri('skill', skill)} ; "
                f' edu:score "{score}"^^xsd:decimal ; '
                f' edu:lastUpdated "{dt}"^^xsd:date .\n'
            )
        else:
            triples.append(
                f"{iri('mastery', ev)} a edu:Mastery ; "
                f" edu:student {iri('student', sid)} ; "
                f" edu:skill {iri('skill', skill)} ; "
                f' edu:score "{score}"^^xsd:decimal .\n'
            )
    return "".join(triples)

def main():
    files = {
        "skills.ttl": export_skills(),
        "resources.ttl": export_resources(),
        "resource_skill.ttl": export_resource_skill(),
        "prerequisites.ttl": export_prerequisites(),
        "question_skill.ttl": export_question_skill(),
        "students.ttl": export_students(),
        "mastery.ttl": export_mastery(),
    }
    for name, content in files.items():
        if content:
            write_file(OUT / name, content)

if __name__ == "__main__":
    main()


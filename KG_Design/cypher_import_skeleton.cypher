// Load files from Neo4j import directory. Copy CSVs there or use absolute URLs.

CREATE CONSTRAINT IF NOT EXISTS FOR (s:Student) REQUIRE s.studentId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (k:Skill)   REQUIRE k.skillId   IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (r:Resource) REQUIRE r.resId     IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (a:Assessment) REQUIRE a.assessId IS UNIQUE;

// Skills
LOAD CSV WITH HEADERS FROM 'file:///skills.csv' AS row
MERGE (k:Skill {skillId: row.skillId})
SET   k += {name: row.name, domain: row.domain, bloomLevel: row.bloomLevel, grade: toInteger(row.grade), description: row.description};

// Resources
LOAD CSV WITH HEADERS FROM 'file:///resources.csv' AS row
MERGE (r:Resource {resId: row.resId})
SET   r += {title: row.title, mediaType: row.mediaType, url: row.url, difficulty: toInteger(row.difficulty), duration: toInteger(row.duration), grade: toInteger(row.grade)};

// Resource → Skill
LOAD CSV WITH HEADERS FROM 'file:///resource_skill.csv' AS row
MATCH (r:Resource {resId: row.resId}), (k:Skill {skillId: row.skillId})
MERGE (r)-[c:COVERS]->(k)
SET c.coverage = toFloat(row.coverage);

// Skill prerequisites
LOAD CSV WITH HEADERS FROM 'file:///prerequisites.csv' AS row
MATCH (p:Skill {skillId: row.fromSkillId}), (q:Skill {skillId: row.toSkillId})
MERGE (p)-[:PREREQUISITE_OF]->(q);

// Assessments (optional)
LOAD CSV WITH HEADERS FROM 'file:///assessments.csv' AS row
MERGE (a:Assessment {assessId: row.assessId})
SET   a += {name: row.name, date: date(row.date), grade: toInteger(row.grade), type: row.type, maxScore: toInteger(row.maxScore)};

// Question mapping (optional)
LOAD CSV WITH HEADERS FROM 'file:///questions_in_assessment.csv' AS row
MATCH (a:Assessment {assessId: row.assessId})
MERGE (q:Question {q_id: row.q_id})
MERGE (a)-[r:CONTAINS]->(q)
SET r.weight = coalesce(toFloat(row.weight),1.0);

LOAD CSV WITH HEADERS FROM 'file:///question_skill.csv' AS row
MATCH (q:Question {q_id: row.q_id}), (k:Skill {skillId: row.skillId})
MERGE (q)-[:MEASURES]->(k);

// Student performance (optional)
LOAD CSV WITH HEADERS FROM 'file:///student_assessment.csv' AS row
MERGE (s:Student {studentId: row.studentId})
WITH s, row
MATCH (a:Assessment {assessId: row.assessId})
MERGE (s)-[t:TOOK]->(a)
SET t.score = toFloat(row.score), t.date = date(row.date);

// Derive mastery per skill (simple baseline)
MATCH (s:Student)-[:TOOK]->(a:Assessment)-[:CONTAINS]->(q:Question)-[:MEASURES]->(k:Skill)
WITH s,k,avg(coalesce(a.maxScore,10.0) * 0 + 10.0 * 0 + 1.0) AS dummy, avg(coalesce(t.score,0.0)) AS score // placeholder
MERGE (s)-[m:MASTERY]->(k)
SET m.score = coalesce(score,0.0), m.lastUpdated = date();


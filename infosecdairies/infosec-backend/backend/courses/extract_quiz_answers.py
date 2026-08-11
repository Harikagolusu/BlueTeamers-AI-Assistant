"""
One-shot extraction script.
Run from repo root:  python infosec-backend/backend/courses/extract_quiz_answers.py
Reads src/data/quizData.ts and writes quiz_answers.py beside this file.
"""
import re, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
_TS   = os.path.join(_REPO, "src", "data", "quizData.ts")
_OUT  = os.path.join(_HERE, "quiz_answers.py")

with open(_TS, encoding="utf-8") as f:
    content = f.read()

# Split on quiz-object boundaries (each starts with { quizId: )
quiz_blocks = re.split(r'(?=\{\s*\n?\s*quizId:)', content)

results = {}  # (course_id, quiz_id) -> {question_id: correct_answer_index}

for block in quiz_blocks:
    cid_m = re.search(r'courseId:\s*"([^"]+)"', block)
    qid_m = re.search(r'quizId:\s*"([^"]+)"', block)
    if not cid_m or not qid_m:
        continue
    course_id = cid_m.group(1)
    quiz_id   = qid_m.group(1)
    questions: dict[str, int] = {}
    # Robust braces-matching question extractor
    pos = 0
    while True:
        q_start_m = re.search(r'\{\s*id:\s*"([^"]+)"', block[pos:])
        if not q_start_m:
            break
        q_id = q_start_m.group(1)
        start_q = pos + q_start_m.start()
        brace_count = 0
        end_q = start_q
        for i in range(start_q, len(block)):
            if block[i] == '{':
                brace_count += 1
            elif block[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_q = i + 1
                    break
        q_text = block[start_q:end_q]
        ans_m = re.search(r'correctAnswer:\s*(\d+)', q_text)
        if ans_m:
            questions[q_id] = int(ans_m.group(1))
        pos = end_q

    if questions:
        results[(course_id, quiz_id)] = questions

lines = [
    "# AUTO-GENERATED from quizData.ts — do not edit manually.",
    "# Re-run extract_quiz_answers.py after updating quizData.ts.",
    "# Mapping: (course_id, quiz_id) -> {question_id: correct_answer_index}",
    "QUIZ_CORRECT_ANSWERS: dict[tuple[str, str], dict[str, int]] = {",
]
for (cid, qid), qs in sorted(results.items()):
    lines.append(f'    ("{cid}", "{qid}"): {{')
    for question_id, ans in qs.items():
        lines.append(f'        "{question_id}": {ans},')
    lines.append("    },")
lines.append("}")

with open(_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {len(results)} quiz answer sets ({sum(len(v) for v in results.values())} questions) -> {_OUT}")

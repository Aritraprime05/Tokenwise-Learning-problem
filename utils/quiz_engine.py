def grade_quiz(questions: list[dict], answers: dict) -> dict:
    correct = []
    incorrect = []
    for i, question in enumerate(questions):
        selected = answers.get(str(i))
        record = {"question": question["question"], "selected": selected,
                  "correct_answer": question["options"][question["answer"]],
                  "explanation": question["explanation"]}
        (correct if selected == question["answer"] else incorrect).append(record)
    total = len(questions)
    return {"score": len(correct), "total": total,
            "percentage": round(100 * len(correct) / total) if total else 0,
            "correct": correct, "incorrect": incorrect}

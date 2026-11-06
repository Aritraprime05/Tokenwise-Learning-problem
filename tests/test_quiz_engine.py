from utils.quiz_engine import grade_quiz

QUESTIONS = [
 {"question":"Q1","options":["A","B"],"answer":1,"explanation":"Because B"},
 {"question":"Q2","options":["C","D"],"answer":0,"explanation":"Because C"}
]

def test_quiz_score():
    result = grade_quiz(QUESTIONS,{"0":1,"1":1})
    assert result["score"] == 1
    assert result["total"] == 2
    assert result["percentage"] == 50
    assert len(result["incorrect"]) == 1

def test_unanswered_are_incorrect():
    result = grade_quiz(QUESTIONS,{})
    assert result["score"] == 0
    assert result["percentage"] == 0

def test_empty_quiz():
    assert grade_quiz([],{})["percentage"] == 0

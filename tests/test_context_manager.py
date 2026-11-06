import pytest
from utils.context_manager import calculate_budget, assess_prompt

def test_budget_fits():
    b = calculate_budget(100,10,20,30,20)
    assert b.input_tokens == 60
    assert b.remaining == 20
    assert b.fits

def test_budget_overflow():
    b = calculate_budget(100,40,30,20,20)
    assert b.remaining == -10
    assert not b.fits

def test_invalid_negative():
    with pytest.raises(ValueError):
        calculate_budget(100,-1,0,0,0)

def test_output_cannot_exceed_window():
    with pytest.raises(ValueError):
        calculate_budget(100,0,0,0,101)

def test_prompt_assessment_checks_fit_and_coverage():
    result = assess_prompt("Explain photosynthesis with sunlight and oxygen",8,10,
                           ["photosynthesis","sunlight","oxygen","glucose"])
    assert result["passed"]
    assert result["coverage"] == .75

def test_prompt_assessment_fails_if_over_budget():
    result = assess_prompt("Explain photosynthesis sunlight oxygen",12,10,
                           ["photosynthesis","sunlight","oxygen"])
    assert not result["passed"]

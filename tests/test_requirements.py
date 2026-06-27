# tests/test_requirements.py
from app.agents.prompt_refiner import PromptRefinerAgent
from app.agents.requirements_agent import RequirementsAgent


def test_extracts_quoted_name_and_dimensions():
    text = 'Make a mirror hanger with name "Hamad" width 90mm height 50mm thickness 4mm'
    refined = PromptRefinerAgent().run(text, "en")
    req = RequirementsAgent().run(text, refined, "PLA")
    assert req.hanger.text.content == "Hamad"
    assert req.hanger.width_mm == 90
    assert req.hanger.height_mm == 50

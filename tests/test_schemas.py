import pytest
from pydantic import ValidationError

from app.schemas import PresentationPlan


def test_valid_presentation_plan() -> None:
    plan = PresentationPlan.model_validate(
        {
            "title": "Minha apresentação",
            "audience": "Alunos",
            "objective": "Ensinar",
            "slides": [
                {
                    "type": "bullets",
                    "title": "Slide 1",
                    "bullets": ["Ponto 1"],
                    "speaker_notes": "Fale sobre ponto 1",
                }
            ],
        }
    )
    assert len(plan.slides) == 1


def test_invalid_without_slides() -> None:
    with pytest.raises(ValidationError):
        PresentationPlan.model_validate(
            {"title": "t", "audience": "a", "objective": "o", "slides": []}
        )

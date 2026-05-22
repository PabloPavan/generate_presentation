from app.agent import generate_presentation_plan


def test_mock_generation(monkeypatch) -> None:
    monkeypatch.setenv("PRESENTATION_AGENT_MOCK", "1")
    plan = generate_presentation_plan("texto", "alunos", "objetivo", 5)
    assert plan.title
    assert plan.slides

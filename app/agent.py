from __future__ import annotations

import json
from pathlib import Path

from app.config import get_settings
from app.exceptions import AgentGenerationError
from app.schemas import PresentationPlan

PLANNER_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "slide_planner.md"
REVIEWER_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "slide_reviewer.md"


def _load_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _mock_plan(audience: str, objective: str) -> PresentationPlan:
    return PresentationPlan.model_validate(
        {
            "title": "Apresentação Gerada em Mock",
            "subtitle": "Fluxo PDF para PPTX",
            "audience": audience,
            "objective": objective,
            "slides": [
                {
                    "type": "title",
                    "title": "Apresentação do Conteúdo",
                    "subtitle": "Resumo executivo",
                    "speaker_notes": "Introduza o tema e o contexto geral.",
                },
                {
                    "type": "agenda",
                    "title": "Agenda",
                    "bullets": ["Contexto", "Pontos principais", "Conclusões"],
                    "speaker_notes": "Explique o roteiro que será seguido.",
                },
                {
                    "type": "conclusion",
                    "title": "Conclusão",
                    "bullets": ["Recapitulação", "Próximos passos"],
                    "speaker_notes": "Finalize com próximos passos claros.",
                },
            ],
        }
    )


def generate_presentation_plan(
    pdf_text: str,
    audience: str,
    objective: str,
    slide_count: int = 12,
    review_pass: bool = True,
) -> PresentationPlan:
    settings = get_settings()
    if settings.mock_mode:
        return _mock_plan(audience=audience, objective=objective)

    if not settings.openai_api_key:
        raise AgentGenerationError("OPENAI_API_KEY is required when mock mode is disabled.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise AgentGenerationError("OpenAI SDK is not installed. Run: pip install -e .") from exc

    planner_prompt = _load_prompt(PLANNER_PROMPT_PATH).format(
        audience=audience,
        objective=objective,
        slide_count=slide_count,
        pdf_text=pdf_text,
    )

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.responses.parse(
            model=settings.openai_model,
            input=[{"role": "user", "content": planner_prompt}],
            text_format=PresentationPlan,
        )
        plan = response.output_parsed

        if not review_pass:
            return plan

        reviewer_prompt = _load_prompt(REVIEWER_PROMPT_PATH).format(
            audience=audience,
            objective=objective,
            pdf_text=pdf_text,
            initial_plan_json=json.dumps(
                plan.model_dump(mode="json"), ensure_ascii=False, indent=2
            ),
        )
        review_response = client.responses.parse(
            model=settings.openai_model,
            input=[{"role": "user", "content": reviewer_prompt}],
            text_format=PresentationPlan,
        )
        return review_response.output_parsed
    except Exception as exc:  # noqa: BLE001
        raise AgentGenerationError(f"Failed to generate presentation plan: {exc}") from exc

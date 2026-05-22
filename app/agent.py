from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.exceptions import AgentGenerationError
from app.schemas import PresentationPlan

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "slide_planner.md"


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


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

    prompt = _load_prompt().format(
        audience=audience,
        objective=objective,
        slide_count=slide_count,
        pdf_text=pdf_text,
    )

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.responses.parse(
            model=settings.openai_model,
            input=[{"role": "user", "content": prompt}],
            text_format=PresentationPlan,
        )
        return response.output_parsed
    except Exception as exc:  # noqa: BLE001
        raise AgentGenerationError(f"Failed to generate presentation plan: {exc}") from exc

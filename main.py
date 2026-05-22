from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate PPTX presentations from PDF content.")
    parser.add_argument("--pdf", required=True, help="Path to source PDF file")
    parser.add_argument("--output", default="outputs/presentation.pptx", help="Output PPTX path")
    parser.add_argument("--audience", default="alunos de graduação")
    parser.add_argument(
        "--objective",
        default="transformar o conteúdo do PDF em uma apresentação didática",
    )
    parser.add_argument("--slides", type=int, default=12)
    parser.add_argument("--template", default=None)
    parser.add_argument("--save-json", dest="save_json", action="store_true", default=True)
    parser.add_argument("--no-save-json", dest="save_json", action="store_false")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        from app.agent import generate_presentation_plan
        from app.pdf_reader import extract_text_from_pdf
        from app.pptx_renderer import render_pptx

        pdf_text = extract_text_from_pdf(args.pdf)
        plan = generate_presentation_plan(
            pdf_text=pdf_text,
            audience=args.audience,
            objective=args.objective,
            slide_count=args.slides,
        )

        output_path = Path(args.output)
        if args.save_json:
            json_path = output_path.with_suffix(".json")
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(
                json.dumps(plan.model_dump(mode="json"), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"Plano JSON salvo em: {json_path}")

        render_pptx(plan=plan, output_path=output_path, template_path=args.template)
        print(f"Apresentação PPTX salva em: {output_path}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

# presentation-agent

Ferramenta para gerar apresentações PPTX com notas do apresentador a partir de PDFs.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Configuração

Crie `.env`:

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.5
```

## Rodar com mock

```bash
PRESENTATION_AGENT_MOCK=1 python main.py --pdf inputs/teste.pdf
```

## Rodar com IA

```bash
python main.py \
  --pdf inputs/aula.pdf \
  --output outputs/aula.pptx \
  --audience "alunos de Ciência da Computação" \
  --objective "criar uma apresentação didática" \
  --slides 20
```

## Saídas

- `.json` com o plano estruturado
- `.pptx` com a apresentação

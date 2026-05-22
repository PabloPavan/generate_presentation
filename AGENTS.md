# AGENTS.md

## Projeto

Este projeto é uma ferramenta Python chamada `presentation-agent`.

Ela recebe um PDF, extrai texto, chama uma IA para gerar um plano de apresentação em JSON e renderiza um arquivo PPTX com notas do apresentador.

## Regras técnicas

- Usar Python 3.12+.
- Usar Pydantic para schemas.
- Usar PyMuPDF para extração de texto.
- Usar python-pptx para geração de PowerPoint.
- Usar OpenAI SDK para chamada da IA.
- Não acoplar a lógica principal ao Canva no MVP.
- Separar claramente:
  - extração de PDF
  - chamada da IA
  - schema dos slides
  - geração do PPTX
  - CLI
- Toda saída estruturada da IA deve ser validada por Pydantic.
- Não gerar slides diretamente a partir de texto solto.
- Sempre passar por um JSON intermediário.

## Padrões de código

- Código simples e explícito.
- Funções pequenas.
- Type hints em tudo.
- Erros tratados com mensagens claras.
- Evitar dependências desnecessárias.
- Não usar notebooks.
- Não hardcodar API keys.
- Configuração via `.env`.

## Critérios de qualidade

Antes de concluir uma tarefa:

- Rodar testes.
- Rodar lint.
- Verificar se o CLI executa.
- Garantir que o PPTX gerado abre no PowerPoint/LibreOffice.

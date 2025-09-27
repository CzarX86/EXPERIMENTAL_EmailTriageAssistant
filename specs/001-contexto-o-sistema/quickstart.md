# Quickstart — Assistente de E-mails (Phase 1)

Este guia demonstra o fluxo principal em ambiente local (CLI-first). Ajuste parâmetros conforme suas contas e arquivos.

1) Preparação
- Instale dependências (Poetry) e configure Tesseract localmente
- Configure acesso M365 (Device Code Flow) ou IMAP conforme necessário

2) Ingestão
- Ingerir de M365 ou IMAP, ou importar mbox local

3) Indexação e Classificação
- Gerar embeddings e construir índice FAISS
- Classificar mensagens e priorizar urgentes

4) Sugestões e Revisão
- Gerar sugestões
- Aprovar/corrigir pelo CLI ou painel

5) Busca e Explicabilidade
- Buscar por similaridade
- Ver explicação (fatores, similares, influência de feedback)

6) Exportação/Importação (sem sincronização automática)
- Exportar bundle criptografado
- Importar bundle em outra máquina mediante confirmação

Notas
- Nenhum dado é enviado para fora sem consentimento explícito
- API local opera em loopback com token no Keychain
- OCR pesado roda em background com retries e modo seguro para arquivos grandes

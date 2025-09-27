<!--
Sync Impact Report
Version change: 2.3.0 → 2.4.0
Modified principles: None
Added sections: Modo de Execução e Autenticação da API Local (detalhe dentro de Stack)
Removed sections: None
Stack changes:
  - Python: 3.12 → 3.11 (compat-first); revisão futura planejada para 3.12
  - UI: Tauri confirmado como padrão; Electron mantido como fallback
Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (stack gate updated; version reference bumped)
	- ✅ .specify/templates/spec-template.md (reviewed, no change)
	- ✅ .specify/templates/tasks-template.md (reviewed, no change)
	- ⚠ .specify/templates/commands/* (directory not present)
	- ✅ README/docs (none present)
Follow-up TODOs: None
-->

# Assistente Inteligente de E-mails com Revisão Supervisionada Constitution

## Propósito
Reduzir a sobrecarga de e-mails de forma prática e personalizada, organizando,
classificando e sugerindo ações com supervisão humana contínua e aprendizado
incremental a partir do feedback do usuário.

## Core Principles

### I. Não Envio Automático de Mensagens
Não enviar mensagens automáticas sem aprovação explícita. Todas as ações de envio devem ser revisadas e aprovadas pelo usuário para garantir controle humano.

### II. Assistente de Apoio
Atuar apenas como assistente de apoio, nunca de forma autônoma. O sistema deve sempre requerer intervenção humana para ações críticas.

### III. Aprendizado Incremental
Aprendizado incremental com base no feedback do usuário. O assistente deve melhorar progressivamente através de correções e feedbacks fornecidos.

### IV. Evolução Contínua
Evoluir continuamente sem perda de histórico. Manter todo o aprendizado e dados acumulados ao longo do tempo.

### V. Interface Clara
Interface clara, objetiva e não intrusiva. A interação com o usuário deve ser simples, direta e não disruptiva.

### VI. Segurança e Privacidade por Padrão
Proteger dados por padrão (privacy-by-default). O sistema DEVE operar local-first, minimizar coleta,
evitar vazamento de dados e NUNCA enviar informações para serviços externos sem consentimento explícito.
Criptografia em repouso e em trânsito, controles de acesso no dispositivo e limpeza segura de dados
temporários SÃO obrigatórios.

## Escopo
- Processar e-mails recebidos, detectando spam e classificando prioridades (urgente, ação, responder, ignorar).
- Sugerir respostas com base em contexto e histórico.
- Aprender progressivamente com feedback.
- Manter base de conhecimento vetorial (conteúdo e anexos).
- Realizar OCR, versionamento e vetorização de anexos.
- Suportar busca semântica contextual.
- Utilizar histórico e threads para inferir urgência.
- Permitir correções pontuais via linguagem natural ou painel de configuração.
- Suportar múltiplos dispositivos sem perda de histórico.

## Critérios de Sucesso
- Acompanhar e melhorar progressivamente a precisão da classificação de e-mails.

## Tecnologia e Stack Inicial
- Linguagem e Runtime: Python 3.11 (local-first, multiplataforma)
	- Revisão planejada para Python 3.12 após verificação de wheels (FAISS/SQLCipher/Tesseract)
- Núcleo de Aplicação: Flask (API local minimalista) + Typer (CLI)
- Integrações de E-mail: Microsoft Graph API (msal, msgraph-core) para M365;
	IMAP (imapclient) para caixas não-365; importação local de mbox quando aplicável
- Armazenamento Local: SQLite com SQLCipher para metadados/índices; anexos em
	sistema de arquivos criptografado; tokens/segredos no macOS Keychain
- Vetorização e Busca: FAISS (índice local); embeddings
	sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- Classificação e Aprendizado: scikit-learn (LogReg/SVM com partial_fit);
	joblib para persistência incremental
- OCR e Parsing: Tesseract (pytesseract) para imagens; pypdf e python-docx;
	biblioteca unstructured para parsing local de documentos comuns
- Segurança: Privacy-by-default; MSAL Device Code Flow; criptografia em repouso
	(SQLCipher) e em trânsito (HTTPS local opcional); zero compartilhamento
	externo sem consentimento explícito
- Observabilidade: logging estruturado (Python logging em JSON)
- Testes: pytest + coverage
- UI: Tauri (padrão) para app desktop nativo; Electron como fallback. Painel web leve com Jinja/HTMX é opcional
- Empacotamento: Poetry para gestão de dependências e scripts
- Plataformas: macOS (prioridade)

### Modo de Execução e Autenticação da API Local
- CLI-first: comandos Typer para ingestão/classificação/indexação/sugestões; `serve` expõe a API local.
- Headless (opt-in): execução em background via macOS LaunchAgent com consentimento do usuário.
- Autenticação API local: loopback-only + Bearer Token aleatório no Keychain; CORS desativado por padrão ou restrito a loopback;
	proteção CSRF quando houver UI web; nunca registrar tokens/segredos em logs.

## Fora de Escopo
- Enviar mensagens em lote sem supervisão.
- Atuar de forma autônoma sem revisão do usuário.
- Mensurar tempo de resposta ou produtividade em KPIs rígidos.
- Questões de LGPD/GDPR, dado que é uso pessoal e dados não saem do ambiente local.

## Governance
A constituição é o documento supremo do projeto. Emendas requerem aprovação unânime dos desenvolvedores principais e documentação completa das mudanças. Versões seguem semântica: MAJOR para mudanças incompatíveis nos princípios, MINOR para adições de princípios ou seções, PATCH para clarificações ou correções. Todas as mudanças no código devem verificar conformidade com os princípios através de revisões manuais e testes. Exceções ao stack aprovado DEVEM ser justificadas (segurança/privacidade/performance) e revisadas.

**Version**: 2.4.0 | **Ratified**: 2025-09-27 | **Last Amended**: 2025-09-27
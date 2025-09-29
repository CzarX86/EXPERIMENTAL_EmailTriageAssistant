# Tasks: Assistente de E-mails com Classificação e S- [x] T018: Implementar modelo `Email` com campos básicos, metadados e relacionamentos- [x] T019: Implementar modelo `Attachment` com suporte OCR e validação- [x] T020: Implementar modelo `Thread` para agrupamento de conversas- [x] T021: Implementar modelo `Classification` com labels e scores- [x] T022: Implementar modelo `Suggestion` para respostas automáticas- [x] T023: Implementar modelo `Feedback` para aprendizado incremental- [x] T024: Implementar modelo `Explanation` para transparência das decisões- [x] T025: Implementar modelo `SemanticIndexEntry` para busca vetorial- [x] T026: Implementar modelo `ModelState` para versionamento de ML- [x] T027: Implementar modelo `RetentionPolicy` para gestão de dados- [x] T028: Implementar modelo `ProcessingJob` para processamento assíncronopervisionadas

**Input**: Design docs from `/specs/001-contexto-o-sistema/`  
Feature dir: `/Users/juliocezar/Dev/work/EXPERIMENTAL_EmailTriageAssistant/specs/001-contexto-o-sistema`  
Context for generation: (no additional arguments)

## Execution Flow (main)
```
1) Load plan.md (stack, structure) → done
2) Load optional docs → research.md, data-model.md, contracts/, quickstart.md → done
3) Generate tasks by category (Setup → Tests → Core → Integration → Polish)
4) Apply task rules (TDD, parallel markers, same-file sequential)
5) Number tasks (T001...)
6) Add dependency graph and parallel examples
7) Validate completeness (entities, contracts, endpoints, stories) → done
```

## Format: `[ID] [P?] Description`
- [P] means the task can run in parallel (different files, no dependencies)
- All paths are absolute or repo-root relative as noted

---

## Phase 3.1: Setup
- [x] T001 Create project structure per plan (repo root): `src/{cli,services,models,lib}`, `tests/{unit,integration,contract}`
- [x] T002 Initialize Poetry project (repo root) with dependencies (Flask, Typer, faiss-cpu, sentence-transformers, scikit-learn, joblib, pytesseract, pypdf, python-docx, unstructured, msal, msgraph-core, imapclient, pysqlcipher3, python-dotenv); add dev deps (pytest, coverage, ruff)
- [x] T003 [P] Configure tooling: ruff (pyproject.toml), pytest.ini, coverage config, basic logging in JSON (src/lib/logging.py)

## Phase 3.2: Tests First (TDD) — MUST FAIL BEFORE IMPLEMENTATION
### Contract tests (from OpenAPI in `contracts/openapi.yaml`)
- [x] T004 [P] Contract test GET /health in `tests/contract/test_health.py`
- [x] T005 [P] Contract test POST /ingest in `tests/contract/test_ingest.py`
- [x] T006 [P] Contract test POST /index in `tests/contract/test_index.py`
- [x] T007 [P] Contract test POST /classify/{email_id} in `tests/contract/test_classify.py`
- [x] T008 [P] Contract test POST /suggest/{email_id} in `tests/contract/test_suggest.py`
- [x] T009 [P] Contract test GET /explain/{email_id} in `tests/contract/test_explain.py`
- [x] T010 [P] Contract test GET /search in `tests/contract/test_search.py`
- [x] T011 [P] Contract test POST /feedback in `tests/contract/test_feedback.py`
- [x] T012 [P] Contract test POST /export in `tests/contract/test_export.py`
- [x] T013 [P] Contract test POST /import in `tests/contract/test_import.py`
 - [x] T013a [P] Security contract tests: loopback-only enforcement and Bearer token required (401/403 cases) in `tests/contract/test_security.py`
 - [ ] T010a [P] Security & privacy tests (FR-012): encryption-at-rest (SQLCipher key required), wrong key rejection, and no-secret-logging assertions in `tests/integration/test_security_privacy_storage.py`

### Integration tests (from User Scenarios in spec)
- [x] T014 [P] Integration: ingest→classify→suggest happy-path (Story 1) in `tests/integration/test_flow_ingest_classify_suggest.py`
- [x] T015 [P] Integration: OCR on image/PDF used in suggestion context (Story 2) in `tests/integration/test_ocr_pdf_flow.py`
- [x] T016 [P] Integration: feedback improves future suggestions (Story 3) in `tests/integration/test_feedback_learning.py`
- [x] T017 [P] Integration: semantic search relevance (Story 4) in `tests/integration/test_semantic_search.py`
 - [x] T017a [P] Integration: multilingual detection and suggestion language preference override in `tests/integration/test_multilang.py`

## Phase 3.3: Core Implementation
### Models (from `data-model.md`) — different files so can run in parallel
- [x] T018 [P] Email model in `src/models/email.py`
- [x] T019 [P] Attachment model in `src/models/attachment.py`
- [x] T020 [P] Thread model in `src/models/thread.py`
- [x] T021 [P] Classification model in `src/models/classification.py`
- [x] T022 [P] Suggestion model in `src/models/suggestion.py`
- [x] T023 [P] Feedback model in `src/models/feedback.py`
- [x] T024 [P] Explanation model in `src/models/explanation.py`
- [x] T025 [P] SemanticIndexEntry model in `src/models/semantic_index.py`
- [x] T026 [P] ModelState model in `src/models/model_state.py`
- [x] T027 [P] RetentionPolicy model in `src/models/retention_policy.py`
- [x] T028 [P] ProcessingJob model in `src/models/processing_job.py`

### Core services and utilities (grouped to stay focused)
- [ ] T029 Storage layer: SQLite + SQLCipher connection helper and migrations stub in `src/lib/storage.py` (and `src/lib/migrations.py`)
- [ ] T030 Embeddings + FAISS utilities in `src/lib/embeddings.py` and `src/lib/index_store.py`
- [ ] T031 OCR/Parsing + Language detection in `src/lib/ocr.py` and `src/lib/lang.py` (MiniLM autodetect policy)
- [ ] T032 IngestionService (M365, IMAP, mbox import stubs) in `src/services/ingestion.py`
- [ ] T033 Core ML services: IndexService + ClassifierService with incremental learning in `src/services/indexing.py` and `src/services/classifier.py`
- [ ] T034 Suggestions/Explainability/Search services in `src/services/suggestions.py`, `src/services/explain.py`, `src/services/search.py`
- [ ] T035 Retention/ExportImport/Jobs (retry queue + chunked safe-mode) in `src/services/retention.py`, `src/services/transfer.py`, `src/services/jobs.py`
 - [ ] T035a Metrics module: collect and persist local metrics (accuracy, urgent precision/recall, suggestion acceptance) in `src/lib/metrics.py` and expose via CLI/API

### API (Flask) — endpoints must match OpenAPI
- [ ] T036 Flask app bootstrap + auth middleware (loopback-only + Keychain token) in `src/services/api.py`
- [ ] T037 Implement GET /health in `src/services/api.py`
- [ ] T038 Implement POST /ingest in `src/services/api.py`
- [ ] T039 Implement POST /index in `src/services/api.py`
- [ ] T040 Implement POST /classify/{email_id} in `src/services/api.py`
- [ ] T041 Implement POST /suggest/{email_id} in `src/services/api.py`
- [ ] T042 Implement GET /explain/{email_id} in `src/services/api.py`
- [ ] T043 Implement GET /search in `src/services/api.py`
- [ ] T044 Implement POST /feedback in `src/services/api.py`
- [ ] T045 Implement POST /export in `src/services/api.py`
- [ ] T046 Implement POST /import in `src/services/api.py`
 - [ ] T046a Ensure API security behaviors: loopback-only host check, Bearer token auth; add negative-path handling (401/403) with no secret logging

## Phase 3.4: Integration
- [ ] T047 Wire services to storage/index; enable JSON logging across app; configure MSAL/IMAP client adapters in `src/lib/` and inject into services
- [ ] T048 Implement FR-019 failure handling (retry queue, backoff, safe mode, needs_attention flagging) across OCR/parsing and ingestion flows
 - [ ] T048a Tests for FR-019: backoff schedule, retry limits by size/type, safe-mode chunking on large files, and needs_attention flagging in `tests/integration/test_failures_retry_safe_mode.py`

## Phase 3.5: Polish
- [ ] T049 [P] Unit tests: urgency rule (FR-010), retention policy (FR-014), explainability content (FR-018) in `tests/unit/test_rules.py`
- [ ] T050 [P] Performance smoke: initial indexing on sample corpus (<5 min) in `tests/integration/test_perf_smoke.py`
- [ ] T051 [P] Docs: refine `quickstart.md` with concrete commands and add API notes referencing `contracts/openapi.yaml`
- [ ] T052 Final QA: run Quickstart end-to-end locally; checklist and fixups in `docs/manual-testing.md` (create file)
 - [ ] T053 [P] CLI corrections (FR-008): approve/reject/correct flows with unit and integration tests in `tests/unit/test_cli_corrections.py` and `tests/integration/test_cli_corrections_flow.py`; implement commands in `src/cli/corrections.py`
 - [ ] T054 [P] Metrics/reporting (FR-013): CLI `report` command to display local metrics; tests in `tests/unit/test_metrics.py` and `tests/integration/test_metrics_report.py`; implement in `src/cli/report.py`

---

## Dependencies
- T001 → T002 → T003 (tooling after init)
- Tests first: T004–T017 must be created and failing before implementing T018+
- Models (T018–T028) unblock services (T029–T035)
- Services (T029–T035) unblock API endpoints (T036–T046)
- Integration (T047–T048) after endpoints
- Polish (T049–T052) last

## Parallel Execution Examples
```
# Launch all contract tests scaffolding in parallel (different files):
Task: "T004 Contract test GET /health in tests/contract/test_health.py"
Task: "T005 Contract test POST /ingest in tests/contract/test_ingest.py"
Task: "T006 Contract test POST /index in tests/contract/test_index.py"
Task: "T007 Contract test POST /classify/{email_id} in tests/contract/test_classify.py"
Task: "T008 Contract test POST /suggest/{email_id} in tests/contract/test_suggest.py"
Task: "T009 Contract test GET /explain/{email_id} in tests/contract/test_explain.py"
Task: "T010 Contract test GET /search in tests/contract/test_search.py"
Task: "T011 Contract test POST /feedback in tests/contract/test_feedback.py"
Task: "T012 Contract test POST /export in tests/contract/test_export.py"
Task: "T013 Contract test POST /import in tests/contract/test_import.py"

# Launch model definitions in parallel (one file per entity):
Task: "T018 Email model in src/models/email.py"
Task: "T019 Attachment model in src/models/attachment.py"
Task: "T020 Thread model in src/models/thread.py"
Task: "T021 Classification model in src/models/classification.py"
Task: "T022 Suggestion model in src/models/suggestion.py"
Task: "T023 Feedback model in src/models/feedback.py"
Task: "T024 Explanation model in src/models/explanation.py"
Task: "T025 SemanticIndexEntry model in src/models/semantic_index.py"
Task: "T026 ModelState model in src/models/model_state.py"
Task: "T027 RetentionPolicy model in src/models/retention_policy.py"
Task: "T028 ProcessingJob model in src/models/processing_job.py"
```

## Validation Checklist
- [x] All contract endpoints have tests (T004–T013)
- [x] All user stories have integration tests (T014–T017)
- [ ] All entities have model tasks (T018–T028)
- [x] Tests come before implementation (T004–T017 before T018+)
- [x] [P] tasks touch different files only
- [x] Each task has an exact file path

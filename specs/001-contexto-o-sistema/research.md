# Research — Assistente de E-mails (Phase 0)

Data: 2025-09-27  
Branch: 001-contexto-o-sistema  
Spec: /Users/juliocezar/Dev/work/EXPERIMENTAL_EmailTriageAssistant/specs/001-contexto-o-sistema/spec.md

## Summary of Decisions
- Runtime/Language: Python 3.11 (compat-first)
- App Posture: CLI-first (Typer) + API local (Flask)
- Privacy/Security: Local-first, zero sharing without consent, SQLCipher + Keychain, loopback-only API
- Vector/Search: FAISS + multilingual MiniLM embeddings
- Classifier: scikit-learn (LogReg/SVM) with partial_fit; joblib persistence
- OCR/Parsing: Tesseract, pypdf, python-docx, unstructured
- Multilingual Scope: pt, en, es with autodetect; suggestions in user’s preferred language (FR-016)
- Sync Strategy: No automatic sync; manual encrypted export/import bundle (FR-017)
- Explainability: Show label+confidence, key factors, similar emails, and feedback influence (FR-018)
- OCR/Parsing Failures: Background retry queue with backoff; safe mode chunking for large files (FR-019)
- Retention: Indices 365d, models indefinite, derived attachments 90d; overrides + manual purge/export (FR-014)
- Urgency Rule: Any strong signal A|B|C marks as urgent (FR-010)

## Rationale
- Python 3.11: broad ecosystem support (FAISS/SQLCipher/Tesseract wheels) and stability.
- CLI-first + local API: aligns with privacy-by-default and keeps UX flexible (panel optional, Tauri later).
- FAISS + MiniLM: fast local semantic search with solid multilingual performance for pt/en/es.
- scikit-learn incremental: simple, reliable, supports online learning from feedback.
- Manual sync: reduces privacy risk and complexity; export/import fits local-first.
- Rich explainability: increases user trust and supports supervised corrections.
- Retry + chunking: improves robustness for corrupt/large files without blocking pipeline.

## Alternatives Considered
- Python 3.12 now → Deferred due to native deps.
- Full real-time sync → Rejected (privacy/complexity); may revisit via user-controlled storage later.
- Deep models (transformers) for classification → Heavier; start with classic ML + embeddings, revisit if needed.
- Cloud-based OCR → Rejected (privacy); local OCR sufficient for MVP.

## Open Questions (Deferred)
- Desktop UI (Tauri) detailed flows and packaging timelines → planned post-MVP.
- Advanced ranking metrics for search/classification → to be tuned with local eval set.

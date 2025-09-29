# EXPERIMENTAL_EmailTriageAssistant

Local-first email triage assistant with AI-powered classification, response suggestions, and multilingual support.

## 🎯 Vision
An intelligent email assistant that helps users efficiently triage and respond to emails while maintaining complete privacy and local control.

## 🏗️ Current Status (Phase 3.3 - September 29, 2025)

### ✅ Completed
- **Phase 3.1**: Project setup, Python environment, CLI scaffolding
- **Phase 3.2**: Complete test suite (23 tests) using TDD approach
- **Phase 3.3 Models**: All 11 core data models implemented with validation

### 🚧 In Progress
- **Phase 3.3 Services**: Storage layer and core business logic services

### 📋 Next Steps
- T029: Storage layer (SQLite + SQLCipher)
- T030-T035: Core services (embeddings, OCR, ingestion, ML)

## 🛠️ Tech Stack
- **Backend**: Python 3.11 + Flask API + Typer CLI
- **Storage**: SQLite + SQLCipher for encryption
- **ML**: FAISS vector search + sentence-transformers
- **OCR**: Tesseract for document processing
- **Models**: Pydantic v2 for data validation

## 🏛️ Architecture
```
src/
├── models/      # ✅ Data models (11 entities + 12 enums)
├── services/    # 🚧 Business logic layer
├── api/         # 🔜 Flask REST API
└── cli/         # ✅ Typer command interface
```

## 🧪 Quality Assurance
- **Tests**: 23 passing, 1 skipped (requires storage)
- **Validation**: TDD approach with comprehensive contracts
- **Standards**: Constitutional compliance (privacy-first, local-only)

## 🚀 Quick Start
See `specs/001-contexto-o-sistema/quickstart.md` for detailed setup instructions.

## 🤖 AI Development
- **Agent Instructions**: See `AGENTS.md` for AI agent workflow and documentation requirements
- **Documentation**: README.md and handoff.md must be updated after every action

## 📊 Progress Tracking
Detailed progress and task status: `specs/001-contexto-o-sistema/tasks.md`

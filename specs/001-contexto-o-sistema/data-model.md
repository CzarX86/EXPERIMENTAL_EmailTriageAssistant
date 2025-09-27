# Data Model — Assistente de E-mails (Phase 1)

Entities and relationships derived from the feature spec. Types are indicative.

## Entities

### Email
- id: UUID
- message_id: string (provider id)
- thread_id: UUID
- from: string (email)
- to: string[]
- cc: string[]
- bcc: string[]
- subject: string
- body_text: string
- body_html: string (optional)
- received_at: datetime
- language: enum(pt,en,es,unknown)
- has_attachments: bool
- source: enum(m365,imap,mbox)
- metadata: object (headers, labels)

### Attachment
- id: UUID
- email_id: UUID (FK Email)
- filename: string
- mime_type: string
- size_bytes: int
- extracted_text: string (nullable)
- ocr_status: enum(pending,processing,done,failed)
- hash: string (content hash)

### Thread
- id: UUID
- subject: string
- participants: string[]
- last_activity_at: datetime
- message_ids: UUID[] (Emails)

### Classification
- id: UUID
- email_id: UUID (FK Email)
- label: enum(spam,urgent,acao,responder,ignorar)
- confidence: float [0,1]
- origin: enum(auto,user_corrected)
- created_at: datetime
- rationale_ref: UUID (FK Explanation)

### Suggestion
- id: UUID
- email_id: UUID (FK Email)
- text: string
- created_at: datetime
- status: enum(pendente,aprovada,rejeitada)
- approved_at: datetime (nullable)
- corrected_text: string (nullable)

### Feedback
- id: UUID
- email_id: UUID (FK Email)
- type: enum(approve,reject,correct)
- payload: object (e.g., corrected_text)
- created_at: datetime

### Explanation
- id: UUID
- email_id: UUID (FK Email)
- label: string
- confidence: float
- key_factors: object { keywords: string[], vip: bool, time_window: string|null, thread_activity: string|null, mentions: string[] }
- similar_emails: Array<{ email_id: UUID, score: float }>
- feedback_influence: Array<{ feedback_id: UUID, weight: float }>
- created_at: datetime

### SemanticIndexEntry
- id: UUID
- ref_type: enum(email,attachment)
- ref_id: UUID (FK Email or Attachment)
- vector: float[]
- dim: int
- language: enum(pt,en,es,unknown)
- created_at: datetime

### ModelState
- id: UUID
- version: string
- params: object
- updated_at: datetime
- metrics: object

### RetentionPolicy
- id: UUID
- item_type: enum(index,model,derived)
- default_ttl_days: int
- user_override_ttl_days: int (nullable)
- auto_purge: bool

### ProcessingJob
- id: UUID
- job_type: enum(ingest,ocr,index,classify,suggest,export,import)
- status: enum(queued,running,done,failed,needs_attention)
- started_at: datetime
- finished_at: datetime (nullable)
- attempts: int
- max_attempts: int
- error: string (nullable)
- safe_mode: bool (for large files chunked processing)

## Relationships
- Email 1—N Attachment
- Thread 1—N Email
- Email 1—1 Classification (latest), historic in separate table or versioning
- Email 1—N Suggestion, Feedback, Explanation
- Email/Attachment 1—N SemanticIndexEntry
- RetentionPolicy applies by item_type across entities
- ProcessingJob references Email/Attachment indirectly via payload

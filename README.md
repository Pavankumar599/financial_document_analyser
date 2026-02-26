# Financial Document Analyzer - Debug Assignment (Fixed)

## Project Overview
A financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents (CrewAI).

This repository was provided with intentional issues:
- **Deterministic bugs** (broken imports, wrong APIs, undefined variables, etc.)
- **Inefficient / unsafe prompts** (hallucination-heavy, unstructured output)

The current version fixes both categories and returns **structured JSON outputs** grounded in the uploaded document.

---

## Setup

### 1) Create a virtual environment
```sh
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows
.venv\\Scripts\\activate
```

### 2) Install dependencies
```sh
pip install -r requirements.txt
```

### 3) Environment variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_key_here
# optional
LLM_MODEL=gpt-4o-mini
```

---

## Run the API
```sh
python main.py
```

API will start at `http://localhost:8000`.

---

## Use a sample document
The system analyzes financial PDFs like Tesla quarterly updates.

1. Download a PDF (example Tesla update)
2. Save it as `data/sample.pdf`
3. Or upload any financial PDF through the API endpoint below.

---

## API

### Health
`GET /`

### Analyze a PDF
`POST /analyze` (multipart/form-data)
- `file`: PDF
- `query`: (optional) analysis question

Example (curl):
```sh
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Summarize revenue, margin trends, risks, and provide investment considerations"
```

Response:
- `analysis` contains the CrewAI final output (stringified). It will include JSON blocks produced by each task.

---

## What was fixed (high level)

### Deterministic bugs
- Fixed broken LLM initialization (`llm = llm`) by creating a real `LLM(...)` instance.
- Fixed invalid tool wiring (`tool=` -> `tools=` and incorrect tool definitions).
- Replaced undefined PDF loader (`Pdf(...)`) with a working PDF extractor (`pypdf`).
- Fixed task/endpoint naming collisions and ensured `file_path` is passed to tasks.
- Added missing dependencies: `python-dotenv`, `pypdf`, `uvicorn`.

### Prompt improvements
- Removed instructions encouraging hallucinations and unsafe advice.
- Enforced **JSON-only** outputs with explicit schemas.
- Required **evidence snippets** from the document for key claims.
- Reduced verbosity and token waste.

---

## Notes
- If you upload scanned PDFs (image-only), text extraction may fail. Add OCR (e.g., pytesseract) if needed.

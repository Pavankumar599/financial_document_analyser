from __future__ import annotations

import os
import uuid

from fastapi import FastAPI, File, UploadFile, Form, HTTPException

from crewai import Crew, Process, Agents, Task

from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from task import verify_document, analyze_document, risk_assessment, investment_recommendation

app = FastAPI(title="Financial Document Analyzer")


def run_crew(query: str, file_path: str) -> str:
    """Run the end-to-end analysis crew."""

    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
        tasks=[verify_document, analyze_document, risk_assessment, investment_recommendation],
        process=Process.sequential,
        verbose=True,
    )

    return financial_crew.kickoff(inputs={"query": query, "file_path": file_path})


@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
):
    """Upload a PDF and receive a structured analysis."""

    if not query or not query.strip():
        query = "Analyze this financial document for investment insights"

    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", f"financial_document_{file_id}.pdf")

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query.strip(),
            "analysis": str(result),
            "file_processed": file.filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {e}")

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

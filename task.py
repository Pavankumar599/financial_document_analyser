"""CrewAI tasks.

The original repo intentionally included prompts that:
- encouraged hallucinations
- ignored the user query
- produced unstructured output

This file replaces them with concise, structured tasks.
"""

from __future__ import annotations

from crewai import Task

from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from tools import read_financial_document


verify_document = Task(
    description=(
        "Verify that the file at {file_path} is a financial document and extract basic metadata. "
        "First, call read_financial_document with the file path. Then output JSON with keys: "
        "is_financial_document (bool), company (string|null), period (string|null), currency (string|null), "
        "document_type (string|null), notes (string)."
    ),
    expected_output="Valid JSON only.",
    agent=verifier,
    tools=[read_financial_document],
)


analyze_document = Task(
    description=(
        "Analyze the financial document at {file_path} to answer the user query: '{query}'. "
        "Call read_financial_document first. Provide a structured analysis grounded in the document. "
        "Output MUST be JSON with keys: summary, key_financials, positives, concerns, open_questions, evidence. "
        "- key_financials: list of objects {metric, value, period, evidence_snippet}. "
        "- evidence: list of short snippets (max 25 words each) supporting the main claims. "
        "If a metric is not clearly stated, omit it or set value to null."
    ),
    expected_output="Valid JSON only.",
    agent=financial_analyst,
    tools=[read_financial_document],
)


risk_assessment = Task(
    description=(
        "Based on the financial document at {file_path} and the user's query '{query}', identify key risks. "
        "Call read_financial_document first. Output JSON with keys: top_risks, mitigants, scenario_notes, evidence. "
        "- top_risks: list of {risk, severity (low|medium|high), rationale, evidence_snippet}."
    ),
    expected_output="Valid JSON only.",
    agent=risk_assessor,
    tools=[read_financial_document],
)


investment_recommendation = Task(
    description=(
        "Provide investment considerations (NOT personalized advice) based on the document at {file_path} "
        "and the user's query '{query}'. Call read_financial_document first. Output JSON with keys: "
        "thesis, bull_case, bear_case, watchlist_metrics, recommendation_style, evidence. "
        "- recommendation_style must be one of: 'bullish', 'neutral', 'cautious'. "
        "- watchlist_metrics: list of {metric, why_it_matters}."
    ),
    expected_output="Valid JSON only.",
    agent=investment_advisor,
    tools=[read_financial_document],
)

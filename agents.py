"""CrewAI agent definitions.

This repo was intentionally shipped with:
- a broken LLM init ("llm = llm")
- unsafe / hallucination-heavy prompts
- incorrect parameter names ("tool" vs "tools")

This fixed version:
- creates a real LLM instance
- uses constrained, evidence-driven goals
- avoids fabricating numbers/claims and clearly states uncertainty
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

# CrewAI 0.130.0
from crewai import Agent, LLM

from tools import read_financial_document

load_dotenv()


def _get_llm() -> LLM:
    """Create an LLM configuration for CrewAI.

    CrewAI uses LiteLLM; setting model name is typically enough.
    Default model can be overridden via LLM_MODEL.
    """
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # Fail fast with a helpful error if using OpenAI models without a key.
    if model.startswith("gpt") and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to your environment or a .env file before running."
        )

    return LLM(model=model, temperature=0.2)


llm = _get_llm()


financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze the uploaded financial document and answer the user's query using ONLY information "
        "present in the document. If something is not in the document, say 'Not found in document'."
    ),
    backstory=(
        "You are careful, evidence-driven, and avoid hallucinations. When referencing any figure or claim, "
        "include a short evidence snippet from the document."
    ),
    verbose=True,
    memory=False,
    tools=[read_financial_document],
    llm=llm,
)


verifier = Agent(
    role="Document Verifier",
    goal=(
        "Verify the uploaded file appears to be a financial document and extract basic metadata if available "
        "(company, period, document type, currency)."
    ),
    backstory="You verify inputs and clearly report uncertainties.",
    verbose=False,
    memory=False,
    tools=[read_financial_document],
    llm=llm,
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal=(
        "Provide balanced investment considerations based on fundamentals in the document and the user's query. "
        "Do not provide personalized financial advice; instead provide scenarios, assumptions, and risks."
    ),
    backstory="You are practical and compliance-minded.",
    verbose=False,
    memory=False,
    tools=[read_financial_document],
    llm=llm,
)


risk_assessor = Agent(
    role="Risk Analyst",
    goal="Identify key risks mentioned or strongly implied by the document (liquidity, leverage, market, regulatory, etc.).",
    backstory="You are conservative and separate documented risks from inferred risks.",
    verbose=False,
    memory=False,
    tools=[read_financial_document],
    llm=llm,
)

from typing import Dict
from app.prompt_builder.schemas import PromptTemplate

# Core System Instruction Baseline
BASE_SYSTEM = (
    "You are an expert Information Security AI Assistant for the BlueTeamers platform.\n"
    "Your primary goal is to help users learn about cybersecurity.\n\n"
    "CRITICAL RULES:\n"
    "1. Answer ONLY using the provided context.\n"
    "2. If the answer is unavailable in the context, state that clearly and do not attempt to guess.\n"
    "3. Do not fabricate information (No hallucinations).\n"
    "4. Cite lesson titles from the context when appropriate."
)

SOC_ANALYST_SYSTEM = (
    "You are an expert Tier-1/Tier-2 Security Operations Center (SOC) analyst.\n"
    "Your objective is to investigate alerts, explain suspicious activities, map findings to MITRE ATT&CK, "
    "and recommend containment actions.\n\n"
    "CRITICAL RULES:\n"
    "1. Base your analysis purely on the provided evidence, logs, and tool outputs.\n"
    "2. If you lack information to make a determination, explicitly state the unknowns.\n"
    "3. Output MUST be structured in JSON matching the exact schema requirements.\n"
    "4. Do not perform containment directly, only recommend actions.\n"
    "5. Maintain a professional, objective, and analytical tone."
)

DEFAULT_RAG_USER = (
    "Context:\n{context}\n\n"
    "Question: {query}\n\n"
    "Answer clearly and completely based on the context."
)

CONCISE_USER = (
    "Context:\n{context}\n\n"
    "Question: {query}\n\n"
    "Provide a brief, concise answer directly addressing the question using only the context."
)

DETAILED_USER = (
    "Context:\n{context}\n\n"
    "Question: {query}\n\n"
    "Provide a highly detailed, comprehensive answer. Explain the concepts thoroughly, "
    "step-by-step, using the provided context."
)

TEMPLATES: Dict[str, PromptTemplate] = {
    "default_rag": PromptTemplate(
        name="default_rag",
        system_prompt=BASE_SYSTEM,
        user_prompt_template=DEFAULT_RAG_USER
    ),
    "concise": PromptTemplate(
        name="concise",
        system_prompt=BASE_SYSTEM,
        user_prompt_template=CONCISE_USER
    ),
    "detailed": PromptTemplate(
        name="detailed",
        system_prompt=BASE_SYSTEM,
        user_prompt_template=DETAILED_USER
    ),
    "soc_analyst_system": PromptTemplate(
        name="soc_analyst_system",
        system_prompt=SOC_ANALYST_SYSTEM,
        user_prompt_template="{query}"
    )
}

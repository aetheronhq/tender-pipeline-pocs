from typing import List, Literal, Optional, TypedDict
from pydantic import BaseModel, Field

InteractionType = Literal[
    "open_text",
    "checkbox",
    "dropdown",
    "multi_select",
    "yes_no",
    "numeric",
    "date",
    "table_row",
]


class Question(BaseModel):
    number: str = Field(..., description="The official question number (e.g. '1.1', 'A1'). Synthesize 'auto-XXX' if missing.")
    text: str = Field(..., description="The question text or requirement description.")
    interaction_type: InteractionType = Field("open_text", description="The type of interaction expected.")
    options: List[str] = Field(default_factory=list, description="List of options for dropdown/multi_select.")
    limit: Optional[str] = Field(None, description="Any length constraint (e.g. '500 words', '2000 chars', '1 page').")
    section_path: List[str] = Field(default_factory=list, description="Hierarchy of headings above this question. Include Number AND Title.")
    # section_path example: ["Schedule 1", "Part A", "1.1 Company Details"]
    # It allows reconstructing the document hierarchy without recursive schema complexity.


# TypedDict schema for Gemini API compatibility (source of truth for API structure)
class QuestionSchema(TypedDict):
    number: str
    text: str
    interaction_type: str
    options: List[str]
    limit: Optional[str]
    section_path: List[str]


class OutputSchema(TypedDict):
    questions: List[QuestionSchema]


class UsageStats(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    model_name: str = "unknown"
    cost_usd: float = 0.0
    latency_s: float = 0.0


class ExtractionResult(BaseModel):
    questions: List[Question] = Field(default_factory=list)
    usage: UsageStats = Field(default_factory=UsageStats)


class Answer(BaseModel):
    number: str
    answer: str
    citations: List[str] = Field(default_factory=list)
    attachment_refs: List[str] = Field(default_factory=list)


class AnswerResult(BaseModel):
    answers: List[Answer] = Field(default_factory=list)

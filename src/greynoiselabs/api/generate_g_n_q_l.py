# Generated by ariadne-codegen on 2023-10-16 13:24
# Source: queries

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GenerateGNQL(BaseModel):
    generate_g_n_q_l: "GenerateGNQLGenerateGNQL" = Field(alias="generateGNQL")


class GenerateGNQLGenerateGNQL(BaseModel):
    input_text: str
    queries: List[Optional[str]]


GenerateGNQL.model_rebuild()
GenerateGNQLGenerateGNQL.model_rebuild()

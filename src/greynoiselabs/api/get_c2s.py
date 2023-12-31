# Generated by ariadne-codegen on 2023-10-16 13:24
# Source: queries

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetC2s(BaseModel):
    top_c2s: "GetC2sTopC2s" = Field(alias="topC2s")


class GetC2sTopC2s(BaseModel):
    c2s: List["GetC2sTopC2sC2s"]


class GetC2sTopC2sC2s(BaseModel):
    source_ip: str
    hits: int
    pervasiveness: int
    c2_ips: List[Optional[str]]
    c2_domains: List[Optional[str]]
    payload: str


GetC2s.model_rebuild()
GetC2sTopC2s.model_rebuild()
GetC2sTopC2sC2s.model_rebuild()

# Generated by ariadne-codegen on 2023-07-28 05:36
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


GetC2s.update_forward_refs()
GetC2sTopC2s.update_forward_refs()
GetC2sTopC2sC2s.update_forward_refs()

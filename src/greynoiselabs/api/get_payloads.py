# Generated by ariadne-codegen on 2023-08-23 00:37
# Source: queries

from typing import List

from pydantic import Field

from .base_model import BaseModel


class GetPayloads(BaseModel):
    top_payloads: "GetPayloadsTopPayloads" = Field(alias="topPayloads")


class GetPayloadsTopPayloads(BaseModel):
    payloads: List["GetPayloadsTopPayloadsPayloads"]


class GetPayloadsTopPayloadsPayloads(BaseModel):
    protocol: str
    size: int
    payload: str
    payload_b64: str
    request_count: int
    source_ip_count: int
    pervasiveness: int


GetPayloads.model_rebuild()
GetPayloadsTopPayloads.model_rebuild()
GetPayloadsTopPayloadsPayloads.model_rebuild()

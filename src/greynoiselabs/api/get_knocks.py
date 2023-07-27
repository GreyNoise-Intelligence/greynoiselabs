# Generated by ariadne-codegen on 2023-07-27 17:26
# Source: queries

from typing import Any, List

from pydantic import Field

from .base_model import BaseModel


class GetKnocks(BaseModel):
    top_knocks: "GetKnocksTopKnocks" = Field(alias="topKnocks")


class GetKnocksTopKnocks(BaseModel):
    knock: List["GetKnocksTopKnocksKnock"]


class GetKnocksTopKnocksKnock(BaseModel):
    source_ip: str
    headers: str
    apps: str
    emails: List[str]
    favicon_mmh3_128: str
    favicon_mmh3_32: int
    ips: List[str]
    knock_port: int
    jarm: str
    last_seen: Any
    last_crawled: Any
    links: List[str]
    title: str
    tor_exit: bool


GetKnocks.update_forward_refs()
GetKnocksTopKnocks.update_forward_refs()
GetKnocksTopKnocksKnock.update_forward_refs()

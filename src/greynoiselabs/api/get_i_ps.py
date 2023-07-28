# Generated by ariadne-codegen on 2023-07-28 01:18
# Source: queries

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetIPs(BaseModel):
    top_popular_i_ps: "GetIPsTopPopularIPs" = Field(alias="topPopularIPs")


class GetIPsTopPopularIPs(BaseModel):
    popular_i_ps: List["GetIPsTopPopularIPsPopularIPs"] = Field(alias="popularIPs")


class GetIPsTopPopularIPsPopularIPs(BaseModel):
    ip: str
    request_count: int
    users_count: int
    last_requested: Any
    noise: bool
    last_seen: Optional[Any]


GetIPs.update_forward_refs()
GetIPsTopPopularIPs.update_forward_refs()
GetIPsTopPopularIPsPopularIPs.update_forward_refs()

# Generated by ariadne-codegen on 2023-07-27 05:00
# Source: queries

from typing import List

from pydantic import Field

from .base_model import BaseModel


class GetRequests(BaseModel):
    top_h_t_t_p_requests: "GetRequestsTopHTTPRequests" = Field(alias="topHTTPRequests")


class GetRequestsTopHTTPRequests(BaseModel):
    http_requests: List["GetRequestsTopHTTPRequestsHttpRequests"] = Field(
        alias="httpRequests"
    )


class GetRequestsTopHTTPRequestsHttpRequests(BaseModel):
    path: str
    request_count: int
    source_ip_count: int
    request_headers: List[str]
    pervasiveness: int


GetRequests.update_forward_refs()
GetRequestsTopHTTPRequests.update_forward_refs()
GetRequestsTopHTTPRequestsHttpRequests.update_forward_refs()

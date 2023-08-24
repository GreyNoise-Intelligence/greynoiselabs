# Generated by ariadne-codegen on 2023-08-24 14:30
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
    source_ips: List[str]


GetRequests.model_rebuild()
GetRequestsTopHTTPRequests.model_rebuild()
GetRequestsTopHTTPRequestsHttpRequests.model_rebuild()

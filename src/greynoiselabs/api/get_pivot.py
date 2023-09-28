# Generated by ariadne-codegen on 2023-09-27 22:53
# Source: queries

from typing import Any, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel


class GetPivot(BaseModel):
    pivot: Union["GetPivotPivotGNQLResult", "GetPivotPivotPCAPResponse"] = Field(
        discriminator="typename__"
    )


class GetPivotPivotGNQLResult(BaseModel):
    typename__: Literal["GNQLResult"] = Field(alias="__typename")
    queries: List["GetPivotPivotGNQLResultQueries"]


class GetPivotPivotGNQLResultQueries(BaseModel):
    type: str
    urls: List[str]


class GetPivotPivotPCAPResponse(BaseModel):
    typename__: Literal["PCAPResponse"] = Field(alias="__typename")
    id: str
    ips: List["GetPivotPivotPCAPResponseIps"]


class GetPivotPivotPCAPResponseIps(BaseModel):
    first_packet_time: Any = Field(alias="firstPacketTime")
    ip: str
    last_packet_time: Any = Field(alias="lastPacketTime")
    user_agents: List[str] = Field(alias="userAgents")
    port_counts: List["GetPivotPivotPCAPResponseIpsPortCounts"] = Field(
        alias="portCounts"
    )
    paths: List[str]
    ja3: List[str]
    hassh: List[str]
    hostnames: List[str]


class GetPivotPivotPCAPResponseIpsPortCounts(BaseModel):
    count: int
    port: str


GetPivot.model_rebuild()
GetPivotPivotGNQLResult.model_rebuild()
GetPivotPivotGNQLResultQueries.model_rebuild()
GetPivotPivotPCAPResponse.model_rebuild()
GetPivotPivotPCAPResponseIps.model_rebuild()
GetPivotPivotPCAPResponseIpsPortCounts.model_rebuild()

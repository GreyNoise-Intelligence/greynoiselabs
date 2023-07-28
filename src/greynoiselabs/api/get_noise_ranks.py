# Generated by ariadne-codegen on 2023-07-28 01:19
# Source: queries

from typing import List

from pydantic import Field

from .base_model import BaseModel


class GetNoiseRanks(BaseModel):
    noise_rank: "GetNoiseRanksNoiseRank" = Field(alias="noiseRank")


class GetNoiseRanksNoiseRank(BaseModel):
    ips: List["GetNoiseRanksNoiseRankIps"]


class GetNoiseRanksNoiseRankIps(BaseModel):
    ip: str
    noise_score: int
    country_pervasiveness: str
    payload_diversity: str
    port_diversity: str
    request_rate: str
    sensor_pervasiveness: str


GetNoiseRanks.update_forward_refs()
GetNoiseRanksNoiseRank.update_forward_refs()
GetNoiseRanksNoiseRankIps.update_forward_refs()

# Generated by ariadne-codegen on 2023-09-26 15:28
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


GetNoiseRanks.model_rebuild()
GetNoiseRanksNoiseRank.model_rebuild()
GetNoiseRanksNoiseRankIps.model_rebuild()

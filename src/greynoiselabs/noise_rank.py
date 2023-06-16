# Generated by ariadne-codegen on 2023-06-16 04:37
# Source: queries

from typing import List

from pydantic import Field

from .base_model import BaseModel


class NoiseRank(BaseModel):
    noise_rank: "NoiseRankNoiseRank" = Field(alias="noiseRank")


class NoiseRankNoiseRank(BaseModel):
    query_info: "NoiseRankNoiseRankQueryInfo" = Field(alias="queryInfo")
    ips: List["NoiseRankNoiseRankIps"]


class NoiseRankNoiseRankQueryInfo(BaseModel):
    results_available: int = Field(alias="resultsAvailable")
    results_limit: int = Field(alias="resultsLimit")


class NoiseRankNoiseRankIps(BaseModel):
    country_pervasiveness: str
    ip: str
    noise_score: int
    payload_diversity: str
    port_diversity: str
    request_rate: str
    sensor_pervasiveness: str


NoiseRank.update_forward_refs()
NoiseRankNoiseRank.update_forward_refs()
NoiseRankNoiseRankQueryInfo.update_forward_refs()
NoiseRankNoiseRankIps.update_forward_refs()

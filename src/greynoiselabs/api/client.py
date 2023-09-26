# Generated by ariadne-codegen on 2023-09-26 13:39
# Source: queries

from typing import Dict

from .async_base_client import AsyncBaseClient
from .base_model import Upload
from .generate_g_n_q_l import GenerateGNQL
from .get_c2s import GetC2s
from .get_i_ps import GetIPs
from .get_knocks import GetKnocks
from .get_noise_ranks import GetNoiseRanks
from .get_payloads import GetPayloads
from .get_pivot import GetPivot
from .get_requests import GetRequests


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_c2s(self) -> GetC2s:
        query = gql(
            """
            query getC2s {
              topC2s {
                c2s {
                  source_ip
                  hits
                  pervasiveness
                  c2_ips
                  c2_domains
                  payload
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetC2s.model_validate(data)

    async def get_requests(self, useragent: str) -> GetRequests:
        query = gql(
            """
            query getRequests($useragent: String!) {
              topHTTPRequests(input: {userAgent: $useragent}) {
                httpRequests {
                  path
                  request_count
                  source_ip_count
                  request_headers
                  pervasiveness
                  source_ips
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"useragent": useragent}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetRequests.model_validate(data)

    async def get_knocks(self, ip: str) -> GetKnocks:
        query = gql(
            """
            query getKnocks($ip: String!) {
              topKnocks(ip: $ip) {
                knock {
                  source_ip
                  headers
                  apps
                  emails
                  favicon_mmh3_128
                  favicon_mmh3_32
                  ips
                  knock_port
                  jarm
                  last_seen
                  last_crawled
                  links
                  title
                  tor_exit
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"ip": ip}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetKnocks.model_validate(data)

    async def generate_g_n_q_l(self, input_text: str) -> GenerateGNQL:
        query = gql(
            """
            query generateGNQL($input_text: String!) {
              generateGNQL(input_text: $input_text) {
                input_text
                queries
              }
            }
            """
        )
        variables: Dict[str, object] = {"input_text": input_text}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GenerateGNQL.model_validate(data)

    async def get_noise_ranks(self, ip: str) -> GetNoiseRanks:
        query = gql(
            """
            query getNoiseRanks($ip: String!) {
              noiseRank(ip: $ip) {
                ips {
                  ip
                  noise_score
                  country_pervasiveness
                  payload_diversity
                  port_diversity
                  request_rate
                  sensor_pervasiveness
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"ip": ip}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetNoiseRanks.model_validate(data)

    async def get_payloads(self, protocol: str) -> GetPayloads:
        query = gql(
            """
            query getPayloads($protocol: String!) {
              topPayloads(input: {protocol: $protocol}) {
                payloads {
                  protocol
                  size
                  payload
                  payload_b64
                  request_count
                  source_ip_count
                  pervasiveness
                  source_ips
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"protocol": protocol}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetPayloads.model_validate(data)

    async def get_pivot(
        self,
        pcap: Upload,
        gnql: bool,
        reverse: bool,
        ignore_private: bool,
        ignore_flows: bool,
    ) -> GetPivot:
        query = gql(
            """
            query getPivot($pcap: Upload!, $gnql: Boolean!, $reverse: Boolean!, $ignorePrivate: Boolean!, $ignoreFlows: Boolean!) {
              pivot(
                input: {file: $pcap, gnql: $gnql, reverse: $reverse, ignorePrivate: $ignorePrivate, ignoreFlows: $ignoreFlows}
              ) {
                __typename
                ... on GNQLResult {
                  queries {
                    type
                    urls
                  }
                }
                ... on PCAPResponse {
                  id
                  ips {
                    firstPacketTime
                    ip
                    lastPacketTime
                    userAgents
                    portCounts {
                      count
                      port
                    }
                    paths
                    ja3
                    hassh
                    hostnames
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "pcap": pcap,
            "gnql": gnql,
            "reverse": reverse,
            "ignorePrivate": ignore_private,
            "ignoreFlows": ignore_flows,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetPivot.model_validate(data)

    async def get_i_ps(self) -> GetIPs:
        query = gql(
            """
            query getIPs {
              topPopularIPs {
                popularIPs {
                  ip
                  request_count
                  users_count
                  last_requested
                  noise
                  last_seen
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetIPs.model_validate(data)

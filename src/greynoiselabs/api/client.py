# Generated by ariadne-codegen on 2023-07-27 17:13
# Source: queries

from .async_base_client import AsyncBaseClient
from .generate_g_n_q_l import GenerateGNQL
from .get_c2s import GetC2s
from .get_i_ps import GetIPs
from .get_knocks import GetKnocks
from .get_noise_ranks import GetNoiseRanks
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
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetC2s.parse_obj(data)

    async def get_requests(self) -> GetRequests:
        query = gql(
            """
            query getRequests {
              topHTTPRequests {
                httpRequests {
                  path
                  request_count
                  source_ip_count
                  request_headers
                  pervasiveness
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetRequests.parse_obj(data)

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
        variables: dict[str, object] = {"ip": ip}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetKnocks.parse_obj(data)

    async def generate_g_n_q_l(self, input: str) -> GenerateGNQL:
        query = gql(
            """
            query generateGNQL($input: String!) {
              generateGNQL(input: $input) {
                input_text
                queries
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GenerateGNQL.parse_obj(data)

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
        variables: dict[str, object] = {"ip": ip}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetNoiseRanks.parse_obj(data)

    async def get_i_ps(self) -> GetIPs:
        query = gql(
            """
            query getIPs {
              topPopularIPs {
                popularIPs {
                  ip
                  request_count
                  users_count
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetIPs.parse_obj(data)

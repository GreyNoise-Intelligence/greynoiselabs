# Generated by ariadne-codegen on 2023-07-27 10:52
# Source: schemas/schema.graphql

from .base_model import BaseModel


class SpectaQLOption(BaseModel):
    key: str
    value: str


SpectaQLOption.update_forward_refs()

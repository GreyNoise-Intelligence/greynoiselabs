# Generated by ariadne-codegen on 2023-08-23 14:04
# Source: schemas/schema.graphql

from .base_model import BaseModel


class SpectaQLOption(BaseModel):
    key: str
    value: str


SpectaQLOption.model_rebuild()

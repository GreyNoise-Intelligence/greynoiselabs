# Generated by ariadne-codegen on 2023-08-22 16:01
# Source: schemas/schema.graphql

from .base_model import BaseModel


class SpectaQLOption(BaseModel):
    key: str
    value: str


SpectaQLOption.model_rebuild()

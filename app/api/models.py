import time

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class PublicBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ResponseWithTimestamp(PublicBaseModel):
    timestamp: int = Field(default_factory=lambda: int(time.time()))

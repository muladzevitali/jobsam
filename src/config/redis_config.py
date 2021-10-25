import os
from typing import Union

from pydantic import (BaseModel)


class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: str = '6379'
    password: str = None
    db: str = 0

    class Config:
        @classmethod
        def alias_generator(cls, string) -> str:
            return f'REDIS_{string.upper()}'

    @property
    def uri(self):
        return self.db_uri(self.db)

    def db_uri(self, db: Union[str, int]) -> str:
        if self.password:
            return f'redis://:{self.password}@{self.host}:{self.port}/{db}'

        return f'redis://{self.host}:{self.port}/{db}'


redis_config = RedisConfig(**os.environ)

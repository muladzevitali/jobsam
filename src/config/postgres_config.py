import os

from pydantic import BaseModel


class PostgresConfig(BaseModel):
    host: str = 'localhost'
    port: str = '5342'
    db: str = 'jobsam'
    user: str = 'postgres'
    password: str = 'postgres'

    class Config:
        @classmethod
        def alias_generator(cls, field_name: str) -> str:
            return f'POSTGRES_{field_name.upper()}'


postgres_config = PostgresConfig(**os.environ)

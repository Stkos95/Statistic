from environs import Env
from dataclasses import dataclass




@dataclass
class Database:
    user: str
    password: str
    container: str

@dataclass
class Config:
    database: Database




def load_config(path=None):

    env = Env()
    env.read_env(path)
    return Config(
        database=Database(
            user=env.str('MONGO_USER'),
            password=env.str('MONGO_PASSWORD'),
            container=env.str('MONGO_CONTAINER_NAME')
        )
    )



from configparser import ConfigParser
from os import getenv

from requests.api import get
__version__ = "0.0.1"

class Config(ConfigParser):
    DEBUG = getenv("DEBUG", "false") in ("true", "True", "TRUE")
    API_ENV = getenv("API_ENV", "devel")
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = getenv("SECRET_KEY", "70f9b42ecd696bc5545915d6316ca590623d09786f3876d71d50c92d7472cb6b")
    ALGORITHM = getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    API_DOCS_URL = getenv("API_DOCS_URL", "/docs")
    API_OPENAPI_PREFIX = getenv("API_OPENAPI_PREFIX", "")
    API_TITLE = getenv("API_TITLE", "BorealAPI")
    API_DESCRIPTION = getenv("API_DESCRIPTION", "description")
    API_VERSION = __version__
    

class Development(Config):
    DATABASE = getenv("DATABASE", "MOCK")


class Production(Config):
    pass
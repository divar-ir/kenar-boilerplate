from functools import lru_cache

from kenar import Client

from boilerplate import settings


@lru_cache(maxsize=1)
def get_divar_kenar_client() -> Client:
    return Client(settings.divar_kenar_client_conf)

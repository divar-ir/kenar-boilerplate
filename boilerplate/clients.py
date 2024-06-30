from functools import lru_cache

from kenar.app import KenarApp

from boilerplate import settings


@lru_cache(maxsize=1)
def get_divar_kenar_client() -> KenarApp:
    return KenarApp(settings.divar_kenar_client_conf)

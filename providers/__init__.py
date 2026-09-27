from .base import ProviderError, ProviderNotConfigured
from .http_json import HttpJsonProvider


def get_provider():
    return HttpJsonProvider()


__all__ = ["get_provider", "ProviderError", "ProviderNotConfigured"]

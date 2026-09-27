from __future__ import annotations

from typing import Any


class ProviderError(RuntimeError):
    """Expected provider-side failure."""


class ProviderNotConfigured(ProviderError):
    """No authorized upstream provider has been configured."""


class BaseProvider:
    def search(self, params: Any):
        raise NotImplementedError

    def info(self, params: Any):
        raise NotImplementedError

    def seasons(self, params: Any):
        raise NotImplementedError

    def episodes(self, params: Any):
        raise NotImplementedError

    def dls(self, params: Any):
        raise NotImplementedError

    def table(self, params: Any):
        raise NotImplementedError

    def similar(self, params: Any):
        raise NotImplementedError

    def previous_next(self, params: Any):
        raise NotImplementedError

    def actors(self, params: Any):
        raise NotImplementedError

    def story(self, params: Any):
        raise NotImplementedError

    def thumbnail(self, params: Any):
        raise NotImplementedError

    def title(self, params: Any):
        raise NotImplementedError

    def trailer(self, params: Any):
        raise NotImplementedError

    def note(self, params: Any):
        raise NotImplementedError

    def quality(self, params: Any):
        raise NotImplementedError

    def rating_percent(self, params: Any):
        raise NotImplementedError

    def page(self, params: Any):
        raise NotImplementedError

    def pages(self, params: Any):
        raise NotImplementedError

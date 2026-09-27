from __future__ import annotations

import json
import os
from typing import Any

import requests

from .base import BaseProvider, ProviderError, ProviderNotConfigured


class HttpJsonProvider(BaseProvider):
    """
    Adapter for an authorized upstream JSON API.

    The Movyz API itself requires no caller bearer token. An upstream bearer
    token may be supplied server-side only when the upstream provider
    legitimately requires one.
    """

    def __init__(self) -> None:
        self.base_url = os.getenv("PROVIDER_BASE_URL", "").strip().rstrip("/")
        self.timeout = float(os.getenv("PROVIDER_TIMEOUT", "20"))
        self.bearer = os.getenv("PROVIDER_BEARER_TOKEN", "").strip()
        self.extra_headers = self._load_headers()

    def _load_headers(self) -> dict[str, str]:
        raw = os.getenv("PROVIDER_HEADERS_JSON", "").strip()
        if not raw:
            return {}
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ProviderError("PROVIDER_HEADERS_JSON is not valid JSON") from exc
        if not isinstance(value, dict):
            raise ProviderError("PROVIDER_HEADERS_JSON must contain a JSON object")
        return {str(k): str(v) for k, v in value.items()}

    def _request(self, route: str, params: Any):
        if not self.base_url:
            raise ProviderNotConfigured(
                "Set PROVIDER_BASE_URL to an authorized upstream provider."
            )

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.extra_headers,
        }
        if self.bearer:
            headers["Authorization"] = f"Bearer {self.bearer}"

        try:
            response = requests.get(
                f"{self.base_url}/{route.lstrip('/')}",
                params={k: v for k, v in params.items() if v not in (None, "")},
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise ProviderError(f"Upstream request failed: {exc}") from exc

        if response.status_code in (401, 403):
            raise ProviderError(
                "The configured upstream rejected the request. "
                "Use an authorized provider credential if that provider requires one."
            )

        if response.status_code >= 400:
            raise ProviderError(
                f"Upstream returned HTTP {response.status_code}."
            )

        try:
            return response.json()
        except ValueError as exc:
            raise ProviderError("Upstream did not return valid JSON.") from exc

    def _call(self, route: str, params: Any):
        return self._request(route, params)

    def search(self, params): return self._call("search", params)
    def info(self, params): return self._call("info", params)
    def seasons(self, params): return self._call("seasons", params)
    def episodes(self, params): return self._call("episodes", params)
    def dls(self, params): return self._call("dls", params)
    def table(self, params): return self._call("table", params)
    def similar(self, params): return self._call("similar", params)
    def previous_next(self, params): return self._call("previous_next", params)
    def actors(self, params): return self._call("actors", params)
    def story(self, params): return self._call("story", params)
    def thumbnail(self, params): return self._call("thumbnail", params)
    def title(self, params): return self._call("title", params)
    def trailer(self, params): return self._call("trailer", params)
    def note(self, params): return self._call("note", params)
    def quality(self, params): return self._call("quality", params)
    def rating_percent(self, params): return self._call("rating_percent", params)
    def page(self, params): return self._call("page", params)
    def pages(self, params): return self._call("pages", params)

from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify, request

from providers import ProviderError, ProviderNotConfigured, get_provider

app = Flask(__name__)


def _required_query(name: str) -> str:
    value = request.args.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required query parameter: {name}")
    return value


def _json_result(value: Any):
    return jsonify(value)


@app.get("/health")
def health():
    return jsonify(
        {
            "ok": True,
            "service": "movyz-egybest-compatible-api",
            "provider_configured": bool(os.getenv("PROVIDER_BASE_URL")),
        }
    )


@app.get("/")
def index():
    return jsonify(
        {
            "name": "Movyz EgyBest-compatible API",
            "version": "1.0.0",
            "auth": {
                "caller_token_required": False,
                "upstream_token_optional": True,
            },
            "endpoints": [
                "/health",
                "/search",
                "/info",
                "/seasons",
                "/episodes",
                "/dls",
                "/table",
                "/similar",
                "/previous_next",
                "/actors",
                "/story",
                "/thumbnail",
                "/title",
                "/trailer",
                "/note",
                "/quality",
                "/rating_percent",
                "/page",
                "/pages",
            ],
        }
    )


def _dispatch(method_name: str):
    provider = get_provider()
    try:
        return getattr(provider, method_name)(request.args)
    except ProviderNotConfigured as exc:
        return jsonify(
            {
                "success": False,
                "error": "provider_not_configured",
                "message": str(exc),
            }
        ), 503
    except ProviderError as exc:
        return jsonify(
            {
                "success": False,
                "error": "provider_error",
                "message": str(exc),
            }
        ), 502


@app.get("/search")
def search():
    if not request.args.get("query", "").strip():
        return jsonify({"success": False, "error": "Missing query parameter: query"}), 400
    return _dispatch("search")


@app.get("/info")
def info():
    if not request.args.get("url", "").strip():
        return jsonify({"success": False, "error": "Missing query parameter: url"}), 400
    return _dispatch("info")


@app.get("/seasons")
def seasons():
    if not request.args.get("url", "").strip():
        return jsonify({"success": False, "error": "Missing query parameter: url"}), 400
    return _dispatch("seasons")


@app.get("/episodes")
def episodes():
    if not request.args.get("url", "").strip():
        return jsonify({"success": False, "error": "Missing query parameter: url"}), 400
    return _dispatch("episodes")


@app.get("/dls")
def dls():
    if not request.args.get("url", "").strip():
        return jsonify({"success": False, "error": "Missing query parameter: url"}), 400
    return _dispatch("dls")


@app.get("/table")
def table():
    return _dispatch("table")


@app.get("/similar")
def similar():
    return _dispatch("similar")


@app.get("/previous_next")
def previous_next():
    return _dispatch("previous_next")


@app.get("/actors")
def actors():
    return _dispatch("actors")


@app.get("/story")
def story():
    return _dispatch("story")


@app.get("/thumbnail")
def thumbnail():
    return _dispatch("thumbnail")


@app.get("/title")
def title():
    return _dispatch("title")


@app.get("/trailer")
def trailer():
    return _dispatch("trailer")


@app.get("/note")
def note():
    return _dispatch("note")


@app.get("/quality")
def quality():
    return _dispatch("quality")


@app.get("/rating_percent")
def rating_percent():
    return _dispatch("rating_percent")


@app.get("/page")
def page():
    return _dispatch("page")


@app.get("/pages")
def pages():
    return _dispatch("pages")


@app.errorhandler(ValueError)
def handle_value_error(exc):
    return jsonify({"success": False, "error": "bad_request", "message": str(exc)}), 400


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )

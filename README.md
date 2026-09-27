# Movyz API

Independent API foundation derived from the original `AmineSoukara/EgyBest-API` project.

## What changed

This fork no longer treats the original project's caller `ACCESS_TOKEN` / `REFRESH_TOKEN` flow as the API contract.

The new service exposes an **EgyBest-compatible route shape without requiring a bearer token from Movyz clients**.

The upstream data source is deliberately isolated behind a provider adapter:

```
Movyz client
    |
    |  no caller bearer token
    v
Movyz API
    |
    |  provider adapter
    v
Authorized upstream provider
```

An upstream bearer token can be configured server-side only when the selected provider legitimately requires one. This project does **not** attempt to bypass upstream authentication.

## Included routes

- `GET /health`
- `GET /search?query=...`
- `GET /info?url=...`
- `GET /seasons?url=...`
- `GET /episodes?url=...`
- `GET /dls?url=...`
- `GET /table?url=...`
- `GET /similar?url=...`
- `GET /previous_next?url=...`
- `GET /actors?url=...`
- `GET /story?url=...`
- `GET /thumbnail?url=...`
- `GET /title?url=...`
- `GET /trailer?url=...`
- `GET /note?url=...`
- `GET /quality?url=...`
- `GET /rating_percent?url=...`
- `GET /page?path=...&number=...`
- `GET /pages?path=...&limit=...`

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Health check:

```
GET http://localhost:8080/health
```

Without a configured provider, data routes intentionally return HTTP 503 with `provider_not_configured`. That is expected until an authorized source is connected.

## Provider configuration

Set:

```env
PROVIDER_BASE_URL=https://your-authorized-provider.example
```

For a provider that explicitly requires a server-side bearer token:

```env
PROVIDER_BEARER_TOKEN=your-own-authorized-token
```

The token is never accepted from Movyz clients and should never be committed to GitHub.

## Deployment

A standard WSGI deployment can use:

```bash
gunicorn app:app
```

The repository also contains a `Procfile` for hosts that support it.

## Tests

```bash
pytest
```

## License

The original project is GPL-3.0. Keep the existing `LICENSE` file and comply with the license when distributing modified versions.


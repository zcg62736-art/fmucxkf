# fmucxkf

A scalable programmatic content and page publishing platform.

## Phase 1

- FastAPI control API
- PostgreSQL data store
- Redis job queue
- Worker service
- Jinja2 page compiler
- Static publisher
- Nginx delivery
- Docker Compose local/runtime stack

Core flow:

`Site -> Keyword -> Campaign -> Candidate -> PageSpec -> Render -> Publish`

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

API health check:

```bash
curl http://localhost/api/v1/health
```

Published static pages are served by Nginx under `/pages/`.

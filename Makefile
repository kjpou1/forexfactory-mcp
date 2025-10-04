# ───────────────────────────────────────────────
#  ForexFactory MCP Makefile
#  Uses local Python MCP for stdio,
#  and npx-based Node Inspector for HTTP/SSE.
# ───────────────────────────────────────────────

# Run MCP Inspector against local Python (stdio)
dev-stdio:
	uv run mcp dev src/forexfactory_mcp/server.py

# Run Node Inspector (npx) against Dockerized HTTP/SSE server
dev-http:
	npx @modelcontextprotocol/inspector dev --url http://localhost:8000

# Build Docker image
build:
	docker compose build

# Run MCP server in Docker (HTTP/SSE mode)
run:
	docker compose up forexfactory_mcp


# Run MCP server in Docker (HTTP/SSE mode)
run-http:
	docker compose run --rm --service-ports \
	-e MCP_TRANSPORT=http \
	-e MCP_HOST=0.0.0.0 \
	-e MCP_PORT=8000 \
	forexfactory_mcp

# Stop containers
stop:
	docker compose down

# Tail logs for live debugging
logs:
	docker compose logs -f forexfactory_mcp

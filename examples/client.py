import asyncio
import json

from mcp import ClientSession, McpError, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "forexfactory_mcp.server"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to ForexFactory MCP server")

            # List available resources
            resources_resp = await session.list_resources()

            print("Resources:")
            for res in resources_resp.resources:
                print(f" - {res.uri} ({res.description}) / {res.name}")

            # Example: fetch today's events if available
            today_res = next(
                (res for res in resources_resp.resources if res.name == "events_today"),
                None,
            )
            if today_res:
                try:
                    result = await session.read_resource(today_res.uri)

                    events_text = ""
                    for content in result.contents:
                        if content.mimeType == "application/json" and content.text:
                            # If the resource returned JSON-as-text
                            try:
                                data = json.loads(content.text)
                                events_text += json.dumps(data, indent=2)
                            except Exception:
                                events_text += content.text
                        elif content.mimeType.startswith("text/") and content.text:
                            # Plain text resource
                            events_text += content.text
                        else:
                            # fallback for blob or unknown
                            events_text += (
                                f"[Unsupported content type: {content.mimeType}]"
                            )

                    print("\nToday’s events:")
                    print(events_text)
                except McpError as e:
                    print(f"⚠️ Could not fetch {today_res.uri}: {e}")

            # week_res = next(
            #     (res for res in resources_resp.resources if res.name == "events_week"),
            #     None,
            # )
            # if week_res:
            #     try:
            #         result = await session.read_resource(week_res.uri)
            #         print("\nThis week’s events:")
            #         print(result)
            #     except McpError as e:
            #         print(f"⚠️ Could not fetch {week_res.uri}: {e}")


if __name__ == "__main__":
    asyncio.run(main())

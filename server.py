import os
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("clay-olostep-mcp")

OLOSTEP_API_KEY = os.environ.get("OLOSTEP_API_KEY", "")

@mcp.tool
def olostep_scrape_page(url_to_scrape: str) -> dict:
    """
    Scrape a page with Olostep and return markdown + text.
    """
    resp = httpx.post(
        "https://api.olostep.com/v1/scrapes",
        headers={
            "Authorization": f"Bearer {OLOSTEP_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"url_to_scrape": url_to_scrape, "formats": ["markdown", "text"]},
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()

    return {
        "url": url_to_scrape,
        "markdown": data.get("markdown_content") or data.get("markdown"),
        "text": data.get("text_content") or data.get("text") or str(data),
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    # Native way to run FastMCP as an SSE HTTP server
    mcp.run(transport="sse", host="0.0.0.0", port=port)

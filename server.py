from fastmcp import FastMCP
import os, httpx

mcp = FastMCP("clay-olostep-mcp")

OLOSTEP_API_KEY = os.environ["OLOSTEP_API_KEY"]

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
        json={
            "url_to_scrape": url_to_scrape,
            "formats": ["markdown", "text"],
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()

    return {
        "url": url_to_scrape,
        "markdown": data.get("markdown"),
        "text": data.get("text"),
    }

if __name__ == "__main__":
    mcp.run()

# server.py
import os
import httpx
from fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# ----- MCP tool definition (same logic you already had) -----

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
        json={"url_to_scrape": url_to_scrape, "formats": ["markdown", "text"]},
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()

    return {
        "url": url_to_scrape,
        "markdown": data.get("markdown"),
        "text": data.get("text"),
    }

# ----- FastAPI HTTP wrapper so Railway has something to talk to -----

app = FastAPI(title="Olostep MCP HTTP Bridge")

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/tools/olostep_scrape_page")
async def http_scrape(payload: dict):
    url = payload.get("url_to_scrape") or payload.get("url")
    if not url:
        return JSONResponse(
            status_code=400,
            content={"error": "url_to_scrape is required"},
        )
    result = olostep_scrape_page(url)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    # IMPORTANT for Railway
    uvicorn.run("server:app", host="0.0.0.0", port=port)

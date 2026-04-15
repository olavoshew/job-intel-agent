import re

import httpx


async def fetch_jd(url: str) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL: HTTP {response.status_code}")

    html = response.text
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<nav[^>]*>.*?</nav>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<header[^>]*>.*?</header>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<footer[^>]*>.*?</footer>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&[a-zA-Z]+;", " ", html)
    text = re.sub(r"\s+", " ", html).strip()

    if len(text) < 200:
        raise ValueError(f"Page text too short ({len(text)} chars), likely not a job description")

    return text

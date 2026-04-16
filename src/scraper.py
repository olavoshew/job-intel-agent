import ipaddress
import re
import socket
from urllib.parse import urlparse

import httpx

MAX_RESPONSE_BYTES = 5_000_000

BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]"}


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https URLs are supported")
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must include a hostname")
    if hostname in BLOCKED_HOSTS:
        raise ValueError("Cannot fetch from localhost or loopback addresses")
    try:
        addr = ipaddress.ip_address(hostname)
        if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved:
            raise ValueError("Cannot fetch from private or reserved IP addresses")
    except ValueError as exc:
        if "private" in str(exc) or "Cannot fetch" in str(exc):
            raise
    try:
        resolved = socket.getaddrinfo(hostname, None)
        for family, _, _, _, sockaddr in resolved:
            ip = ipaddress.ip_address(sockaddr[0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError("URL resolves to a private or reserved IP address")
    except socket.gaierror:
        raise ValueError("Could not resolve hostname")


async def fetch_jd(url: str) -> str:
    _validate_url(url)

    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError("Failed to fetch the provided URL")

    if len(response.content) > MAX_RESPONSE_BYTES:
        raise ValueError("Page is too large to process")

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
        raise ValueError("Page text too short, likely not a job description")

    return text

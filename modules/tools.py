import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
from modules.logging import logger
from modules.memory import ChromaDBMemory, RedisMemory

class Tools:
    def __init__(self, config):
        self.config = config
        memory_config = self.config.get("memory", {})

        # ChromaDB setup
        chroma_config = memory_config.get("chromadb", {})
        self.chroma_memory = ChromaDBMemory(
            path=chroma_config.get("path", "chroma_db"),
            collection_name=chroma_config.get("collection_name", "documents")
        )

        # Redis setup
        redis_config = memory_config.get("redis", {})
        self.redis_memory = RedisMemory(
            redis_host=redis_config.get("host", "localhost"),
            redis_port=redis_config.get("port", 6379),
            redis_db=redis_config.get("db", 0)
        )

    async def get_website_content(self, url: str) -> str:
        logger.info("Getting website content for URL: %s", url)
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url, timeout=60000)
                content = await page.content()
                await browser.close()

            soup = BeautifulSoup(content, "html.parser")
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            logger.info("Successfully retrieved and parsed content from %s", url)
            return text
        except Exception as e:
            logger.error("Error getting website content for URL %s: %s", url, e)
            return f"Error: Could not retrieve content from {url}. Reason: {e}"

    def searx_search(self, query: str, base_url: str = "http://127.0.0.1:8888") -> str:
        logger.info("Performing SearxNG search for query: %s", query)
        try:
            params = {"q": query, "format": "json"}
            response = requests.get(f"{base_url}/search", params=params)
            response.raise_for_status()
            results = response.json()

            formatted_results = []
            if "results" in results:
                for item in results["results"]:
                    formatted_results.append(f"Title: {item.get('title', 'N/A')}\nURL: {item.get('url', 'N/A')}\nSnippet: {item.get('content', 'N/A')}")

            logger.info("SearxNG search completed successfully.")
            return "\n\n".join(formatted_results) if formatted_results else "No results found."
        except requests.exceptions.RequestException as e:
            logger.error("SearxNG search failed: %s", e)
            return f"Error: Search failed. Reason: {e}"

    def save_to_memory(self, document: str):
        self.chroma_memory.add_document(document)
        return "Document successfully saved to memory."

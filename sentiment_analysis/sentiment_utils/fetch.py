import requests
import time
import random
from dotenv import load_dotenv


load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")


def fetch_papers(query, max_results=100):
    if not SERP_API_KEY:
        raise EnvironmentError("❌ SERP_API_KEY not found. Check your .env file.")
    all_papers = []
    start = 0

    while len(all_papers) < max_results:
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": SERP_API_KEY,
            "num": min(20, max_results - len(all_papers)),
            "start": start,
            "hl": "en",
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        papers = data.get("organic_results", [])
        if not papers:
            break

        all_papers.extend(papers)
        start += len(papers)
        time.sleep(random.uniform(1, 2))

    return all_papers[:max_results]

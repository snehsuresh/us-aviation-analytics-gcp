import re


def classify_publication(paper):
    pub_info = str(paper.get("publication_info", {}).get("summary", "")).lower()
    link = paper.get("link", "").lower()

    if "arxiv" in link or "ssrn" in link:
        return "Working paper"
    if "doi.org" in link:
        return "Journal article"
    if "conference" in pub_info:
        return "Conference paper"
    if "thesis" in pub_info:
        return "Thesis"
    return "Unclassified"

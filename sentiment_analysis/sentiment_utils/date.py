import re
from datetime import datetime


def extract_dates(paper):
    year = None
    full_date = None
    pub_info = str(paper.get("publication_info", {}).get("summary", ""))

    year_sources = [
        paper.get("year"),
        re.search(r"(20\d{2})", pub_info),
        re.search(r"(20\d{2})", paper.get("link", "")),
    ]
    for source in year_sources:
        if hasattr(source, "group"):
            year = int(source.group(1))
            break
        elif isinstance(source, str) and source.isdigit():
            year = int(source)
            break

    date_patterns = [r"(\d{4}-\d{2}-\d{2})"]
    for pattern in date_patterns:
        match = re.search(pattern, pub_info)
        if match:
            try:
                full_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
            except ValueError:
                pass

    return {
        "year": year,
        "full_date": full_date,
        "date_string": str(full_date) if full_date else None,
    }

import argparse
import pandas as pd
from sentiment_utils.fetch import fetch_papers
from sentiment_utils.date import extract_dates
from sentiment_utils.classify import classify_publication
from sentiment_utils.analyze import analyze_sentiment

try:
    from gcp_config.upload_to_gcs import upload_to_gcs
    from gcp_config.write_to_bigquery import write_df_to_bigquery

    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False

SEARCH_QUERIES = [
    "consumer attitudes toward airline ticket prices",
    "airfare transparency customer expectations",
    "price sensitivity in air travel demand analysis",
    "low-cost carrier pricing strategy feedback",
    "dynamic pricing effects on airline passengers",
]


def run_analysis(queries, output_path="aviation_research_enhanced.csv", upload=False):
    all_data = []
    for query in queries:
        papers = fetch_papers(query, max_results=100)
        for paper in papers:
            date_info = extract_dates(paper)
            pub_type = classify_publication(paper)
            text = f"{paper.get('title', '')}. {paper.get('snippet', '')}"
            sentiment = analyze_sentiment(text)

            data = {
                "Title": paper.get("title", ""),
                "Year": date_info["year"],
                "Full_Date": date_info["date_string"],
                "Publication_Type": pub_type,
                "Sentiment": sentiment["sentiment"],
                "Polarity_Score": sentiment["polarity"],
                "Subjectivity_Score": sentiment["subjectivity"],
                "Search_Query": query,
                "Link": paper.get("link", ""),
            }
            all_data.append(data)

    df = pd.DataFrame(all_data)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved analysis to {output_path}")

    if upload and GCP_AVAILABLE:
        upload_to_gcs(output_path, "your-bucket", f"sentiment/{output_path}")
        write_df_to_bigquery(df, "your_project.dataset.sentiment_output")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--upload", action="store_true", help="Upload results to GCP")
    args = parser.parse_args()
    run_analysis(SEARCH_QUERIES, upload=args.upload)

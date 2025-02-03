from google.cloud import bigquery
import pandas as pd


def write_df_to_bigquery(df, table_id):
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"✅ Written to BigQuery: {table_id}")

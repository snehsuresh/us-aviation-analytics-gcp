from google.cloud import storage


def upload_to_gcs(local_file, bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file)
    print(f"✅ Uploaded to gs://{bucket_name}/{blob_name}")

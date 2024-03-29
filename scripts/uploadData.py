
from google.cloud import storage
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(r"C:\Users\16466\Desktop\cis4400Homework\modified-shape-418121-5e39251205f6.json")
storage_client = storage.Client(credentials=credentials)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "de_hw_bucket"
    # The path to your file to upload
    source_file_name = "C:\\Users\\16466\\Desktop\\cis4400Homework\\Data Sources\\bedBugData.csv"
    # The ID of your GCS object
    destination_blob_name = "destination_blob.csv"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")



upload_blob("de_hw_bucket", "C:\\Users\\16466\Desktop\cis4400Homework\\Data Sources\\bedBugData.csv", "modified-shape-418121")

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account

# Create BigQuery client
credentials = service_account.Credentials.from_service_account_file(r"C:\Users\16466\Desktop\cis4400Homework\scripts\Private Key\modified-shape-418121-5e39251205f6.json")
client = bigquery.Client(credentials=credentials)
project_id = "modified-shape-418121"
dataset_id = "BedBugDataset"
table_name = "BedBugTable"

# Extract data from the existing table
query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}`"
df = client.query(query).to_dataframe()

# Convert columns to strings
for column in df.columns:
    try:
        df[column] = df[column].astype(str)
    except ValueError:
        print(f"Error converting column '{column}' to string. Some values may not be convertible.")

# Get the schema of existing table
existing_table_ref = client.dataset(dataset_id).table(table_name)
existing_table = client.get_table(existing_table_ref)

# Create a new schema with the same structure 
new_schema = []
for field in existing_table.schema:
    if field.name in ["building_id", "registration_id", "postcode", "community_board", "city_council_district", "census_tract_2010", "bin", "bbl"]:
        new_schema.append(bigquery.SchemaField(field.name, "STRING"))
    else:
        new_schema.append(field)

# Create a new table with the updated schema
new_table_ref = client.dataset(dataset_id).table(f"{table_name}_updated")
new_table = bigquery.Table(new_table_ref, schema=new_schema)

# Delete the existing table if it exists
try:
    client.delete_table(new_table_ref)
    print(f"Existing table {dataset_id}.{table_name}_updated deleted successfully.")
except NotFound:
    print(f"Table {dataset_id}.{table_name}_updated does not exist. Skipping deletion.")

# Create the new table with the updated schema
client.create_table(new_table)

# Load data from the DataFrame into the new table
client.load_table_from_dataframe(df, new_table_ref)

print(f"Data successfully migrated to a new table with updated schema.")

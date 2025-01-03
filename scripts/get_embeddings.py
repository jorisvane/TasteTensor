import csv
from supabase import create_client
from backend.app.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)

def fetch_batch_from_supabase(last_processed_id, batch_size):
    response = supabase.table('recipe_data') \
        .select('id, Embedding') \
        .gt('id', last_processed_id) \
        .order('id') \
        .limit(batch_size) \
        .execute()
    rows = response.data
    return rows

def process_database_to_csv(batch_size=1000, output_file="embeddings.csv"):
    last_processed_id = 0
    is_file_initialized = False

    # Open the CSV file
    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Loop through database rows in batches
        while True:
            rows = fetch_batch_from_supabase(last_processed_id, batch_size)
            if not rows:
                print('All rows from database are processed')
                break

            # Initialize the CSV file with headers on the first batch
            if not is_file_initialized:
                writer.writerow(["id", "Embedding"])  # CSV headers
                is_file_initialized = True

            # Write each row to CSV
            for row in rows:
                # Extract the data
                recipe_id = row["id"]
                embedding = row["Embedding"]  # Fetch existing embedding from Supabase

                # Write the row to the CSV file
                writer.writerow([recipe_id, embedding])

                # Update the last processed ID
                last_processed_id = recipe_id

            print(f"Processed up to row ID {last_processed_id}")

# Run the script
process_database_to_csv()
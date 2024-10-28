from tkinter import messagebox
from siret_processor import SiretProcessor, get_siret_data
import os
from dotenv import load_dotenv
import threading
import json
from client_csv_maker import csv_maker
from tqdm import tqdm
import json


def process_data(db_name, results : list):
    """
    Fetches SIRET data from the database and initiates processing.

    Args:
        db_name (str): The name of the database from which to fetch SIRET data.
    """
    

def main():
    """
    The main entry point of the application.

    Initializes the GUI and starts the data processing in separate threads for each database.
    """
    load_dotenv()
    threads = []
    results = []

    try:
        databases = os.getenv("DB_NAMES").split(",")
    except Exception:
        print("ERROR: No array of databases provided. Please check your environment variables.")
        exit(84)

    files_to_check = ['client_good_siret.csv', 'client_duplicate_siret.csv', 'client_bad_siret.csv']

    for file in files_to_check:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")
        else:
            print(f"File does not exist: {file}")

    for db_name in databases:
        thread = threading.Thread(target=process_data, args=(db_name, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for result, db_name in tqdm(zip(results, databases), total=len(results), desc="Processing databases"):
        result["db_name"] = db_name
        print(f"DB[{result['db_name']}]")
        if 'counts' in result:  # Check if 'counts' exists
            print(f"counts:\ngood[{result['counts']['good']}]\nduplicate[{result['counts']['duplicate']}]\nbad[{result['counts']['bad']}]")
        else:
            print("counts data not found for this database.")
        csv = csv_maker(db_name)

        # Process good customers
        for customer in tqdm(result['customers']['good'], desc="Processing good customers", leave=False):
            csv.write_good_csv(customer)

        # Process duplicate customers
        for customer in tqdm(result['customers']['duplicate'], desc="Processing duplicate customers", leave=False):
            csv.write_duplicate_csv(customer)

        # Process bad customers
        for customer in tqdm(result['customers']['bad'], desc="Processing bad customers", leave=False):
            csv.write_bad_csv(customer)

    # Writing final stats to JSON
    with open("final.json", 'w') as json_file:
        results_stats = [
            {
                "counts": result["counts"],
                "db_name": result["db_name"]
            }
            for result in results
        ]
        json.dump(results_stats, json_file, indent=4)

if __name__ == "__main__":
    main()

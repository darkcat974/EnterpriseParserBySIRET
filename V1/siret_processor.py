from db import get_db
import re


class SiretProcessor:
    """
    A class for processing SIRET numbers.

    This class is responsible for validating SIRET numbers, categorizing them, 
    and writing the results to CSV files.
    """

    def __init__(self):
        """
        Initializes the SiretProcessor.

        Sets up lists to store valid, invalid, duplicate, and empty SIRET numbers,
        and initializes a CSV maker for output.
        """
        self.true_siret = []
        self.false_siret = []
        self.duplicate_siret = []
        self.empty_siret = []
        self.csv_maker = None

    def process_siret(self, siret, index, total_count):
        """
        Validates a single SIRET number.

        Args:
            siret (str): The SIRET number to process.
            index (int): The index of the SIRET number being processed.
            total_count (int): The total number of SIRET numbers to process.

        Returns:
            dict: A dictionary containing the processing result and statistics.
        """
        result = None
        if not siret or siret.strip() == "":
            self.empty_siret.append(siret)
            result = "⚠ Empty"
        else:
            if not re.match(r'^\d{9}$|^\d{14}$', siret):
                self.false_siret.append(siret)
                result = "✗ Invalid"
            else:
                if siret not in self.true_siret:
                    self.true_siret.append(siret)
                    result = "✓ Valid"
                else:
                    self.duplicate_siret.append(siret)
                    result = "⚠ Duplicate"
        return {
            "item": siret,
            "result": result,
            "processed": index + 1,
            "total": total_count,
            "categories": {
                "Valid": len(self.true_siret),
                "Invalid": len(self.false_siret),
                "Duplicate": len(self.duplicate_siret),
                "Empty": len(self.empty_siret),
            },
        }

    def process_sirets(self, df):
        """
        Processes a DataFrame of SIRET numbers.

        Args:
            df (DataFrame): The DataFrame containing SIRET numbers to process.

        This method processes SIRET numbers in parallel and updates progress.
        """
        total_count = len(df)
        counter = {
            "bad" : 0,
            "good" : 0,
            "duplicate" : 0
        }
        customers = {
            'good' : [],
            'bad' : [],
            'duplicate' : [],
        }

        for index, row in df.iterrows():
            siret = row['CT_Siret']
            customer = self.process_siret(siret, index, total_count)
            print(f"{index + 1}/{total_count} | result = {customer['result']} | siret: {customer['item'] if customer['item'] != '' else 'None'}")
            if customer["result"] == "⚠ Empty" or customer["result"] == "✗ Invalid":
                counter["bad"] += 1
                customers["bad"].append(customer["item"])
            elif customer["result"] == "✓ Valid":
                counter["good"] += 1
                customers["good"].append(customer["item"])
            elif customer["result"] == "⚠ Duplicate":
                counter["duplicate"] += 1
                customers["duplicate"].append(customer["item"])
        return {
            "db_name": df['DB_Name'],
            "counts": counter,
            "customers": customers,
        }

def get_siret_data(db_name):
    """
    Fetches SIRET data from the specified database.

    Args:
        db_name (str): The name of the database to query.

    Returns:
        The result of the database query, containing SIRET data.
    """
    return get_db(db_name)

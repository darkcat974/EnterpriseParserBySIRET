from tqdm import tqdm
import os
import pandas as pd
from dotenv import load_dotenv
import pyodbc
import json

def get_filtered_siret(db_name):
    """
    @brief Connects to the specified database and retrieves filtered SIRET data.

    This function loads database connection parameters from environment variables
    and executes SQL queries to fetch valid, invalid, and duplicate SIRET data
    from the specified database.

    @param db_name The name of the database to connect to.

    @return A tuple of three pandas DataFrames: 
            - The first DataFrame contains valid SIRET data.
            - The second DataFrame contains duplicate SIRET data.
            - The third DataFrame contains invalid SIRET data.
            Returns None if the connection fails.

    @note This function assumes that the environment variables for the database connection
          address, user, and password are defined in a .env file.
    
    The SQL queries executed in this function:
    - Valid SIRET: Length of 14 or 9, numeric format.
    - Invalid SIRET: Any SIRET that doesn't meet the valid criteria.
    - Duplicate SIRET: Valid SIRETs that appear more than once.
    """
    load_dotenv()
    server = os.getenv('DB_ADDR')
    database = db_name
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    try:
        # Create pyodbc engine
        engine = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

        # Use pyodbc engine with pandas
        querybase = "SELECT [CT_Siret], [CT_Num], [CT_Intitule], DB_NAME() as 'DB_Name' FROM [F_COMPTET] WHERE CT_Type=0 AND CT_Sommeil=0;"
        query1 = """WITH CleanedSIRET AS (
                        SELECT 
                            CASE 
                                WHEN CT_Siret LIKE '% %' THEN REPLACE(CT_Siret, ' ', '')
                                ELSE CT_Siret 
                            END AS CleanSIRET,
                            CT_Siret AS OriginalSIRET,
                            [CT_Num],
                            [CT_Intitule],
                            DB_NAME() as 'DB_Name',
                            ROW_NUMBER() OVER (PARTITION BY 
                                CASE 
                                    WHEN CT_Siret LIKE '% %' THEN REPLACE(CT_Siret, ' ', '')
                                    ELSE CT_Siret 
                                END
                            ORDER BY (SELECT NULL)) AS RowNum
                        FROM F_COMPTET
                    )
                """
        querygood = """SELECT CleanSIRET,
                            [CT_Num],
                            [CT_Intitule],
                            DB_NAME() as 'DB_Name'
                        FROM CleanedSIRET
                        WHERE (LEN(CleanSIRET) = 14 OR LEN(CleanSIRET) = 9)
                            AND (CleanSIRET LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' 
                                OR CleanSIRET LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
                            AND RowNum = 1;
                    """
        querybad = """SELECT OriginalSIRET,
                            [CT_Num],
                            [CT_Intitule],
                            DB_NAME() as 'DB_Name'
                        FROM CleanedSIRET
                        WHERE NOT ((LEN(CleanSIRET) = 14 OR LEN(CleanSIRET) = 9)
                            AND (CleanSIRET LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' 
                                OR CleanSIRET LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'));
                    """
        querydup = """SELECT CleanSIRET,
                            [CT_Num],
                            [CT_Intitule],
                            DB_NAME() as 'DB_Name'
                        FROM CleanedSIRET
                        WHERE (LEN(CleanSIRET) = 14 OR LEN(CleanSIRET) = 9)
                            AND (CleanSIRET LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' 
                                OR CleanSIRET LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
                            AND RowNum > 1;
                    """
        good = pd.read_sql(query1 + querygood, engine)
        dup = pd.read_sql(query1 + querydup, engine)
        bad = pd.read_sql(query1 + querybad, engine)
        return good, dup, bad
    except Exception as e:
        print(f"Couldn't connect to the db: {str(e)}")
        return None

def write_csv(client_info, type):
    """
    @brief Creates CSV files for client data based on SIRET validity.

    This function generates a CSV file from the provided DataFrame based
    on the specified SIRET status (valid, invalid, or duplicate).

    @param client_info The DataFrame containing client information.
    @param type A string indicating the SIRET status, which determines the
                filename (should be 'good', 'bad', or 'duplicate').

    The generated file will be named:
    - client_good_siret.csv
    - client_bad_siret.csv
    - client_duplicate_siret.csv

    @note Ensure that the 'client_info' DataFrame has the columns:
          ['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_NAME'].
    """
    client_info.to_csv(f'client_{type}_siret.csv', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_NAME'])


def main():
    load_dotenv()
    stats = []

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

    for db_name in tqdm(databases, desc="Processing databases"):
        good, dup, bad = get_filtered_siret(db_name)

        write_csv(good, "good")
        write_csv(dup, "dup")
        write_csv(bad, "bad")

        results = {
            "db_name": db_name,
            "good": len(good),
            "duplicate": len(dup),
            "bad": len(bad),
            "total": len(good) + len(dup) + len(bad),
        }
        stats.append(results)

    with open("stats.json", 'w') as json_file:
        json.dump(stats, json_file, indent=4)

if __name__ == "__main__":
    main()

import os
import pandas as pd
from dotenv import load_dotenv
import pyodbc

def get_db(db_name):
    """
    @brief Connects to the specified database and retrieves SIRET data.

    This function loads database connection parameters from environment variables
    and executes a SQL query to fetch specific data from the specified database.

    @param db_name The name of the database to connect to.

    @return A pandas DataFrame containing the SIRET data, or None if the connection fails.
    
    This function assumes that the environment variables for the database connection
    address, user, and password are defined in a .env file.
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
        query = "SELECT [CT_Siret], [CT_Num], [CT_Intitule], DB_NAME() FROM [F_COMPTET] WHERE CT_Type=0 AND CT_Sommeil=0;"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Couldn't connect to the db: {str(e)}")
        return None

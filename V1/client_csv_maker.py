import os
import pandas

def client_csv_maker(db, good_siret_client, bad_siret_client, duplicate_siret_client):
    """
    @brief Creates CSV files for client data based on SIRET validity.

    This function generates three CSV files from the provided DataFrame based
    on the SIRET status: valid, invalid, and duplicate.

    @param db The DataFrame containing client information.
    @param good_siret_client A list of validated SIRET numbers.
    @param bad_siret_client A list of invalid SIRET numbers.
    @param duplicate_siret_client A list of duplicate SIRET numbers.

    The generated files are:
    - client_good_siret.csv
    - client_bad_siret.csv
    - client_duplicate_siret.csv
    """
    # Creation of validated client
    db[db['CT_Siret'].isin(good_siret_client)].to_csv('client_good_siret.csv', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_NAME'])
    # Creation of invalid client
    db[db['CT_Siret'].isin(bad_siret_client)].to_csv('client_bad_siret.csv', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_NAME'])
    # Creation of duplicated client
    db[db['CT_Siret'].isin(duplicate_siret_client)].to_csv('client_duplicate_siret.csv', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_NAME'])


class csv_maker:
    """
    @brief A class for writing client SIRET data to CSV files.

    This class handles the creation and updating of CSV files for
    validated, invalid, and duplicate SIRET numbers.
    """

    def __init__(self, db):
        """
        @brief Initializes the csv_maker.

        @param db The DataFrame containing client information.
        """
        self.db = db

    def write_good_csv(self, siret):
        """
        @brief Writes a valid SIRET number to the good SIRET CSV file.

        @param siret The valid SIRET number to write to the CSV file.

        If the file does not exist, it creates it with a header; 
        otherwise, it appends to the existing file without a header.
        """
        if not os.path.isfile('client_good_siret.csv'):
            self.db[self.db['CT_Siret'].isin([siret])].to_csv('client_good_siret.csv', mode='w', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_Name'])
        else:
            existing_data = pandas.read_csv('client_good_siret.csv', dtype={'CT_Siret': str,'CT_Num' : str, 'CT_Intitule' : str, 'DB_Name' : str})
            if existing_data['CT_Siret'].isin([siret]).any():
                return
            else:
                self.db[self.db['CT_Siret'].isin([siret])].to_csv('client_good_siret.csv', mode='a', index=False, header=False)

    def write_bad_csv(self, siret):
        """
        @brief Writes an invalid SIRET number to the bad SIRET CSV file.

        @param siret The invalid SIRET number to write to the CSV file.

        If the file does not exist, it creates it with a header; 
        otherwise, it appends to the existing file without a header.
        """
        if not os.path.isfile('client_bad_siret.csv'):
            self.db[self.db['CT_Siret'].isin([siret])].to_csv('client_bad_siret.csv', mode='w', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_Name'])
        else:
            existing_data = pandas.read_csv('client_bad_siret.csv', dtype={'CT_Siret': str,'CT_Num' : str, 'CT_Intitule' : str, 'DB_Name' : str})
            if existing_data['CT_Siret'].isin([siret]).any():
                return
            else:
                self.db[self.db['CT_Siret'].isin([siret])].to_csv('client_bad_siret.csv', mode='a', index=False, header=False)

    def write_duplicate_csv(self, siret):
        """
        @brief Writes a duplicate SIRET number to the duplicate SIRET CSV file.

        @param siret The duplicate SIRET number to write to the CSV file.

        If the file does not exist, it creates it with a header; 
        otherwise, it appends to the existing file without a header.
        """
        if not os.path.isfile('client_duplicate_siret.csv'):
            self.db[self.db['CT_Siret'].isin([siret])].to_csv('client_duplicate_siret.csv', mode='w', index=False, header=['CT_Siret', 'CT_Num', 'CT_Intitule', 'DB_Name'])
        else:
            existing_data = pandas.read_csv('client_duplicate_siret.csv', dtype={'CT_Siret': str,'CT_Num' : str, 'CT_Intitule' : str, 'DB_Name' : str})
            if existing_data['CT_Siret'].isin([siret]).any():
                return
            else:
                self.db[self.db['CT_Siret'].isin([siret])].to_csv('client_duplicate_siret.csv', mode='a', index=False, header=False)

# AllianzTrade

## Introduction

AllianzTrade is a Python-based application designed for processing and validating **SIRET** numbers. It connects to a database, retrieves client information, categorizes SIRET numbers into valid, invalid, and duplicate entries, and generates CSV files for each category. The application provides a user-friendly GUI for visualizing the processing progress.

> **⚠️ WARNING:**
> We are not using a verification process through an external site. The database is substantial, and verifying through the site would either take too long (multiple days/weeks) or spam the connected API.
>
> Please note that only the **format** and **composition** of the SIRET are verified, **not** its existence in an official database. After trying through multiple APIs, we got banned for some time. Try your luck, but we do not recommend spamming sites, even for simple verifications.

## Process

1. Connects to a SQL Server database to fetch client data.
2. Validates SIRET numbers based on specific criteria.
3. Categorizes SIRET numbers into:
   - **Valid**
   - **Invalid**
   - **Duplicate**
   - **Empty**
4. Generates separate CSV files for each category of SIRET numbers.
5. Provides a visual representation of processing progress through a GUI.

## Requirements

- **Python 3**
- **Libraries:**
  - `pandas`
  - `pyodbc`
  - `tkinter`
  - `dotenv`

You can install the required libraries using pip:

```bash
pip install pandas pyodbc python-dotenv
```
### Author
Florian DAJON : [Github](https://github.com/darkcat974) | [linkedin](https://www.linkedin.com/in/florian-dajon-99a963231)
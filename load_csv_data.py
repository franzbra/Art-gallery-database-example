# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 15:45:59 2024

@author: Francesco Brandoli
"""
# load_csv.py

import pandas as pd
from db_connection import *

def load_csv_to_mysql(file_path, table_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Establish a database connection
    cnx, cursor = get_connection()

    # Iterate over the DataFrame and insert each row into the database
    for i, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        update_stmt = ', '.join([f"{col} = VALUES({col})" for col in row.index])
        
        sql = (f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) "
               f"ON DUPLICATE KEY UPDATE {update_stmt}")
        
        try:
            cursor.execute(sql, tuple(row))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            continue

    # Commit the transaction
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()


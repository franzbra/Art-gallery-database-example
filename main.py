# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 15:39:56 2024

@author: Francesco Brandoli
"""
from create_tables import create_tables
from  load_csv_data import *

if __name__ == '__main__':
    # Create database
    create_tables()
    # Load data into tables from CSV files
    csv_files_and_tables = [
    ('artists.csv', 'Artist'),
    ('locations.csv', 'Location'),
    ('artworks.csv', 'Artwork'),
    ('exhibitions.csv', 'Exhibition'),
    ('exhibition_artworks.csv', 'Exhibition_Artwork'),
    ('customers.csv', 'Customer'),
    ('sales.csv', 'Sales'),
    ('loans.csv', 'Loan'),
    ('employees.csv', 'Employee'),
    ('donations.csv', 'Donation'),
    ('donors.csv', 'Donor'),
    ('inventory.csv', 'Inventory')
    ]

    for file_path, table_name in csv_files_and_tables:
        load_csv_to_mysql(file_path, table_name)
    

# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 15:39:21 2024

@author: Francesco Brandoli
"""
from db_connection import *

TABLES = {}

TABLES['Artwork'] = (
    "CREATE TABLE `Artwork` ("
    "  `ArtworkID` int NOT NULL AUTO_INCREMENT,"
    "  `Title` varchar(255) NOT NULL,"
    "  `ArtistID` int NOT NULL,"
    "  `Year` year,"
    "  `Medium` varchar(255),"
    "  `Dimensions` varchar(255),"
    "  `Price` decimal(10,2),"
    "  `LocationID` int NOT NULL,"
    "  `Status` varchar(50),"
    "  `Description` text,"
    "  `ImageURL` varchar(255),"
    "  PRIMARY KEY (`ArtworkID`),"
    "  FOREIGN KEY (`ArtistID`) REFERENCES `Artist`(`ArtistID`),"
    "  FOREIGN KEY (`LocationID`) REFERENCES `Location`(`LocationID`)"
    ") ENGINE=InnoDB")

TABLES['Artist'] = (
    "CREATE TABLE `Artist` ("
    "  `ArtistID` int NOT NULL AUTO_INCREMENT,"
    "  `FirstName` varchar(255),"
    "  `LastName` varchar(255),"
    "  `DateOfBirth` date,"
    "  `Nationality` varchar(255),"
    "  `Biography` text,"
    "  `WebsiteURL` varchar(255),"
    "  `ImageURL` varchar(255),"
    "  PRIMARY KEY (`ArtistID`)"
    ") ENGINE=InnoDB")

TABLES['Exhibition'] = (
    "CREATE TABLE `Exhibition` ("
    "  `ExhibitionID` int NOT NULL AUTO_INCREMENT,"
    "  `Title` varchar(255) NOT NULL,"
    "  `StartDate` date,"
    "  `EndDate` date,"
    "  `LocationID` int NOT NULL,"
    "  `Description` text,"
    "  PRIMARY KEY (`ExhibitionID`),"
    "  FOREIGN KEY (`LocationID`) REFERENCES `Location`(`LocationID`)"
    ") ENGINE=InnoDB")

TABLES['Exhibition_Artwork'] = (
    "CREATE TABLE `Exhibition_Artwork` ("
    "  `ExhibitionID` int NOT NULL,"
    "  `ArtworkID` int NOT NULL,"
    "  PRIMARY KEY (`ExhibitionID`, `ArtworkID`),"
    "  FOREIGN KEY (`ExhibitionID`) REFERENCES `Exhibition`(`ExhibitionID`),"
    "  FOREIGN KEY (`ArtworkID`) REFERENCES `Artwork`(`ArtworkID`)"
    ") ENGINE=InnoDB")

TABLES['Location'] = (
    "CREATE TABLE `Location` ("
    "  `LocationID` int NOT NULL AUTO_INCREMENT,"
    "  `Name` varchar(255) NOT NULL,"
    "  `Address` varchar(255),"
    "  `City` varchar(255),"
    "  `State` varchar(255),"
    "  `ZipCode` varchar(10),"
    "  `Country` varchar(255),"
    "  PRIMARY KEY (`LocationID`)"
    ") ENGINE=InnoDB")

TABLES['Customer'] = (
    "CREATE TABLE `Customer` ("
    "  `CustomerID` int NOT NULL AUTO_INCREMENT,"
    "  `FirstName` varchar(255) NOT NULL,"
    "  `LastName` varchar(255) NOT NULL,"
    "  `Email` varchar(255),"
    "  `PhoneNumber` varchar(15),"
    "  `Address` varchar(255),"
    "  `City` varchar(255),"
    "  `State` varchar(255),"
    "  `ZipCode` varchar(10),"
    "  `Country` varchar(255),"
    "  PRIMARY KEY (`CustomerID`)"
    ") ENGINE=InnoDB")

TABLES['Sales'] = (
    "CREATE TABLE `Sales` ("
    "  `SaleID` int NOT NULL AUTO_INCREMENT,"
    "  `ArtworkID` int NOT NULL,"
    "  `CustomerID` int NOT NULL,"
    "  `DateOfSale` date,"
    "  `SalePrice` decimal(10,2),"
    "  PRIMARY KEY (`SaleID`),"
    "  FOREIGN KEY (`ArtworkID`) REFERENCES `Artwork`(`ArtworkID`),"
    "  FOREIGN KEY (`CustomerID`) REFERENCES `Customer`(`CustomerID`)"
    ") ENGINE=InnoDB")

TABLES['Loan'] = (
    "CREATE TABLE `Loan` ("
    "  `LoanID` int NOT NULL AUTO_INCREMENT,"
    "  `ArtworkID` int NOT NULL,"
    "  `BorrowerName` varchar(255),"
    "  `BorrowerAddress` varchar(255),"
    "  `StartDate` date,"
    "  `EndDate` date,"
    "  `ReturnDate` date,"
    "  PRIMARY KEY (`LoanID`),"
    "  FOREIGN KEY (`ArtworkID`) REFERENCES `Artwork`(`ArtworkID`)"
    ") ENGINE=InnoDB")

TABLES['Employee'] = (
    "CREATE TABLE `Employee` ("
    "  `EmployeeID` int NOT NULL AUTO_INCREMENT,"
    "  `FirstName` varchar(255),"
    "  `LastName` varchar(255),"
    "  `Role` varchar(255),"
    "  `Email` varchar(255),"
    "  `PhoneNumber` varchar(15),"
    "  `HireDate` date,"
    "  PRIMARY KEY (`EmployeeID`)"
    ") ENGINE=InnoDB")

TABLES['Donation'] = (
    "CREATE TABLE `Donation` ("
    "  `DonationID` int NOT NULL AUTO_INCREMENT,"
    "  `DonorID` int NOT NULL,"
    "  `ArtworkID` int NOT NULL,"
    "  `DateOfDonation` date,"
    "  PRIMARY KEY (`DonationID`),"
    "  FOREIGN KEY (`DonorID`) REFERENCES `Donor`(`DonorID`),"
    "  FOREIGN KEY (`ArtworkID`) REFERENCES `Artwork`(`ArtworkID`)"
    ") ENGINE=InnoDB")

TABLES['Donor'] = (
    "CREATE TABLE `Donor` ("
    "  `DonorID` int NOT NULL AUTO_INCREMENT,"
    "  `FirstName` varchar(255),"
    "  `LastName` varchar(255),"
    "  `Email` varchar(255),"
    "  `PhoneNumber` varchar(15),"
    "  `Address` varchar(255),"
    "  PRIMARY KEY (`DonorID`)"
    ") ENGINE=InnoDB")

TABLES['Inventory'] = (
    "CREATE TABLE `Inventory` ("
    "  `InventoryID` int NOT NULL AUTO_INCREMENT,"
    "  `ArtworkID` int NOT NULL,"
    "  `CurrentLocation` varchar(255),"
    "  `Condition` varchar(255),"
    "  `LastCheckedDate` date,"
    "  PRIMARY KEY (`InventoryID`),"
    "  FOREIGN KEY (`ArtworkID`) REFERENCES `Artwork`(`ArtworkID`)"
    ") ENGINE=InnoDB")

def create_tables():
    cnx, cursor = get_connection()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()



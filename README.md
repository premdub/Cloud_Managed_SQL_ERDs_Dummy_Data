# Cloud_Managed_SQL_ERDs_Dummy_Data
HHA504_assignment_6
# Cloud_Managed_SQL_ERDs-_Dummy_Data
HHA 504 Assignment 6

Assignment Details
Create a cloud-managed MySQL DB on either Azure or GCP

Create a new database inside of that mysql instance called patient_portal

Create a python script called (sql_table_creation.py) that creates the following tables inside of patient_portal: patients, medications, treatments_procedures, conditions, and social determinants. Be sure to use a .env file to hide your login credentials

Create a python script called (sql_dummy_data.py) using python and send some dummy data into each of the tables. Please see notes for ideas related to dummy data.

Create an ERD for your DB design using MySQL Work Bench. You must have at least two foreignKeys representing a relationship between at least 2 tables.

Github docs to include:

a python script that contains the SQL code to create db (sql_table_creation.py)
a python script that contains code to insert in some dummy data (sql_dummy_data.py)
a readme file that describes a) where you setup the mySQL db, b) any issues you ran into
a images folder that contains:
screen shot of a ERD of your proposed setup (use either popSQL or mysql work bench)
screen shots of you connected to the sql server, performing the following queries:
Query1: show databases (e.g., show databases;)
Query2: all of the tables from your database (e.g., show tables;)
Query3: select * from patient_portal.medications
Query4: select * from patient_portal.treatment_procedures
Query5: select * from patient_portal.conditions
Be CREATE with your dummy data and find examples that are from real-world codexes: Medications: NDC codes Treatments/Procedures: CPT Conditions: ICD10 codes Social_Determinants: LOINC codes

Resources to pull some test data: NDC: https://dailymed.nlm.nih.gov/dailymed/index.cfm CPT: https://www.aapc.com/codes/cpt-codes-range/ ICD: https://icdcodelookup.com/icd-10/codes LOINC: https://www.findacode.com/loinc/LG41762-2--socialdeterminantsofhealth.html

REAL CPT Values that are older: https://gist.github.com/lieldulev/439793dc3c5a6613b661c33d71fdd185

How to set up
You will need to use a .env file with this information to utilize dotenv module
GCP_MYSQL_HOSTNAME = "ip address"
GCP_MYSQL_USERNAME = "root"
GCP_MYSQL_PASSWORD = "password"
GCP_MYSQL_DATABASE = "database"
How to set up Virtual Cloud Environment
I will be using GCP for the assignment but this can also be done using Microsoft Azure Platform

Create a Azure Database for MySQL flexible server:

Please make sure to have require_secure_transport = OFF

Resources used
NDC Codes: https://raw.githubusercontent.com/hantswilliams/FDA_NDC_CODES/main/NDC_2022_product.csv

ICD-10 Codes: https://raw.githubusercontent.com/Bobrovskiy/ICD-10-CSV/master/2020/diagnosis.csv

CPT Codes: https://gist.githubusercontent.com/lieldulev/439793dc3c5a6613b661c33d71fdd185/raw/25c3abcc5c24e640a0a5da1ee04198a824bf58fa/cpt4.csv

LOINC Codes: https://loinc.org/downloads/

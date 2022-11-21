#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dbm
import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


### drop the old tables that do not start with production_
def droppingFunction_limited(dbList, db_source):
    for table in dbList:
        if table.startswith('production_') == FALSE:
            db_source.execute(f'drop table {table}')
            print(f'dropped table {table}')
        else:
            print(f'kept table {table}')

def droppingFunction_all(dbList, db_source):
    for table in dbList:
        db_source.execute(f'drop table {table}')
        print(f'dropped table {table} succesfully!')
    else:
        print(f'kept table {table}')
        
#load environment variables
load_dotenv()

MYSQL_HOSTNAME = os.getenv("MYSQL_HOSTNAME")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

########
#connect to mysql database
connection_string_db = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:3306/{MYSQL_DATABASE}'
db_gcp = create_engine(connection_string_db)


### show tables from databases
tableNames = db_gcp.table_names()

tableNames = ['conditions', 'medications', 'patient_conditions', 'patient_medications', 'patient_social_determinants', 'patient_treatments_procedures', 'patients', 'social_determinants', 'treatments_procedures']
# delelete everthing
droppingFunction_all(tableNames,db_gcp)

### #Set up queries for creating tables
table_prod_patients = """
create table if not exists patients (
    id int auto_increment,
    mrn varchar(255) default null unique,
    first_name varchar(255) default null,
    last_name varchar(255) default null,
    zip_code varchar(255) default null,
    dob varchar(255) default null,
    gender varchar(255) default null,
    contact_mobile varchar(255) default null,
    contact_home varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""
#Medications: NDC codes
table_prod_medications = """
create table if not exists medications (
    id int auto_increment,
    med_ndc varchar(255) default null unique,
    med_human_name varchar(255) default null,
    med_is_dangerous varchar(255) default null,
    PRIMARY KEY (id)
); 
"""

#treatment/procedures: CPT
table_prod_treatments_procedures = """
create table if not exists treatments_procedures (
    id int auto_increment,
    cpt_code varchar(255) default null unique,
    cpt_description varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""

## Conditions: ICD10 codes
table_prod_conditions = """
create table if not exists conditions (
    id int auto_increment,
    icd10_code varchar(255) default null unique,
    icd10_description varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""

##Social_Determinants: LOINC codes
table_prod_social_determinants = """
create table if not exists social_determinants (
    id int auto_increment,
    Loinc_code varchar(255) default null unique,
    Loinc_Description varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""

table_prod_patients_medications = """
create table if not exists patient_medications (
    id int auto_increment,
    mrn varchar(255) default null,
    med_ndc varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (med_ndc) REFERENCES medications(med_ndc) ON DELETE CASCADE
); 
"""
table_prod_patients_social_determinants = """
create table if not exists patient_social_determinants (
    id int auto_increment,
    mrn varchar(255) default null,
    loinc_code varchar(255) default null,
    loinc_description varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (loinc_code) REFERENCES social_determinants(loinc_code) ON DELETE CASCADE
); 
"""
table_prod_patient_conditions = """
create table if not exists patient_conditions (
    id int auto_increment,
    mrn varchar(255) default null,
    icd10_code varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (icd10_code) REFERENCES conditions(icd10_code) ON DELETE CASCADE
); 
"""

table_prod_patients_treatments_procedures = """
create table if not exists patient_treatments_procedures (
    id int auto_increment,
    mrn varchar(255) default null,
    cpt_code varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (cpt_code) REFERENCES treatments_procedures(cpt_code) ON DELETE CASCADE
); 
"""
#Set up queries for creating tables
db_gcp.execute(table_prod_patients)
db_gcp.execute(table_prod_medications)
db_gcp.execute(table_prod_treatments_procedures)
db_gcp.execute(table_prod_conditions)
db_gcp.execute(table_prod_social_determinants) 
db_gcp.execute(table_prod_patients_medications)
db_gcp.execute(table_prod_patient_conditions)
db_gcp.execute(table_prod_patients_treatments_procedures)

# get tables from db_tables
gcp_tables = db_gcp.table_names()


# drop table if existing
#droppingFunction_all(gcp_tables,db_gcp)

### confirm that it worked 
gcp_tables = db_gcp.table_names()


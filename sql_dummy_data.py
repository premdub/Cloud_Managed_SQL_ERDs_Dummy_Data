#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dbm
import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from faker import Faker # https://faker.readthedocs.io/en/master/
import uuid
import random

#load environment variables
load_dotenv()

MYSQL_HOSTNAME = os.getenv("MYSQL_HOSTNAME")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")



connection_string_db = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:3306/{MYSQL_DATABASE}'
db_tables = create_engine(connection_string_db)

### show databases
print(db_tables.table_names())


#### fake stuff 
fake = Faker()

fake_patients = [
    {
        #keep just the first 8 characters of the uuid
        'mrn': str(uuid.uuid4())[:8], 
        'first_name':fake.first_name(), 
        'last_name':fake.last_name(),
        'zip_code':fake.zipcode(),
        'dob':(fake.date_between(start_date='-90y', end_date='-20y')).strftime("%Y-%m-%d"),
        'gender': fake.random_element(elements=('M', 'F')),
        'contact_mobile':fake.phone_number(),
        'contact_home':fake.phone_number()
    } for x in range(50)]

df_fake_patients = pd.DataFrame(fake_patients)
# drop duplicate mrn
df_fake_patients = df_fake_patients.drop_duplicates(subset=['mrn'])
df_fake_patients.head()

######## insert a sample of patients  to mysql database
insertQuery = "INSERT INTO patients (mrn, first_name, last_name, zip_code, dob, gender, contact_mobile, contact_home) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

for index, row in df_fake_patients.iterrows():
    # db_azure.execute(insertQuery, (row['mrn'], row['first_name'], row['last_name'], row['zip_code'], row['dob'], row['gender'], row['contact_mobile'], row['contact_home']))
    db_tables.execute(insertQuery, (row['mrn'], row['first_name'], row['last_name'], row['zip_code'], row['dob'], row['gender'], row['contact_mobile'], row['contact_home']))
    print("inserted row: ", index)

# # query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM patients", db_tables)


#### real icd10 codes
icd10codes = pd.read_csv('https://raw.githubusercontent.com/Bobrovskiy/ICD-10-CSV/master/2020/diagnosis.csv')
list(icd10codes.columns)
icd10codesShort = icd10codes[['CodeWithSeparator', 'ShortDescription']]
icd10codesShort_1k = icd10codesShort.sample(n=1000)
# drop duplicates
icd10codesShort_1k = icd10codesShort_1k.drop_duplicates(subset=['CodeWithSeparator'], keep='first')
icd10codesShort_1k.head()

### insert a sample of icd10 codes to mysql database
insertQuery = "INSERT INTO conditions (icd10_code, icd10_description) VALUES (%s, %s)"

startingRow = 0
for index, row in icd10codesShort_1k.iterrows():
    startingRow += 1
    print('startingRow: ', startingRow)
    db_tables.execute(insertQuery, (row['CodeWithSeparator'], row['ShortDescription']))
    print("inserted row db_gcp: ", index)
    ## stop once we have 100 rows
    if startingRow == 100:
        break

# query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM conditions", db_tables)



#### real ndc codes
ndc_codes = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/FDA_NDC_CODES/main/NDC_2022_product.csv')
ndc_codes_1k = ndc_codes.sample(n=1000, random_state=1)
# drop duplicates from ndc_codes_1k
ndc_codes_1k = ndc_codes_1k.drop_duplicates(subset=['PRODUCTNDC'], keep='first')
ndc_codes_1k.head()

#########insert a sample of medications to mysql database
insertQuery = "INSERT INTO medications (med_ndc, med_human_name) VALUES (%s, %s)"

medRowCount = 0
for index, row in ndc_codes_1k.iterrows():
    medRowCount += 1
    db_tables.execute(insertQuery, (row['PRODUCTNDC'], row['NONPROPRIETARYNAME']))
    print("inserted row: ", index)
    ## stop once we have 50 rows
    if medRowCount == 50:
        break

# query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM medications", db_tables)


#### real CPT codes
cpt_codes = pd.read_csv('https://gist.githubusercontent.com/lieldulev/439793dc3c5a6613b661c33d71fdd185/raw/25c3abcc5c24e640a0a5da1ee04198a824bf58fa/cpt4.csv')
cpt_codes['cpt_code'] = cpt_codes['com.medigy.persist.reference.type.clincial.CPT.code']
cpt_codes.drop(columns=['com.medigy.persist.reference.type.clincial.CPT.code'], inplace=True)
cpt_codes_1k = cpt_codes.sample(n=1000, random_state=1)
# drop duplicates from cpt_codes_1k
cpt_codes_1k = cpt_codes_1k.drop_duplicates(subset=['cpt_code'], keep='first')
cpt_codes_1k.head()

#upload a sample of cptcodes to mysql database
insertQuery = "INSERT INTO treatments_procedures (cpt_code, cpt_description) VALUES (%s, %s)"
cptRow = 0
for index, row in cpt_codes_1k.iterrows():
    cptRow = cptRow + 1
    print("starting row: " + str(cptRow))
    db_tables.execute(insertQuery, row['cpt_code'], row['label'])
    print("inserted row: " + str(cptRow))
    if cptRow == 100:
        break
    
# query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM treatments_procedures", db_tables)


#### real Social Determinant Loinc codes
import pandas as pd
loinc_codes = pd.read_csv('Social_Determinants_.csv', low_memory=False)
# drop duplicates from ndc_codes_1k
loinc_codes = loinc_codes.drop_duplicates(subset=['Loinc_code'], keep='first')
loinc_codes.head()


#upload a sample of icd10 codes to mysql database
insertQuery = "INSERT INTO social_determinants (Loinc_code, Loinc_Description) VALUES (%s, %s)"
loincRow = 0
for index, row in loinc_codes.iterrows():
    loincRow = loincRow + 1
    print("starting row: " + str(loincRow))
    db_tables.execute(insertQuery, row['Loinc_code'], row['Loinc_Description'])
    print("inserted row: " + str(loincRow))
    if loincRow == 20:
        break

# query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM social_determinants", db_tables)


##### Create some fake patient_conditions 

# first, lets query production_conditions and production_patients to get the ids
df_conditions = pd.read_sql_query("SELECT icd10_code FROM conditions", db_tables)
df_patients = pd.read_sql_query("SELECT mrn FROM patients", db_tables)

# create a dataframe that is stacked and give each patient a random number of conditions between 1 and 5
df_patient_conditions = pd.DataFrame(columns=['mrn', 'icd10_code'])
# for each patient in df_patient_conditions, take a random number of conditions between 1 and 10 from df_conditions and palce it in df_patient_conditions
for index, row in df_patients.iterrows():
    # get a random number of conditions between 1 and 5
    # numConditions = random.randint(1, 5)
    # get a random sample of conditions from df_conditions
    df_conditions_sample = df_conditions.sample(n=random.randint(1, 5))
    # add the mrn to the df_conditions_sample
    df_conditions_sample['mrn'] = row['mrn']
    # append the df_conditions_sample to df_patient_conditions
    df_patient_conditions = df_patient_conditions.append(df_conditions_sample)
print(df_patient_conditions.head(20))

# add fake patient conditions to mysql database
insertQuery = "INSERT INTO patient_conditions (mrn, icd10_code) VALUES (%s, %s)"
for index, row in df_patient_conditions.iterrows():
    db_tables.execute(insertQuery, (row['mrn'], row['icd10_code']))
    print("inserted row: ", index)
# query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM conditions", db_tables)

##### now lets create some fake patient_medications

# first, lets query production_medications and production_patients to get the ids

df_medications = pd.read_sql_query("SELECT med_ndc FROM medications", db_tables) 
df_patients = pd.read_sql_query("SELECT mrn FROM patients", db_tables)

# create a dataframe that is stacked and give each patient a random number of medications between 1 and 5
df_patient_medications = pd.DataFrame(columns=['mrn', 'med_ndc'])
# for each patient in df_patient_medications, take a random number of medications between 1 and 10 from df_medications and place it in df_patient_medications
for index, row in df_patients.iterrows():
    # get a random number of medications between 1 and 5
    numMedications = random.randint(1, 5)
    # get a random sample of medications from df_medications
    df_medications_sample = df_medications.sample(n=numMedications)
    # add the mrn to the df_medications_sample
    df_medications_sample['mrn'] = row['mrn']
    # append the df_medications_sample to df_patient_medications
    df_patient_medications = df_patient_medications.append(df_medications_sample)

print(df_patient_medications.head(10))

# now lets add a random medication to each patient
insertQuery = "INSERT INTO patient_medications (mrn, med_ndc) VALUES (%s, %s)"

for index, row in df_patient_medications.iterrows():
    db_tables.execute(insertQuery, (row['mrn'], row['med_ndc']))
    print("inserted row: ", index)


###create a list of fake patient social determinants

#first query database for a list of patients and social determinants
df_patients = pd.read_sql_query('SELECT mrn FROM patients', con=db_tables)
df_social_determinants = pd.read_sql_query('SELECT loinc_code FROM social_determinants', con=db_tables)
#create a stacked dataframe of patients and social determinants
df_patient_social_determinants = pd.DataFrame(columns=['mrn', 'Loinc_code'])
#for each patient, randomly select a random number of social determinants and add to dataframe
for index, row in df_patients.iterrows():
    #randomly select a list of social determinants for each patient
    df_social_determinants_sample = df_social_determinants.sample(n=random.randint(1, 10))
    #add an mrn column to the list of social determinants
    df_social_determinants_sample['mrn'] = row['mrn']
    #add patient and social determinants to dataframe
    df_patient_social_determinants = df_patient_social_determinants.append(df_social_determinants_sample)
print(df_patient_social_determinants.head(20))

#upload fake patient social determinants to mysql database
insertQuery = "INSERT INTO patient_social_determinants (mrn, loinc_code) VALUES (%s, %s)"
for index, row in df_patient_social_determinants.iterrows():
    db_tables.execute(insertQuery, row['mrn'], row['loinc_code'])
    print("inserted row: " + str(index))
    
    # query dbs to see if data is there
df_tables = pd.read_sql_query("SELECT * FROM conditions", db_tables)
    
###generate a list of fake patient procedures and treatments

#first query the database for a list of all patients and conditions
df_patients = pd.read_sql_query("SELECT mrn FROM patients", db_tables)
df_procedures = pd.read_sql_query("SELECT cpt_code FROM treatments_procedures", db_tables)
#create a dataframe that is stacked and gives each patient a random number of conditions between 1 and 10
df_patient_procedures = pd.DataFrame(columns=['mrn', 'cpt_code'])
# for each patient in df_patient_conditions, take a random number of conditions between 1 and 10 from df_conditions and place it in df_patient_conditions
for index, row in df_patients.iterrows():
    # get a random sample of conditions from df_conditions
    df_procedures_sample = df_procedures.sample(n=random.randint(1, 10))
    # add the mrn to the df_conditions_sample
    df_procedures_sample['mrn'] = row['mrn']
    # append the df_conditions_sample to df_patient_conditions
    df_patient_procedures = df_patient_procedures.append(df_procedures_sample)
print(df_patient_procedures.head(20))
#upload fake patient conditions to mysql database
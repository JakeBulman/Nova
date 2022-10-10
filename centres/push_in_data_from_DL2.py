import pandas as pd
import psycopg2
import pyodbc

# Get datalake data
with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
    df = pd.read_sql('''
SELECT name1, eps_centre_id, iso_countryname from cie.ca_centres LIMIT 2
                            ''', conn)

# Amend datalake data (won't be required in future)
df['open_status'] = "True"
df = df.rename(columns={
'ca_centres.name1': 'centre_name',
'ca_centres.iso_countryname': 'country',
'ca_centres.eps_centre_id': 'centre_id'
})

# replacing ' symbol in column so this character does not interfer with SQL command
df['centre_name'] = df['centre_name'].str.replace('\'','')
print(df)

# Push data into Postgres database (DEFAULT in SQL is for auto-increment primary key)
with psycopg2.connect(dbname='myproject', user='bulmaj', host='localhost', password='jman') as conn:
    cursor = conn.cursor()

    for index, row in df.iterrows():
        sql_query = "INSERT INTO public.centres_centres VALUES (DEFAULT, '" + str(row.centre_name) + "', '" + str(row.centre_id) + "', '" + str(row.country) + "', '"+ str(row.open_status) + "')"
        print("Running: " + sql_query)
        cursor.execute(sql_query)

conn.close()






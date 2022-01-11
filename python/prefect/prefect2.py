import requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3
import pandas as pd

from prefect import task, Flow

@task
def get_complaint_data():
    r = requests.get("https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/", params={'size':10})
    json_response = json.loads(r.text)
    return json_response['hits']['hits']

@task
def parse_complaint_data(raw):
     complaints = []
     Complaint = namedtuple('Complaint', ['data_received', 'state', 'product', 'company', 'complaint_what_happened'])
     for row in raw:
        source = row.get('_source')
        this_complaint = Complaint(
            data_received=source.get('date_recieved'),
            state=source.get('state'),
            product=source.get('product'),
            company=source.get('company'),
            complaint_what_happened=source.get('complaint_what_happened')
        )
        complaints.append(this_complaint)
     return complaints

@task
def store_complaints(parsed):
    create_script = 'CREATE TABLE IF NOT EXISTS complaint (timestamp TEXT, state TEXT, product TEXT, company TEXT, complaint_what_happened TEXT)'
    insert_cmd = "INSERT INTO complaint VALUES (?, ?, ?, ?, ?)"

    with closing(sqlite3.connect("cfpbcomplaints.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(create_script)
            cursor.executemany(insert_cmd, parsed)
            conn.commit()

with Flow("etl flow") as f:
    d = get_complaint_data()
    p = parse_complaint_data(d)
    s = store_complaints(p)

f.run()
conn = sqlite3.connect("cfpbcomplaints.db")
table = pd.read_sql_query("SELECT * FROM complaint", conn)
print(table)
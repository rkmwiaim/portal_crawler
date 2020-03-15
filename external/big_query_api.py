import os
from google.cloud import bigquery
import definitions


class BigQueryApi:
  def __init__(self):
    self.service_account_json_file = os.path.join(definitions.RESOURCE_DIR, "youtube-crawler-spreadsheet.json")
    self.client = bigquery.Client.from_service_account_json(self.service_account_json_file)

  def query(self, query):
    query_job = self.client.query(query)
    return query_job.result()
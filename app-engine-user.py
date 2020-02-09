import config
import datetime
import time
from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import datastore
from google.cloud import bigquery

class user:
	def __init__(self,fromID = -1):
		self.ID = request.headers.get('X-Goog-Authenticated-User-ID')
		self.name = request.headers.get('X-Goog-Authenticated-User-Email')
		if self.name != None:
			self.name = str(self.name.split(':')[1])
			self.ID = str(self.ID.split(':')[1])
			self.client = bigquery.Client()
		else:
			if fromID != -1:
				self.ID = fromID
			else:
				self.ID = 'None'
			self.name = ''
	def setupUserDataset(self):
		bq = bigquery.Client()
		from google.cloud.exceptions import NotFound
		try:
			bq.get_dataset(self.ID)
		except NotFound:
			dataset_ref = bq.dataset(self.ID)
			dataset = bigquery.Dataset(dataset_ref)
			dataset.location = "US"
			dataset = bq.create_dataset(dataset)

			access_entries = dataset.access_entries
			access_entries.append(bigquery.AccessEnty('READER', 'groupByEmai',self.name))
			dataset.access_entries = access_entries
			dataset = bq.update_dataset(dataset,['access_entries'])
	def addTable(self,table_name):
		if self.ID != -1:
			self.setupUserDataset()
			bq = bigquery.Client()
			dataset_ref = bq.dataset(self.ID)
			schema = [
				bigquery.SchemaField('id', 'STRING', mode = 'REQUIRED'),
				bigquery.SchemaField('data', 'STRING', mode = 'REQUIRED')
			]
			table_ref = dataset_ref.table(table_name)
			table = bigquery.Table(table_ref, schema = schema)
			table = bq.create_table(table)
			table.table_id == table_name
	def addData(self,table_id,data):
		if self.ID != -1 and data != []:
			bq = bigquery.Client()
			dataset_ref = bq.dataset(self.ID)
			table_ref = dataset_ref.table(table_id)
			table = bq.get_table(table_ref)

			errors = bq.insert_rows(table,data)
	def getData(self,table_id):
		bq = bigquery.Client()
		dataset_ref = bq.dataset(self.ID)
		table_ref = dataset_ref.table(table_id)
		table = bq.get_table(table_ref)

		sql = "SELECT * FROM `{0}.{1}.{2}`".format(config.apiConfig['tasks']['project-id'],self.ID,table_id)
		request = bq.query(sql)
		data = request.result()
		return data


import config
import datetime
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import datastore
from google.cloud import bigquery

class googleDrive:
	def __init__(self):
		self.credentials = service_account.Credentials.from_service_account_file('credentials.json')
		self.datastore = datastore.Client()
	def startDrive(self):
		self.drive = build('drive', 'v3', credentials = self.credentials)
		self.sheets = build('sheets', 'v4', credentials = self.credentials)

	def createSheet(self,name):
		spreadsheet = {'properties': {'title': name}}
		spreadsheet = self.sheets.spreadsheets().create(body = spreadsheet,fields = 'spreadsheetId').execute()
		sheetID = spreadsheet.get('spreadsheetId')
		return sheetID

	def addDataToSheet(self,sheetID,dataRange,data):
		body = {'values':data}
		self.sheets.spreadsheets().values().update(spreadsheetId = sheetID,range = dataRange,valueInputOption = "RAW",body = body).execute()

	def shareFileWithUser(self,fileID,userEmail,message = ''):
		if userEmail != '':
			permissions = self.drive.permissions().create(
				fileId = fileID,
				transferOwnership = False,
				sendNotificationEmail = True,
				emailMessage = message,
				body = {
					'type':'user',
					'role':'writer',
					'emailAddress': userEmail
				}
			).execute()

			self.drive.files().update(fileId = fileID,body = {'permissionIds': [permissions['id']]}).execute()

	def transferToUser(self,fileID,userEmail):
		if userEmail != '':
			permissions = self.drive.permissions().create(
				fileId = fileID,
				transferOwnership = True,
				body = {
					'type':'user',
					'role':'owner',
					'emailAddress': userEmail
				}
			).execute()

			self.drive.files().update(fileId = fileID,body = {'permissionIds': [permissions['id']]}).execute()

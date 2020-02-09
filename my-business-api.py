import os
import httplib2
import json
import argparse
import datetime

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from apiclient.discovery import build
from apiclient import errors

class gmbApi:
	api = None
	def __init__(self):
		self.oathInit()
	def oathInit(self):
		API_NAME = 'mybusiness'
		API_VERSION = 'v4'
		DISCOVERY_URI = 'https://developers.google.com/my-business/samples/{api}_google_rest_{apiVersion}.json'

		parser = argparse.ArgumentParser(parents=[tools.argparser])
		flags = parser.parse_args()
		flow = flow_from_clientsecrets('gmbsecret.json', scope='https://www.googleapis.com/auth/plus.business.manage', redirect_uri='http://localhost:8080/oauth2callback')
		flow.params['access_type'] = 'offline'
		flow.params['approval_prompt'] = 'force'

		storage = Storage('.' + os.path.basename(__file__))
		credentials = storage.get()
		if credentials is not None and credentials.access_token_expired:
			try:
				credentials.refresh(h)
			except:
				pass
		if credentials is None or credentials.invalid:
			credentials = tools.run_flow(flow, storage, flags)	
		http = credentials.authorize(httplib2.Http())
		self.api = build(API_NAME, API_VERSION, http=http, discoveryServiceUrl=DISCOVERY_URI)
	def serviceWorkerInit(self):
		#init API as service worker - not currently working
		jsonLocation = 'gmbapi.json'
		scope = ['https://www.googleapis.com/auth/business.manage']

		DISCOVERY_URI = 'https://developers.google.com/my-business/samples/{api}_google_rest_{apiVersion}.json'
		credentials = service_account.Credentials.from_service_account_file(jsonLocation, scopes = scope, subject = 'example@internet.com')
		delegated_credentials = credentials.with_subject('example@internet.com')

		self.api = discovery.build('mybusiness','v4',credentials = delegated_credentials, discoveryServiceUrl=DISCOVERY_URI)
	def getAccounts(self):
		if self.api != None:
			response = self.api.accounts().list().execute()
			accountData = json.dumps(response)
			print(accountData)
			return accountData

	def getLocations(self,accountID):
		if self.api != None:
			if accountID != '':
				response = self.api.accounts().locations().list(parent='accounts/' + accountID).execute()
				locationData = json.dumps(response)
				print(locationData)
				return locationData
	def getLocationMetrics(self,accountID,locationID,startDate,endDate):
		if self.api != None:
			if accountID != '' and locationID != '':
			
				request = {
					"locationNames":["accounts/" + accountID + "/locations/" + locationID],
					"basicRequest":{
						"metricRequests": [{"metric": "ALL"}],
						"timeRange":{"startTime":startDate,"endTime":endDate}
					}
				}
				response = self.api.accounts().locations().reportInsights(name='accounts/' + accountID,body=request).execute()
				reportData = json.dumps(response)
				print(reportData)
				return reportData
	def getDirectionsRequests(self,accountID,locationID,days):
		if self.api != None:
			if accountID != '' and locationID != '':
				request = {
					"locationNames":["accounts/" + accountID + "/locations/" + locationID],
					"drivingDirectionsRequest":{
						"numDays": days,
						"languageCode": "en"
					}
				}
				response = self.api.accounts().locations().reportInsights(name='accounts/',body=request).execute()
				reportData = json.dumps(response)
				print(reportData)
				return reportData
	def getReviews(self,accountID,locationID):
		if self.api != None:
			if accountID != '' and locationID != '':
				response = self.api.accounts().locations().reviews().list(parent='accounts/' + accountID + '/locations/' + locationID).execute()
				reportData = json.dumps(response)
				print(reportData)
				return reportData
				
g = gmbApi()
g.getAccounts()

accountID = 12345
locationID = 4567

g.getLocations(accountID)
g.getLocationMetrics(accountID,locationID,'2020-01-01T01:01:23.045123456Z','2020-01-01T23:59:59.045123456Z')
g.getDirectionsRequests(accountID,locationID,'NINETY')
g.getReviews(accountID,locationID)

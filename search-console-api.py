import os
import httplib2
import json
import argparse
import datetime
import csv
import calendar

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from apiclient.discovery import build
from apiclient import errors

class gscApi:
	api = None
	site = ''
	def __init__(self,site):
		self.oathInit()
		self.site = site
	def oathInit(self):
		parser = argparse.ArgumentParser(parents=[tools.argparser])
		flags = parser.parse_args()
		flow = flow_from_clientsecrets('secret.json', scope='https://www.googleapis.com/auth/webmasters.readonly', redirect_uri='http://localhost:8080/oauth2callback')
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
		self.api = build('webmasters','v3', http=http)
	def reauth(self):
		parser = argparse.ArgumentParser(parents=[tools.argparser])
		flags = parser.parse_args()
		flow = flow_from_clientsecrets('gmbsecret.json', scope='https://www.googleapis.com/auth/webmasters.readonly', redirect_uri='http://localhost:8080/oauth2callback')
		flow.params['access_type'] = 'offline'
		flow.params['approval_prompt'] = 'force'

		storage = Storage('.' + os.path.basename(__file__))
		credentials = storage.get()

		credentials = tools.run_flow(flow, storage, flags)	
		http = credentials.authorize(httplib2.Http())
		self.api = build('webmasters','v3', http=http)
	def initService(self):
		jsonLocation = 'credentials.json'
		scope = ['https://www.googleapis.com/auth/cloud-platform','email','https://www.googleapis.com/auth/webmasters.readonly',
				'https://www.googleapis.com/auth/userinfo.email'
		   ]
		credentials = service_account.Credentials.from_service_account_file(jsonLocation,scopes=scope,subject='example@internet.com')

		scoped_credentials = credentials.with_scopes(['email'])
		delegated_credentials = credentials.with_subject('example@internet.com')

		service = discovery.build('webmasters','v3',credentials = delegated_credentials)
		print(service)
		siteList = service.sites().list().execute()
		print(siteList)
	def query(self,startDate,endDate,dimensions = [],limit = 25000,start = 0,filters = []):
		request = {
			'startDate':startDate,
			'endDate':endDate,
			'dimensions':dimensions,
			'rowLimit':limit,
			'startRow':start
		}
		if filters != []:
			request['dimensionFilterGroups'] = [{'filters':filters}]
		return self.api.searchanalytics().query(siteUrl=self.site,body=request).execute()

def dailyKeywordsByPage(site,startDate,endDate,csvName):
	g = gscApi(site)
	g.reauth()
	
	thisPage = 0
	maxPages = 100
	
	kwData = []
	while thisPage < maxPages:
		batch = g.query(startDate,endDate,['date','page','query'],25000,(thisPage * 25000))
		#print(batch['rows'])
		kwData.extend(batch['rows'])
		if len(batch['rows']) != 25000:
			break
		thisPage = thisPage + 1
		print(thisPage)
			
	print(len(kwData))
	
	with open(csvName + ' - GSC Daily.csv', 'w', newline = '',encoding='utf8') as csvfile:
		output = csv.writer(csvfile, delimiter=',', quotechar='"')
		csvHeader = ['Date','Page','Query','Clicks','Impressions','CTR','Position']
		output.writerow(csvHeader)
		for thisResult in kwData:
			thisRow = thisResult['keys']
			thisRow.append(thisResult['clicks'])
			thisRow.append(thisResult['impressions'])
			thisRow.append(thisResult['ctr'])
			thisRow.append(thisResult['position'])
			output.writerow(thisRow)

def monthlyKeywordsByPage(site,csvName):
	g = gscApi(site)
	g.reauth()
	maxPages = 50

	dateRange = [	
		[2019,1],
		[2019,2],
		[2019,3],	
		[2019,4],
		[2019,5],
		[2019,6],	
		[2019,7],
		[2019,8],
		[2019,9],	
		[2019,10],
		[2019,11],
		[2019,12]
	]

	exportData = []
	for thisDate in dateRange:
	
		days = calendar.monthrange(thisDate[0],thisDate[1])
		sd = datetime.datetime(thisDate[0],thisDate[1],1)
		ed = datetime.datetime(thisDate[0],thisDate[1],days[1])		

		thisPage = 0
		kwData = []
		while thisPage < maxPages:
			batch =  g.query(sd.strftime("%Y-%m-%d"),ed.strftime("%Y-%m-%d"),['device','page','query'],25000,(thisPage * 25000))
			if 'rows' in batch:
				kwData.extend(batch['rows'])
				if len(batch['rows']) != 25000:
					break
				thisPage = thisPage + 1
				print(thisDate[0],thisDate[1],thisPage)
			else:
				break
		
		exportData.append({'date':str(thisDate[0]) + '-' + str(thisDate[1]),'data': kwData})
		print('Rows -',len(kwData))
	
	with open(csvName + ' GSC Monthly.csv', 'w', newline = '',encoding='utf8') as csvfile:
		output = csv.writer(csvfile, delimiter=',', quotechar='"')
		csvHeader = ['Date','Device','Page','Query','Clicks','Impressions','CTR','Position']
		output.writerow(csvHeader)
		for thisData in exportData:
			for thisResult in thisData['data']:
				thisRow = [thisData['date']]
				thisRow.extend(thisResult['keys'])
				thisRow.append(thisResult['clicks'])
				thisRow.append(thisResult['impressions'])
				thisRow.append(thisResult['ctr'])
				thisRow.append(thisResult['position'])
				output.writerow(thisRow)
				
monthlyKeywordsByPage('https://www.example.com','Example.com GSC Data')

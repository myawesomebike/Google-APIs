import csv
import time

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account

class googleSentimentAnalysis():
	credentials = service_account.Credentials.from_service_account_file('key.json')
	client = language.LanguageServiceClient(credentials = credentials)
	retries = 0
	sentimentData = {}
	
	def processCSV(self,csvPath):
		self.getCSV(csvPath)
	
		for index,thisSentiment in self.sentimentData.items():
			sentiment = self.checkSentiment(thisSentiment[0])
			if(sentiment != None):
				self.sentimentData[index] = [thisSentiment[0],sentiment.score,sentiment.magnitude]
			else:
				break
		self.writeCSV(csvPath)
	
	def checkSentiment(self,text):
		text.strip()
		print('Text: {}'.format(text))
		document = types.Document(
			content = text,
			language = "en",
			type = enums.Document.Type.PLAIN_TEXT)
		
		if(self.retries < 5):
			try:
				sentiment = self.client.analyze_sentiment(document = document).document_sentiment
				return sentiment
			except:
				print("Waiting...")
				time.sleep(1)
				self.retries = self.retries + 1
		else:
			print("Too many requests")
			return None
	
	def getCSV(self,csvPath):
		with open(csvPath, 'r', encoding = "utf-8") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			index = 0
			for row in csv_reader:
				if(len(row) != 0):
					self.sentimentData[index] = [row[0]]
					index = index + 1
	def writeCSV(self,csvPath):
		with open(csvPath, 'w', newline = '', encoding="utf-8") as csvfile:
			output = csv.writer(csvfile, delimiter = ',', quotechar = '"')
			header = ['Content','Sentiment','Magnitude']
			output.writerow(header)
			
			for index,thisString in self.sentimentData.items():
				output.writerow(self.sentimentData[index])
				
s = googleSentimentAnalysis()
s.processCSV('source.csv')

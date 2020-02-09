import csv, time, re, math
from googleads import adwords

class googleKeywordPlanner:
  '''
  Python module to connect to the Google Keyword Planner API and get average search volume
  and 12 month trends for seed keywords read from a CSV
  '''
	locationID = 2840
	languageID = 1000

	keywords = {}
	dateRanges = []
	
	def __init__(self, keywordList = [], getIdeas = False, listName = ''):
		if keywordList != []:
			chunkSize = 700
			chunks = math.ceil(len(keywordList) / chunkSize)
			keywordChunks = []
			for thisChunk in range(0,chunks):
				keywordChunks.append(keywordList[thisChunk * chunkSize:(thisChunk + 1) * chunkSize])
			
			cCount = 0
			for thisChunk in keywordChunks:
				cCount = cCount + 1
				print(cCount,'of',chunks,'- Getting data...')
				self.getData(thisChunk,"STATS")
			if getIdeas == True:
				for thisKW in keywordList:
					self.getData([thisKW],'IDEAS')
		if listName != '':
			self.listName = listName

  '''
  Point to your Google Account YAML file
  '''
	client = adwords.AdWordsClient.LoadFromStorage('googleads.yaml')
	def getData(self,keywordList,requestType):
		targeting_idea_service = self.client.GetService('TargetingIdeaService', version='v201809')

		offset = 0
		results = 1000
		selector = {'ideaType': 'KEYWORD','requestType': requestType}
		selector['requestedAttributeTypes'] = ['KEYWORD_TEXT', 'SEARCH_VOLUME', 'CATEGORY_PRODUCTS_AND_SERVICES', 'TARGETED_MONTHLY_SEARCHES', 'COMPETITION', 'AVERAGE_CPC']
		selector['paging'] = {'startIndex': str(offset),'numberResults': str(results)}
		selector['searchParameters'] = [
			{
				'xsi_type': 'RelatedToQuerySearchParameter',
				'queries': keywordList
			},
			{
				'xsi_type': 'LocationSearchParameter',
				'locations': [{'id': self.locationID}]
			},
			{
				'xsi_type': 'LanguageSearchParameter',
				'languages': [{'id': self.languageID}]
			}
			]
		ideas = None
    
    '''
    Back off requests if the API returns an error
    Add 5 seconds each time we're throttled and give up after 5 attempts
    '''
		retries = 0
		while retries < 4:
			try:
				ideas = targeting_idea_service.get(selector)
				break
			except Exception as e:
				wait = (5 * retries) + 1
				print('API error - waiting',wait,'seconds.',e)
				time.sleep(wait)
				retries = retries + 1
		if ideas != None:
			for thisIdea in ideas['entries']:
				thisKeyword = {}
				for thisResult in thisIdea['data']:
					thisKeyword[thisResult['key']] = getattr(thisResult['value'], 'value', '0')
				kwID = len(self.keywords)
				self.keywords[kwID] = thisKeyword
				if self.dateRanges == []:
					for thisDate in thisKeyword['TARGETED_MONTHLY_SEARCHES']:
						self.dateRanges.append(str(thisDate['month']) + "/" + str(thisDate['year']))
					self.dateRanges.reverse()
			return True
		else:
			return False

	def exportCSV(self):
		with open(self.listName + ' - volume.csv', 'w', encoding='utf-8', newline = '') as csvfile:
			output = csv.writer(csvfile, delimiter=',', quotechar='"')
			csvHeader = ['Keyword','AdWords Categories','Competition','Average CPC','Average Search Volume','YoY Change']
			csvHeader += self.dateRanges
			output.writerow(csvHeader)
			for kwID,thisKeyword in self.keywords.items():
				kwTrend = []
				yoy = 0
				if self.keywords[kwID]['TARGETED_MONTHLY_SEARCHES'] != None:
					for thisMonth in self.keywords[kwID]['TARGETED_MONTHLY_SEARCHES']:
						kwTrend.append(thisMonth['count'])
					kwTrend.reverse()
					if kwTrend[0] != 0 and kwTrend[11] != None:
						yoy = (kwTrend[11] - kwTrend[0]) / kwTrend[0]
				cpc = 0
				if self.keywords[kwID]['AVERAGE_CPC'] != None:
					cpc = self.keywords[kwID]['AVERAGE_CPC']['microAmount'] / 1000000
				thisRow = [
					self.keywords[kwID]['KEYWORD_TEXT'],
					self.keywords[kwID]['CATEGORY_PRODUCTS_AND_SERVICES'],
					self.keywords[kwID]['COMPETITION'],
					cpc,
					self.keywords[kwID]['SEARCH_VOLUME'],
					yoy,
					] + kwTrend
				output.writerow(thisRow)

kwp = googleKeywordPlanner()

csvPath = 'keyword list.csv'

with open(csvPath,'r', encoding = 'utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    kwIdeas = []
    for row in csv_reader:
      kwIdeas.append(row[0])

kwp = googleKeywordPlanner(kwIdeas,False,'Keyword List Volume')
kwp.exportCSV()

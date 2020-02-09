import gfunctions
import config
import datetime
import time
import json
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from google.cloud import datastore
from google.cloud import storage


class task:
	def addToQueue(self):
	    tasks = tasks_v2.CloudTasksClient()
	    in_seconds = None

	    parent = tasks.queue_path(config.apiConfig['tasks']['project-id'],config.apiConfig['tasks']['project-location'],self.taskType)

	    task = {
	        'app_engine_http_request': {
	            'http_method': 'POST',
	            'relative_uri': '**task-handler**'
	        }
	    }
	    if self.reportID != -1:
	        requestBody = str(self.reportID).encode()
	        task['app_engine_http_request']['body'] = requestBody

	    if in_seconds is not None:
	        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

	        timestamp = timestamp_pb2.Timestamp()
	        timestamp.FromDatetime(d)

	        task['schedule_time'] = timestamp

	    response = tasks.create_task(parent, task)

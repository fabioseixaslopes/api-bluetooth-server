import falcon, json, os, time, sys, subprocess, datetime, threading
import training
from threading import Thread

class TrainingResource:
    def on_post(self, req, resp):
       """Handles POST requests"""
       name_thread = 'Bluetooth Peripheral' 
       for thread in threading.enumerate(): #check if a request is already running
           if name_thread in thread.name:
               print('There is another request running, try again later.')
               resp.status = falcon.HTTP_503 #service unavailable
               return
       training_data = json.load(req.stream) #load data
       resp.status = falcon.HTTP_204 # no content
       os.system("sudo service bluetooth restart") #ensure clean bt stack
       t1 = Thread(target = training.main().run_peripheral, args=(training_data['timestamp'],training_data['length'],training_data['score'],training_data['calories'],training_data['repetitions'],training_data['weight']))
       t1.daemon = True
       t1.name = name_thread
       t1.start() #start bluetooth thread
       print('POST Request closed.')

app = falcon.API()
json_file = open(os.path.dirname(__file__) + '/../variables.json', "r")
variables = json.load(json_file)
API_ROUTE = variables["api_route"]
json_file.close()
app.add_route(API_ROUTE, TrainingResource()) 
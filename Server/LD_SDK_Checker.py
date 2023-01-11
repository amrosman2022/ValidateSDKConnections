import socket
import time
import logging
from pprint import pprint
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import reqparse, abort, Api, Resource

retry = 1
delay = 1
timeout = 3
final = []

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                final.append(1)
                return True
        except:
                final.append(0)
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup

def Loop_All_Ports ():
    # LD endpoints to be checked
    Svr_List = ("sdk.launchdarkly.com", "clientstream.launchdarkly.com", "stream.launchdarkly.com", "clientsdk.launchdarkly.com", "events.launchdarkly.com", "mobile.launchdarkly.com",);
    port = 443
    # Clear the results from last time API was called
    final.clear()

    # Cycle through all LD endpoints and check in order. Store results in var: final
    for ip in Svr_List: 
        checkHost(ip, port)
        app.logger.debug(ip)

    pprint(Svr_List)
    #return (final)
    return(Svr_List , final)


#-------------------------------------
# **************** API setup *********
#-------------------------------------
app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

#API First Function Exposed
class Get_LD_SDK_Status(Resource):
    def get(self):
        arrStatus = Loop_All_Ports()
        app.logger.debug(arrStatus)
        return arrStatus[1]
        

#---------------------------------------------------------
## **** Setup the Api resource routing here ****
#---------------------------------------------------------
api.add_resource(Get_LD_SDK_Status, '/')

if __name__ == '__main__':
    app.run(debug=False, port=8080, host='0.0.0.0')

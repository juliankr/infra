import cherrypy
import json
import requests
import os

class MyWebService(object):

  @cherrypy.expose
  @cherrypy.tools.json_out()
  @cherrypy.tools.json_in()
  def send(self):
    data = cherrypy.request.json

    url = os.getenv("SIGNAL_CLI_REST_API_BASE_URL") + "/v2/send"
    message = {"message": json.dumps(data), "number": os.getenv("SOURCE_NUMBER"), "recipients": [os.getenv("TARGET_NUMBER")]}
    x = requests.post(url, json = message)

    return x.text

if __name__ == '__main__':
  config = {'server.socket_host': '0.0.0.0'}
  cherrypy.config.update(config)
  cherrypy.quickstart(MyWebService())

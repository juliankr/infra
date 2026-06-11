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

    # Extract readable information from the alert
    status = data.get("status", "unknown")

    # Get info from the first alert (there could be multiple)
    alerts = data.get("alerts", [])
    if alerts:
        alert = alerts[0]
        labels = alert.get("labels", {})
        room = labels.get("room", "unknown")
        alertname = labels.get("alertname", "unknown")
    else:
        room = "unknown"
        alertname = "unknown"

    # Format a readable message
    readable_message = f"Alert: {alertname}\nRoom: {room}\nStatus: {status.upper()}"

    url = os.getenv("SIGNAL_CLI_REST_API_BASE_URL") + "/v2/send"
    message = {"message": readable_message, "number": os.getenv("SOURCE_NUMBER"), "recipients": [os.getenv("TARGET_NUMBER")]}
    x = requests.post(url, json = message)

    return x.text

if __name__ == '__main__':
  config = {'server.socket_host': '0.0.0.0'}
  cherrypy.config.update(config)
  cherrypy.quickstart(MyWebService())

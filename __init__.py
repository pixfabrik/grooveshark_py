# ----------
# grooveshark_py: A simple module for building Grooveshark API calls.
#
# For more information on the Grooveshark API, see http://www.grooveshark.com/api
#
# This file copyright (c) 2011 Ian Gilman, ian@iangilman.com
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
# ----------

import hmac

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json # works in Google App Engine

# ----------
# build_request
#
# Parameters: 
#   method, ws_key, secret, and session_id are all strings
#   params is a dictionary (possibly nested, e.g. the country param for getSubscriberStreamKey).
#
# Returns a dictionary with 3 strings. 
def build_request(method, params, ws_key, secret, session_id):
  host = "api.grooveshark.com"
  endpoint = "ws3.php"
  protocol = "http"
  if method == "startSession" or method == "authenticate":
    protocol = "https"
    
  header = {"wsKey": ws_key}
  if session_id: 
    header["sessionID"] = session_id
    
  request = {"method": method, "header": header, "parameters": params}
  request_json = json.dumps(request)
  sig = hmac.new(secret, request_json).hexdigest()
  url = "%s://%s/%s?sig=%s" % (protocol, host, endpoint, sig)
  
  return {"url": url, "payload": request_json, "method": "POST"}


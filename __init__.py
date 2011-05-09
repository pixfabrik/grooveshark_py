# ----------
# grooveshark_py: A simple module for building Grooveshark API call URLs.
#
# build_url() is the only function you need; the other two are just helpers for it. 
#
# Note: I'm new to Python, so there may be naive or incomplete bits.
#
# ----------
# LICENSE
#
# The MIT License
#
# Copyright (c) 2011 Ian Gilman, ian@iangilman.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ----------

import hmac

# ----------
# The arguments method, ws_key and secret are all strings, and params is a 
# dictionary (possibly nested, e.g. the country param for getSubscriberStreamKey).
# For more information, see http://www.grooveshark.com/api
def build_url(method, params, ws_key, secret):
  host = "api.grooveshark.com"
  endpoint = "ws/2.1/"

  sig = make_sig(method, params, secret)
  url = "http://%s/%s?method=%s&%s&wsKey=%s&sig=%s&format=json" % \
    (host, endpoint, method, make_param_string(params), ws_key, sig)
  
  return url

# ----------
def make_sig(method, params, secret): 
  data = method 
  
  keys = params.keys()
  keys.sort()
  for key in keys:
    data += key
    value = params[key]
    if (type(value) == dict):
      keys2 = value.keys()
      if (len(keys2)):
        for key2 in keys2:
          data += key2 + value[key2]
    else:
      data += value
    
  return hmac.new(secret, data).hexdigest()

# ----------
# We use this instead of urllib.urlencode, because the latter doesn't handle 
# nested parameters in the fashion the grooveshark API expects. 
def make_param_string(params):
  param_string = ""
  keys = params.keys()
  if (len(keys)):
    keys.sort()
    for key in keys:
      value = params[key]
      if (type(value) == dict):
        keys2 = value.keys()
        if (len(keys2)):
          for key2 in keys2:
            param_string += "%s[%s]=%s&" % (key, key2, value[key2].replace(" ", "+"))
      else: 
        param_string += "%s=%s&" % (key, params[key].replace(" ", "+"))
  
  return param_string.rstrip("&")
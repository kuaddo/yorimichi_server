import os
import urllib.request

baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?{}"

def bykeyword(location, radius, keyword):
  params = {
    'language': 'ja',
    'location': location,
    'radius': radius,
    'keyword': keyword,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format(urllib.parse.urlencode(params)) + '&opennow'
  print(url)
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body
  except urllib.error.HTTPError as err:
    print(err)
  except urllib.error.URLError as err:
    print(err)

def bytype(location, radius, type_value):
  params = {
    'language': 'ja',
    'location': location,
    'radius': radius,
    'type': type_value,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format(urllib.parse.urlencode(params)) + '&opennow'
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body
  except urllib.error.HTTPError as err:
    print(err)
  except urllib.error.URLError as err:
    print(err)

def nextpage(nextToken):
  pass
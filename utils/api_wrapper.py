import os
import urllib.request
import base64

baseurl = "https://maps.googleapis.com/maps/api/place{}?{}"

def bykeyword(location, radius, keyword):
  params = {
    'language': 'ja',
    'location': location,
    'radius': radius,
    'keyword': keyword,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format('/nearbysearch/json', urllib.parse.urlencode(params)) + '&opennow'
  print(url)
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body, 200
  except urllib.error.HTTPError as err:
    print(err)
    return err, 400
  except urllib.error.URLError as err:
    print(err)
    return err, 400

def bytype(location, radius, type_value):
  params = {
    'language': 'ja',
    'location': location,
    'radius': radius,
    'type': type_value,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format('/nearbysearch/json', urllib.parse.urlencode(params)) + '&opennow'
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body, 200
  except urllib.error.HTTPError as err:
    print(err)
    return err, 400
  except urllib.error.URLError as err:
    print(err)
    return err, 400

def nextpage(nextToken):
  pass

def direction(origin, destination):
  params = {
    'origin': origin,
    'destination': destination
  }

  url = 'https://maps.googleapis.com/maps/api/directions/json?{}'.format(urllib.parse.urlencode(params))
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body, 200
  except urllib.error.HTTPError as err:
    return err, 400
  except urllib.error.URLError as err:
    return err, 400

def photo(photoReference, maxWidth, maxHeight):
  params = {
    'photoreference': photoReference,
    'maxwidth': maxWidth,
    'maxheight': maxHeight,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format('/photo', urllib.parse.urlencode(params))
  print(url)
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read()
      return b64string, 302
  except urllib.error.HTTPError as err:
    return err, 400
  except urllib.error.URLError as err:
    return err, 400

if __name__ == '__main__':
  photoReference = "CmRaAAAA6mwU-yVTSziKp6lidH6MnPLMuJ1J9oe_J3uHRlg6uK-n-YtWrCfeAOhJ3JuhZbL6CLvNtzBWMyQx0abVKQK7UUgChVpsqYLhzSkWunLDCSJNK_AlUO8Ddd1vm4JKwSCjEhAp4ERYtaR0ACSh-6CWhMQeGhT9zuyljfUbD1TT3dIQu6WuV536EQ"
  maxHeight = 600
  maxWidth = 600
  content, code = photo(photoReference, maxWidth, maxHeight)
  print(content)
  print(code)

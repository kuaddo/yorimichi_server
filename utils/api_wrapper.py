import os
import urllib.request
import json
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
  params = {
    'pagetoken': nextToken,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format('/nearbysearch/json', urllib.parse.urlencode(params))
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body, 200
  except urllib.error.HTTPError as err:
    return err, 400
  except urllib.error.URLError as err:
    return err, 400

def direction(origin, destination):
  params = {
    'language': 'ja',
    'mode': 'walking',
    
    'origin': origin,
    'destination': destination,
    'key': os.environ['PLACE_API_KEY']
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
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      redirect_url = res.geturl()
      return {'redirect_url': redirect_url}, 302
  except urllib.error.HTTPError as err:
    return err, 400
  except urllib.error.URLError as err:
    return err, 400

def detail(placeid):
  params = {
    'language': 'ja',
    'placeid': placeid,
    'key': os.environ['PLACE_API_KEY']
  }

  url = baseurl.format('/details/json', urllib.parse.urlencode(params))
  req = urllib.request.Request(url)
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      return body, 200
  except urllib.error.HTTPError as err:
    return err, 400
  except urllib.error.URLError as err:
    return err, 400

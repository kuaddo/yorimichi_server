import os
import base64
from datetime import datetime
from google.cloud import storage

def uploadPost(b64image, user_id):
  # Upload a file to the bucket
  storage_client = storage.Client()
  bucket = storage_client.get_bucket('yorimichi_posts')
  destination_blob_name = make_dest_name(user_id)
  blob = bucket.blob(destination_blob_name)

  # create uploadfile from b64
  source_file_name = make_tmp_filename()
  f = open(source_file_name, 'wb')
  f.write(base64.b64decode(b64image))
  f.close()

  # upload
  blob.upload_from_filename(source_file_name)
  # remove tmpfile
  os.remove(source_file_name)
  return {'message': 'succeeded', 'cloud_storage_filename': destination_blob_name}

def downloadPost(bucket_name, stored_filename):
  # Download a file and convert to base64
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(stored_filename)
  tmp_filename = make_tmp_filename()
  f = open(tmp_filename, 'wb')
  blob.download_to_file(f)
  f.close()

  f = open(tmp_filename, 'rb')
  encoded = base64.b64encode(f.read())
  f.close()

  os.remove(tmp_filename)

  return encoded

def make_tmp_filename():
  return os.path.dirname(os.path.abspath(__file__)) + '/tmp' + datetime.now().strftime('%f') + '.png'

def make_dest_name(user_id):
  return str(user_id) + '-' + datetime.now().strftime('%Y%m%d%H%M%S%f') + '.png'
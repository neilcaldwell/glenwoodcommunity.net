import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))


gca_bucket = s3.Bucket('glenwoodcommunity.net')
build_bucket = s3.Bucket('build.glenwoodcommunity.net')
#build_bucket.download_file('gcabuild.zip','c:/Users/Default/Desktop/gcabuild.zip')

site_zip = StringIO.StringIO()
build_bucket.download_fileobj('gcabuild.zip',site_zip)

with zipfile.ZipFile(site_zip) as myzip:
    for nm in myzip.namelist():
        print nm
        obj = myzip.open(nm)
        gca_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        gca_bucket.Object(nm).Acl().put(ACL='public-read')

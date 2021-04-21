# QRCode API

### Installing via this button

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/lab9k/generic-qr-toolkit-ghent&env[DJANGO_SETTINGS_MODULE]=QRcodeAPI.settings.production)

When the project is set up on heroku, you must create a super user. This can be done by pressing the "Run console" button at the top-right. Then typing:
```bash
python manage.py createsuperuser
```
This will take you trough some steps of creating the user (info can be changed later on).

```http request
GET https://api/qrcodes/
```
Returns a list of all the qrcodes with their respective fields in the db.

```http request
GET https://api/qrcodes/<string:uuid>[.html|.json]/
```
When you send a get request to a specific uuid you get the qrcode and it
s fields. There are 2 ways of specifying the return type. Either using a document type at the end of the uuid or by using content negotiation.
When you specify either 

- ```Accept: text/html```
- ```Accept: application/json```

The API will either returned a html page or a json.

### behavior
If only redirect field of a qrcode is set, it will send a redirect to the that url. Unless the accept header is json.

If the information field is filled it will always return a json containing all filled fields.

If the information field is empty and both links are filled, it will also return a json with both links and the title.

```http request
PUT https://api/qrcodes/<string:uuid>/
```
When you use PUT you can update existing qrcodes in the data base by including
a body that has the new model fields ``found in api.models.py`` 
if the qrcode with that uuid exists. Otherwise it will create a new qrcode with a new uuid and insert it into the db.
```http request
POST http://api/qrcodes/<int:n>/
```
This tis the 'batch create' operation. You can either include a 
body in the request that has one or more fields from ``api.models.py`` or no body at all.
The api will then create `n` new empty qrcodes with unique uuid. If a body is 
provided all qrcodes will have these fields populated. The default titles will be set to 
'create by batch operations'. The return value is a list of all the created uuids.


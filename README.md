# CheckIfCovid API

This is a set of endpoints that can be used to access the data. Currently, **Survey App** is the only client but access can be extended to third-party apps.

Endpoint URL: https://28geu7g1z5.execute-api.us-east-2.amazonaws.com/dev

## How to get access
Reach out to us at #proj-findthecluster to request for an API key


---
###  Report Endpoint
Use this endpoint to submit self-reported symptoms.

**Request**

`POST /survey`

**Payload**
```
{"survey_id": "001",
 "user_id": "12345678",
 "report_date": "2020-03-27 12:00:00",
 "report_source": "survey_app",
 "gender": "Female",
 "age": "54",
 "postcode": "07093",
 "country": "United States of America",
 "country_code" : "USA",
 "symptoms": {
 "fever": "False",
 "cough": "True",
 "runny_nose": "false"},
  "travel": [{"country":"Italy","travel_start_date":"2020-03-01", "travel_end_date":"2020-03-26"},{"country":"France","travel_start_date":"2020-03-27", "travel_end_date":"2020-03-31"}]
}
```

**Response**
```
{
  statusCode: 200,
  user_id: xxxx,
  survey_id: yyyy,
  msg: 'Form Submitted'
}
```

---

### Probability Endpoint (coming soon)
Get the probability of a COVID-19 positive given some parameters. 

**Request**

`POST /stats`

**Payload**
```
{"survey_id": "001",
 "user_id": "12345678",
 "report_date": "2020-03-27 12:00:00",
 "report_source": "survey_app",
 "gender": "Female",
 "age": "54",
 "postcode": "07093",
 "country": "United States of America",
 "country_code" : "USA",
 "symptoms": {
 "fever": "False",
 "cough": "True",
 "runny_nose": "false"},
  "travel": [{"country":"Italy","travel_start_date":"2020-03-01", "travel_end_date":"2020-03-26"},{"country":"France","travel_start_date":"2020-03-27", "travel_end_date":"2020-03-31"}]
}
```

**Response**
```
{
  statusCode: 200,
  Diagnose: 'Positive',
  probability: 0.8,
  msg: 'Probability Calculated'
}
```
---

### Technical Details
Below are the specifications for making a POST call to the API from the clients. 

Steps to follow:

1. Get the API Key to make the calls in a secured manner.
2. Use the below url to make POST calls. (GET/PUT in Progress)

| Endpoint | Method | CRUD |Environment | API Link |
| :---    |:---         |     :---:      | :--- |:--- |
| /surver | POST   | Update/Replace   |DEV| https://28geu7g1z5.execute-api.us-east-2.amazonaws.com/dev/survey  |
| /stats  | POST   | Update/Replace   |DEV| https://28geu7g1z5.execute-api.us-east-2.amazonaws.com/dev/stats  |



3. Example curl Call format:
```sql
curl -X POST https://28geu7g1z5.execute-api.us-east-2.amazonaws.com/dev/survey -H 'x-api-key:*******' -H "Content-Type: application/json" -d '{"survey_id": "001","user_id": "12345680","report_date": "2020-03-30 16:00:00", "report_source": "survey_app", "gender": "female","age": "29", "postcode": "122017","country": "INDIA", "country_code" : "INDIA","symptoms": {"fever": "true","cough": "false","runny_nose": "false"},"travel": [{"country":"Italy","travel_start_date":"2020-03-01", "travel_end_date":"2020-03-26"},{"country":"France","travel_start_date":"2020-03-27", "travel_end_date":"2020-03-31"}]}'
```


## Support

Reach out to us at one of the following places!

- Website at <a href="http://findthecluster.com" target="_blank">`findthecluster.com`</a>
- Twitter at <a href="http://twitter.com/findthecluster" target="_blank">`@findthecluster`</a>


---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="http://findthecluster.com" target="_blank">FindTheCluster</a>.

# FindTheCluster API App

## Report Endpoint
Use this endpoint to submit self-reported symptoms

**Request**

`POST /reports`

**Payload**
```
{
 report_source: "survey_app",
 gender: "Female",
 age: "54",
 postcode: "07093",
 country: "USA",
 symptoms: {
   fever: "False",
   cough: "True",
   runny_nose: "false"},
   travel: ["Italy","France"]
  }
}
```

**Response**
```
{
  status: 200
}
```

## Probability Endpoint (coming soon)
Get the probability of a COVID-19 positive based on parameters

**Request**

`POST /reports`

**Payload**
```
{
 report_source: "survey_app",
 gender: "Female",
 age: "54",
 postcode: "07093",
 country: "USA",
 symptoms: {
   fever: "False",
   cough: "True",
   runny_nose: "false"},
   travel: ["Italy","France"]
  }
}
```

**Response**
```
{
  status: 200
  result: 0.8
}
```


## Technical Details
Below are the specifications for making a POST call to the API from the clients. 

Steps to follow:

1. Get the API Key to make the calls in a secured manner.
2. Use the below url to make POST calls. (GET/PUT in Progress)

| Method | CRUD |Environment | API Link |
| :---         |     :---:      | :--- |:--- |
| POST   | Update/Replace   |DEV| https://komyfif1zd.execute-api.us-east-2.amazonaws.com/dev1/reports  |



3. Example curl Call format:
```sql
curl -X POST https://komyfif1zd.execute-api.us-east-2.amazonaws.com/dev1/reports -H 'x-api-key:********' -H "Content-Type: application/json" 
-d '{"report_date": "2020-03-23 16:00:00", "report_source": "survey_app", "gender": "male","age": "29", "postcode": "122017","country": "USA","symptoms": {"fever": "true","cough": "false","runny_nose": "false"},"travel": ["London"]}'
```

Payload:(Finalize with Survey Team)

```js

{"report_date": "2020-03-27 12:00:00",
 "report_source": "survey_app",
 "gender": "Female",
 "age": "54",
 "postcode": "07093",
 "country": "USA",
 "symptoms": {
 "fever": "False",
 "cough": "True",
 "runny_nose": "false"},
  "travel": ["Italy","France"]
}
```

Response text (WIP): 
```
Status code 200
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

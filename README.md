# PathFinder

This application is path computing web service.
Written in Python with Falcon Library

#API:
**All responses are in json format**
- '/path/{start}/{finish}'

  - HTTP GET - get path from start to finish and distance

  - DELETE - remove connection between cities
- '/path/{start}/{finish}/{distance}'

  - HTTP POST - add connection between cities 

  - PUT - update connection between cities
- '/cities'

  - HTTP GET - returns all cities
  
#Example: 
>Server running on loacalhost:5000

>get path from Warszawa to Kraków

>http get localhost:5000/path/Warszawa/Kraków

>response will be:

    {
        "distance": 295.1, 
        "finish": "Kraków", 
        "path": [
            "Warszawa", 
            "Kielce", 
            "Kraków"
        ], 
        "start": "Warszawa"
    }

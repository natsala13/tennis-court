# Tennis court reverse API

## How to use
`pip install -r requirements.txt`

* Update `configs/court_preferences.yaml` with the courts you like, days and hours.
* A list of courts id can be found here at the end of the readme.

`python lazuz/find_courts.py`


## Reproduce reverse
* Using proxy mitmproxy from "https://github.com/mitmproxy/mitmproxy.git".

Using transparent HTTPS mode with flag "--set tls_version_client_min=TLS1"

Download Iphone certificate - for some reason downloading iphone certificate didn't work, but downloading Android one on my iphone worked.
* Correction - iphone certificate worked for me last time.
* may have to remove the old certificate and download again. to remove it - go to settings -> general -> vpn...

![Alt text](transparent_https_mitm.png)


https://docs.mitmproxy.org/stable/howto-transparent/

Follow this steps to enable forwroding any HTTP / HTTPS scommunication to computer to the proxy.




## Reasearch results..
* Get list of all clubs
https://server.lazuz.co.il/client-app/club-list/?lng=34.77248220695786&lat=32.08339617836291&date=2024-10-26&duration=60&category=1

doesn't work directly from browser...
example can be seen under examples/club_list_example.json.


* Get list of all available clubs
https://server.lazuz.co.il/client-app/clubs-by-ids/?clubIds=66,139,54,55,106,65,53,21,189,64&duration=60&date=2024-10-26&court_type=3&category=1

example can be seen under examples/club_available_example.json


* Weird available request I didn't understand
https://server.lazuz.co.il/client-app/ext/clubs/availble/?clubIds=66,139,54,55,106,65,53,21,189,64&date=2024-10-26&duration=60&court_type=3



* Get rent rate per hour of a given club

https://server.lazuz.co.il/client-app/rent-rate/?club_id=66&date=2024-10-26


* Get available slots per club (per court)

https://server.lazuz.co.il/client-app/club/availble-slots/?club_id=66&date=2024-10-26&duration=60&court_type=3&external_club_id=null&from_time=14:00:00


* Get app settings of the club
https://server.lazuz.co.il/client-app/club-settings/?club_id=66&external_api_id=null

This can be usefull when trying to understand when should I reserve each court.



## Resending messages
* In order to send the messages above, the correct headers and query params need to be sent.
* examples can be seen in files `query.file` and `headers.file`. attach them to the matching url (see example in sandbox) and I got the response.

* authentication token needs to be joined to that.

## Authentication
* Authentication is done via the help of google FCM - Firebase Cloud Messaging.
* The app acess two apis although only one of them looks helpfull - `https://fcmtoken.googleapis.com/register` that returns some sort of token.
Then I access the api server.lazuz.co.il/users/token and I send it a new token and receive another one ??? where from?? 


## Court ids

* Court id 66 is Rokah 4
* Court id 139 is Rokah 67
* Court 54 is Country Dekel
* Court 106 is Shikun Vatikim
* Court 55 is Yad Eliyahu
* Court 177 is Country Rannana
* Court 123  is Ranana Edan Leshem
* Court 125 is Ranana Tennis way 
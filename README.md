# sdwan
Cisco SDWAN API Calls Examples
We are building an use case for Geofencing. In this case the use case is just capturing the vManage ip address, username/password
With the conection to vManage we could get the Geolocation and a google map fill markers per site
With other code under construction we are going to monitor the Geolocation by calls to vEdge100M of cEdge1100 with LTE modem where googlemaps api
could help to determine the exact location (200m accuracy) then launch a button in the main portal (Python with Flask) to disable Risky sytes.
Prior to start usign this code please install a viptela library from bobthebutcher github repository : 
pip install https://github.com/bobthebutcher/viptela/archive/master.zip

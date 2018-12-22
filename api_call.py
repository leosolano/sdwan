import json
import urllib3
#import xlsxwriter

urllib3.disable_warnings()
from pprint import pprint
from viptela.viptela import Viptela
from flask import Flask, render_template, request, session
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from geopy.geocoders import Nominatim

geolocator = Nominatim()

app = Flask(__name__)
GoogleMaps(app, key="AIzaSyD1FwM3UF_1em5FURznQX06cp3vgkAGPWE")

system_ip_list = []



def get_device_list(v):
#Get the system-ip list of  vEdges in the whole network + coordinates
    device_dic = v.get_all_devices()
    device_list = device_dic[4]
    devices_all = []
    for devices in device_list:
        system_ip=devices.get('local-system-ip', None)
        lat = float(devices.get('latitude', None))
        long =float(devices.get('longitude', None))
        hostname =devices.get('host-name', None)
        location= geolocator.reverse(str(lat)+","+str(long))
        devices_all.append((hostname,system_ip,lat,long,location))
    return devices_all

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/geo-fencing.html')
def geo():
    global system_ip_list
    rel_lat=system_ip_list[0][2]
    rel_lng=system_ip_list[0][3]
    # creating a map in the view
    markers1=[]
    for items in system_ip_list:
        markers1.append(
        {
         'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
         'lat': items[2],
         'lng': items[3],
         'infobox': items[0]  
        }  
        )
    pprint (markers1)
    sndmap = Map(
        identifier="sndmap",
        lat=rel_lat,
        lng=rel_lng,
        markers=markers1,
        zoom = 6,
        style="height:500px;width:700px;margin:0;"
    )
        
    ##return render_template('geo-fencing.html',result =system_ip_list)
    return render_template('geo-fencing.html', sndmap=sndmap)


@app.route('/geo-fencing-risky.html')
def geo_risk():
    global system_ip_list
    rel_lat=system_ip_list[0][2]
    rel_lng=system_ip_list[0][3]
    # creating a map in the view
    markers1=[]
    markers1.append(
    {
    'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
    'lat': system_ip_list[0][2],
    'lng': system_ip_list[0][3],
    'infobox': system_ip_list[0][0]  
    }  
    )
    sndmap = Map(
        identifier="sndmap",
        lat=rel_lat,
        lng=rel_lng,
        markers=markers1,
        zoom = 6,
        style="height:500px;width:700px;margin:0;"
    )
        
    ##return render_template('geo-fencing.html',result =system_ip_list)
    return render_template('geo-fencing-risky.html', sndmap=sndmap)

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/uses.html')  
def uses():
    return render_template('uses.html' ,result =[])

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit_textarea():
    global system_ip_list
    credentials =	{
        "vmanageip": "",
        "username": "",
        "password": ""
        }
    credentials["vmanageip"] = format(request.form["vManageIP"])
    credentials["username"] = format(request.form["Username"])
    credentials["password"] = format(request.form["Password"])

    v = Viptela(user=credentials["username"], user_pass=credentials["password"], vmanage_server=credentials["vmanageip"])
    system_ip_list = get_device_list(v)


    return render_template("uses.html",result =system_ip_list)


@app.route('/disable_WAN_Edge', methods=['POST'])
def disable_textarea():
    global system_ip_list
    local_uuid = system_ip_list[0][0]
    

    return render_template("geo-fencing-risky.html",result =system_ip_list)

if __name__ == '__main__':
    app.run()








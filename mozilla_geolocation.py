"""
    wifi-based geolocation, using Mozilla's service
    
    @author github.com/ZsBT
"""
from ubinascii import hexlify
import urequests,ujson

def mozilla_geolocation( wlan_scan, apikey='test'):
    waps = {'wifiAccessPoints':[]}
    for ap in wlan_scan:
        (ssid,bssid,channel,strength,auth,hidden) = ap
        details = {}
        mac = hexlify(bssid).decode()
        details['macAddress'] = '%s:%s:%s:%s:%s:%s' % (mac[0:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:12])
        details['signalStrength'] = strength
        details['channel'] = channel
        #details['age'] = 1
        waps['wifiAccessPoints'].append(details)
    
    return urequests.post('https://location.services.mozilla.com/v1/geolocate?key='+apikey, data=ujson.dumps(waps).encode('utf-8') ).json()['location']


def google_maps_link( geolocation ):
    return 'https://www.google.com/maps/@%s,%s,20z' % (geolocation['lat'],geolocation['lng'] )


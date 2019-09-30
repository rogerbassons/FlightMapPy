from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from opensky_api import OpenSkyApi
import time
import ctypes
import os
import subprocess

LON = 2.80
LAT = 41.98
DPI = 400

def getFlights(bbox):
    states = []
    api = OpenSkyApi()
    lon = []
    lat = []
    j = 0
    # bbox = (min latitude, max latitude, min longitude, max longitude)
    try:
        states = api.get_states(bbox=bbox).states
    except:
        time.sleep(30)

    if (len(states) == 0):
        return getFlights(bbox)

    return states


minLat = LAT - 1
maxLat = LAT + 1
minLon = LON - 3
maxLon = LON + 3

bbox = (minLat + 0.2, maxLat - 0.2, minLon + 0.2, maxLon - 0.2)

plt.figure(figsize=(12, 12))
m = Basemap(projection="mill", resolution="i", llcrnrlon=minLon,llcrnrlat=minLat,urcrnrlon=maxLon,urcrnrlat=maxLat)

m.drawcoastlines(linewidth=1, color="white")
m.drawmapboundary(fill_color='black')

points = []
while True:
    for point in points:
        try:
            point.remove()
        except:
            pass

    flights = getFlights(bbox)

    for f in flights:
        lon = f.longitude
        lat = f.latitude

        speed = f.velocity * 3.6 / 1.852

        altitude = "0"
        if (f.baro_altitude):
            altitude = str(int(round(f.baro_altitude * 3.2908) / 100))

        if (len(altitude) <= 2):
            altitude = "0" + altitude
        altitude = "F" + altitude

        if (f.vertical_rate == None):
            pass
        elif (f.vertical_rate > 0):
            altitude = "↑" + altitude
        elif (f.vertical_rate < 0):
            altitude = "↓" + altitude

        text = f.callsign + '\n' + altitude + " " + str(int(round(speed))) 

        x, y = m(lon, lat)
        markerX, markerY = m(lon + 0.01, lat + 0.01)
        point = m.scatter(x, y, s = 1, color="green")
        marker = plt.text(markerX, markerY, text, color="green", fontsize = 4)

        points.append(point)
        points.append(marker)
   
    plt.axis('off')
    plt.savefig("wallpaper.png", format='png', bbox_inches='tight', dpi=DPI, pad_inches = 0)
    
    path = os.path.abspath("wallpaper.png")
    try:
        import win32con
        changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER,0,path,changed)
    except:
        subprocess.run(["feh", "--bg-fill", path])

    time.sleep(20)


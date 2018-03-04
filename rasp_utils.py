from myutils import *

french_stations=['R9F1B','RE4C0','R57C7','R0B29','RA3B7']
french_stations=['R9F1B','RE4C0']
french_stations=['R9F1B','R0B29','RA3B7']
NODATA=('R6E96','R052F','R1FBA','RB511','SFD6B', 'RA70D','R9DA3','R5661','RE7F9','R9DBD','R3F3B')

STATIONBOOK="%s/stations_raspberryshake.txt" % DATADIR
print "STATIONBOOK=%s" % STATIONBOOK

HOST1="gmazet.freeboxos.fr"
HOST2="manchot.emsc-csem.org"
HOST3="rtserve.iris.washington.edu"
HOST4="rtserver.ipgp.fr"
HOST5="geofon.gfz-potsdam.de"
HOST6="geosrt1.ipgp.fr"
HOST6="eida.ipgp.fr"
HOST7="caps.raspberryshakedata.com"
HOST8="fdsnws.raspberryshakedata.com"

RASP_NET="AM"
RASP_LOCALCODE="00"
RASP_CHANNEL="SHZ"
RASP_HOST=HOST8

BEFORE=10

#-------------------------------------------------------------------
def counts2Amp (c): #Only for Raspberryshake data (not reliable)
    # Av=470*c ( 470 counts ~ 1 um/s according to sensor sensentivity provided by sensor technical specs)
    # log(Ad/T)=Av/2pi and  T ~ 1.0 sec
    Av=float(c)/470
    Ad=pow(10,(Av/(2*pi)))
    return Av,Ad
    
# Build station book
# ------------------
def build_station_book(ev):
    fsta=open(STATIONBOOK,'r')
    ALLSTATIONS=[]
    i=0
    for line in fsta:
        sta=req_station()
        sta.lat,sta.lon,sta.elevation=float(line.split()[1]),float(line.split()[2]),float(line.split()[3])
        sta.get_epidist(ev.lat,ev.lon)
        sta.network, sta.name,  sta.location, sta.channel, sta.slserver = RASP_NET,line.split()[0], RASP_LOCALCODE,RASP_CHANNEL,RASP_HOST
        i+=1
        ALLSTATIONS.append((sta.network, sta.name, sta.location, sta.channel, sta.lat, sta.lon, sta.elevation, sta.slserver,sta.epidist_deg,sta.azimuth))
    
    fsta.close()

    """
    # Add CLF
    lat,lon,elev=48.025790,2.26,100
    D,Az1,Az2=gps2dist_azimuth(lat,lon, ev.lat, ev.lon)
    ALLSTATIONS.append(("G","CLF","00", "BHZ", lat,lon,elev,"SDS",D/1000*km2deg, Az2))
    # Add LOR
    lat,lon,elev=47.2683,3.8589, 300.0
    D,Az1,Az2=gps2dist_azimuth(lat,lon, ev.lat, ev.lon)
    ALLSTATIONS.append(("RD","LOR","", "BHZ", lat,lon,elev,"SDS",D/1000*km2deg, Az2))
    """

    ALLSTATIONS=array(ALLSTATIONS,dtype=([('network', 'S5'),('name', 'S10'), ('location', 'S5'), ('channel', 'S10'), ('lat', 'f4'), ('lon', 'f4'), ('elevation,', 'f4'), ('slserver', 'S30'), ('epidist_deg', 'f4'), ('azimuth', 'f4') ]))
    isortbydist=argsort(ALLSTATIONS['epidist_deg'])
    CLOSE_STATIONS= ALLSTATIONS[isortbydist]

    FR_STATIONS=[]
    for sta in ALLSTATIONS:
        if (sta['name'] in french_stations):
            FR_STATIONS.append(sta)

    return CLOSE_STATIONS,FR_STATIONS

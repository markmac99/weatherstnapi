import xml.etree.ElementTree as ET


def getData():
    tree=ET.parse('/home/pi/weather/temp/output/yowindow.xml')
    root=tree.getroot()
    temps=[c for c in root[0] if c.tag=='temperature']
    sky=[c for c in root[0] if c.tag=='sky']
    wind=[c for c in root[0] if c.tag=='wind']
    rain_id = [t for t in sky[0][0] if t.tag=='rain']

    temp_out = [t for t in temps[0] if t.tag=='current'][0].attrib['value']
    temp_in = [t for t in temps[0] if t.tag=='indoor'][0].attrib['value']
    hum_out = [c for c in root[0] if c.tag=='humidity'][0].attrib['value']
    press = [c for c in root[0] if c.tag=='pressure'][0].attrib['value']
    rainrate = [t for t in rain_id[0] if t.tag=='rate'][0].attrib['value']
    windspeed = [c for c in wind[0] if c.tag=='speed'][0].attrib['value']
    winddir = [c for c in wind[0] if c.tag=='direction'][0].attrib['value']
    windgust = [c for c in wind[0] if c.tag=='gusts'][0].attrib['value']

    reslist = {"temp_out": temp_out, "temp_in": temp_in, 
        "rel_pressure": press, "rain": rainrate,
        "hum_out": hum_out, "wind_ave": windspeed, "wind_dir": winddir, 
        "wind_gust": windgust}
    print(reslist)
    return reslist


def getOutsideTemp():
    with open('/home/pi/weather/temp/output/dragontailcurrenttemp.txt', 'r') as inf:
        li = inf.readline()
    tempval = li.split(' ')[0]
    reslist={"temp_out": tempval}
    return reslist


if __name__ == '__main__':
    res = getData()
    print(res['tempout'])

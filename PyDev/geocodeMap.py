#coding: utf-8

import urllib
from xml.etree.ElementTree import parse
 
def adr2geo(adr):
    api = "http://www.geocoding.jp/api/?v=1.1&q=%s" % (urllib.quote(adr.encode('utf-8')))
    xml = parse(urllib.urlopen(api)).getroot()
 
    lat = xml.find('coordinate/lat').text
    lng = xml.find('coordinate/lng').text
    return (float(lat), float(lng))
 
def main():
    print adr2geo(u'東京都板橋区徳丸３－１１－１')
 
if __name__ == '__main__':
    main()
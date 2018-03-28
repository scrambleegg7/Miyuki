#coding: utf-8
from jinja2 import Template
from readCSVF import readFileCSVEXCEL  

def readGeocode():
    codes_ = []
    gfile = "c:\\temp\\geocoder.txt"
    fh_ = readFileCSVEXCEL(gfile,False)
    for rr in fh_:
        codes_.append((rr[0],rr[1],rr[2]))
    return codes_

def process():
    file = "c:\\temp\\temp.html" 
    with open(file, "r") as f:
        template = Template(f.read().decode('utf-8'))

    f = open('c:\\temp\\javascr_loop_.txt', 'w')
    f.write("var markers = new Array(\n") 
    codes_ = readGeocode()
    for item in codes_:
        print item[0],item[1],item[2]
        str1 = "{ name: \"" + str(item[0]) + "\",\n"
        f.write(str1)
        str2 = "  latlng: new google.maps.LatLng(" + str(item[1]) + "," + str(item[2]) + "),\n"
        f.write(str2)
        str3 = "  content: \"" + str(item[0]) + "\"\n"
        f.write(str3)
        str4 = "},\n"
        f.write(str4)
    f.write(");")    
    #outfile = "c:\\temp\\output.html" 
    #with open(outfile, "w") as f:
    #    f.write(html.encode('utf-8'))
    
def main():
    process()
    
if __name__ == "__main__":
    main()
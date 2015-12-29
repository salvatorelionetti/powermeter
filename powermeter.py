#Pushing data to Thingspeak
import httplib, urllib
import os, sys

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getPowerConsumed():
    ret = -10
    cmd = os.popen('/home/pi/projects/powermeter/a.out 0x5B14 2')
    for line in cmd.readlines():
        #reg[1]=13175
        line1 = line.replace('reg[1]=','')
        if line1 != line:
            ret = int(line1.split()[0])
    return ret

def getPowerAccumulated():
    ret = -100
    cmd = os.popen('/home/pi/projects/powermeter/a.out 0x5000 4')
    for line in cmd.readlines():
        #reg[1]=13175
        line1 = line.replace('reg[3]=','')
        if line1 != line:
            ret = int(line1.split()[0])
    return ret

def getFrequency():
    ret = -50
    cmd = os.popen('/home/pi/projects/powermeter/a.out 0x5b2c 1')
    for line in cmd.readlines():
        #reg[1]=13175
        line1 = line.replace('reg[0]=','')
        if line1 != line:
            ret = int(line1.split()[0])
    return ret

def getPowerFactor():
    ret = -50
    cmd = os.popen('/home/pi/projects/powermeter/a.out 0x5b3a 1')
    for line in cmd.readlines():
        #reg[1]=13175
        line1 = line.replace('reg[0]=','')
        if line1 != line:
            ret = int(line1.split()[0])
    return ret

def getPowerFailCnt():
    ret = -50
    cmd = os.popen('/home/pi/projects/powermeter/a.out 0x8a2f 1')
    for line in cmd.readlines():
        #reg[1]=13175
        line1 = line.replace('reg[0]=','')
        if line1 != line:
            ret = int(line1.split()[0])
    return ret

T = getCPUtemperature()
W = getPowerConsumed()
tot = getPowerAccumulated()
f = getFrequency()
powerFactor = getPowerFactor()
powerFailCnt = getPowerFailCnt()

totKm1_fileName = '/tmp/totKm1'
totKm1 = None

# Read previous consumed energy
try:
    with open(totKm1_fileName, 'r') as totKm1_file:
        totKm1 = int(totKm1_file.read())
except IOError as e:
    print("Reading ({})".format(e))

# Save current consumed energy
try:
    if totKm1 is None or tot != totKm1:
        with open(totKm1_fileName, 'w') as totKm1_file:
            totKm1_file.write(str(tot))
except IOError as e:
    print("Writing ({})".format(e))

powerFailCntKm1_fileName = '/tmp/powerFailCntKm1'
powerFailCntKm1 = None

# Read previous power fail count
try:
    with open(powerFailCntKm1_fileName, 'r') as powFailCntKm1_file:
        powerFailCntKm1 = int(powFailCntKm1_file.read())
except IOError as e:
    print("Reading powerFailCnt ({})".format(e))

# Save current power fail cnt
try:
    if powerFailCntKm1 is None or powerFailCnt != powerFailCntKm1:
        with open(powerFailCntKm1_fileName, 'w') as powFailCntKm1_file:
            powFailCntKm1_file.write(str(powerFailCnt))
except IOError as e:
    print("Writing powerFailCnt ({})".format(e))

dict = {}
dict['field1'] = W
dict['field2'] = T
if totKm1 is None or tot != totKm1:
    dict['field3'] = tot
if totKm1 is None:
    dict['field4'] = -200
elif tot != totKm1:
    dict['field4'] = tot - totKm1
dict['field5'] = f
dict['field6'] = powerFactor
if powerFailCnt is None or powerFailCnt != powerFailCntKm1:
    dict['field7'] = powerFailCnt

print dict

dict['key'] = 'I7JZQRT6TT4NVWAE'

sortedKeys = sorted(dict)
params = urllib.urlencode([(x, dict[x]) for x in sortedKeys])
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("api.thingspeak.com:80", timeout=30)
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()

from sys import argv
import urllib2

# for use with 'TV calendar' from http://www.pogdesign.co.uk/cat/

catid = argv[1]
urlroot = 'http://www.pogdesign.co.uk/cat/generate_ics/'
ical = urllib2.urlopen(urlroot+catid)

# static locations for now..

currentcal = ical.read().splitlines()
calheader, calfooter = currentcal[:9], currentcal[-1:]
currentcal = currentcal[9:-1]

# '\n'.join(currentcal).split('BEGIN:VEVENT')



events = {}
while 1:
	try:
		endindex = currentcal.index('END:VEVENT')
		event = currentcal[:endindex+1]
		for line in event:
			if 'UID' in line:
				uid = line
		events[uid] = '\n'.join(currentcal[:endindex+1])
		del currentcal[:endindex+1]
	except:
		break



updatedcal = open('tv.ical','w')
listevents = events.keys()
updatedcal.write('\n'.join(calheader))
updatedcal.write('\n')
for evt in listevents:
	updatedcal.write(events[evt])
	updatedcal.write('\n')
updatedcal.write('\n'.join(calfooter))
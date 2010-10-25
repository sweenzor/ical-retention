from sys import argv
import os
import urllib2

# for use with 'TV calendar' from http://www.pogdesign.co.uk/cat/

# breaks ical file apart into events
def parse_ical(cal,dict):
	while 1:
		try:
			endindex = cal.index('END:VEVENT')
			event = cal[:endindex+1]
			for line in event:
				if 'UID' in line:
					uid = line
			dict[uid] = '\n'.join(cal[:endindex+1])
			del cal[:endindex+1]
		except:
			break

# read (or create) local cal
events = {}
if os.path.isfile('tv.ical'):
	oldcalfid = open('tv.ical','r')
	oldcal = oldcalfid.read().splitlines()
	oldcal = oldcal[9:-1]
	parse_ical(oldcal,events)

# pull freshest cal from web
catid = argv[1]
urlroot = 'http://www.pogdesign.co.uk/cat/generate_ics/'
ical = urllib2.urlopen(urlroot+catid)

# remove header/footer, static locations for now..
currentcal = ical.read().splitlines()
calheader, calfooter = currentcal[:9], currentcal[-1:]
currentcal = currentcal[9:-1]

parse_ical(currentcal,events)

# write dict of events back out to file
updatedcal = open('tv.ical','w')
listevents = events.keys()
updatedcal.write('\n'.join(calheader))
updatedcal.write('\n')
for evt in listevents:
	updatedcal.write(events[evt])
	updatedcal.write('\n')
updatedcal.write('\n'.join(calfooter))
import os
import argparse
import syslog
import urllib2


# breaks ical file apart into events
def parse_ical(cal,dict):
	while True:
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

if __name__=='__main__':

	# command line argument handler
	parser = argparse.ArgumentParser()
	parser.add_argument('url')
	parser.add_argument('out')
	args = parser.parse_args()

	# read (or create) local cal
	events = {}
	if os.path.isfile(args.out+'.ical'):
		oldcalfid = open(args.out+'.ical','r')
		oldcal = oldcalfid.read().splitlines()
		oldcal = oldcal[9:-1]
		parse_ical(oldcal,events)
		oldcalfid.close()

	# pull freshest cal from web
	ical = urllib2.urlopen(args.url)

	# remove header/footer, static locations for now..
	currentcal = ical.read().splitlines()
	calheader, calfooter = currentcal[:9], currentcal[-1:]
	currentcal = currentcal[9:-1]

	parse_ical(currentcal,events)

	# write dict of events back out to file
	updatedcal = open(args.out+'.ical','w')
	listevents = events.keys()
	updatedcal.write('\n'.join(calheader))
	updatedcal.write('\n')
	for evt in listevents:
		updatedcal.write(events[evt])
		updatedcal.write('\n')
	updatedcal.write('\n'.join(calfooter))
	updatedcal.close()

	# check size, write to syslog
	filesize = os.path.getsize(args.out+'.ical')
	syslog.syslog(args.out+'.ical '+str(filesize))
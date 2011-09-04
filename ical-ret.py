import os
import argparse
import syslog
import urllib2
from datetime import datetime, date


# breaks ical file apart into events
def parse_ical(calendar,dict):
	cal = calendar[:]
	while True:
		try:
			endindex = cal.index('END:VEVENT')
			event = cal[:endindex+1]
			for line in event:
				if 'UID' in line:
					uid = line
				if 'START' in line:
					entry_date = line[8:-7]
			dict[uid] = [entry_date, '\n'.join(cal[:endindex+1])]
			del cal[:endindex+1]
		except:
			break

def expire_entries(dict,duration):
	for key, entry in dict.items():
		entry_date = datetime.strptime(entry[0], '%Y%m%d')
		delta = datetime.today() - entry_date
		if (int(delta.days) >= int(duration)):
			del dict[key]

def pretty_ical(dict):
	for entry in dict:
		print entry


if __name__=='__main__':

	# command line argument handler
	parser = argparse.ArgumentParser()
	parser.add_argument('url')
	parser.add_argument('out')
	parser.add_argument('expire')
	args = parser.parse_args()

	# read (or create) local cal
	events = {}
	if os.path.isfile(args.out+'.ical'):
		oldcalfid = open(args.out+'.ical','r')
		oldcal = oldcalfid.read().splitlines()
		oldcal = oldcal[9:-1]
		parse_ical(oldcal,events)
		oldcalfid.close()
	print 'local calendar contains '+ \
		str(len(events))+ ' events.'

	#expire old entries
	expire_entries(events, args.expire)
	print 'local calendar contains '+ \
		str(len(events))+ ' events.'

	# pull freshest cal from web
	ical = urllib2.urlopen(args.url)

	# remove header/footer, static locations for now..
	remote_events = {}
	currentcal = ical.read().splitlines()
	calheader, calfooter = currentcal[:9], currentcal[-1:]
	currentcal = currentcal[9:-1]
	
	parse_ical(currentcal,remote_events)
	print 'remote calendar contains '+ \
		str(len(remote_events))+ ' events.'

	parse_ical(currentcal,events)
	print 'local calendar now contains '+ \
		str(len(events))+ ' events.'

	# write dict of events back out to file
	updatedcal = open(args.out+'.ical','w')
	listevents = events.keys()
	updatedcal.write('\n'.join(calheader))
	updatedcal.write('\n')
	for evt in listevents:
		updatedcal.write(events[evt][1])
		updatedcal.write('\n')
	updatedcal.write('\n'.join(calfooter))
	updatedcal.close()

	# check size, write to syslog
	syslog.syslog(args.out+'.ical contains ' \
		+str(len(events)) + ' entries')

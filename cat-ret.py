from sys import argv
import urllib2

catid = argv[1]
print catid

urlroot = 'http://www.pogdesign.co.uk/cat/generate_ics/'

ical = urllib2.urlopen(urlroot+catid)

print ical.read()
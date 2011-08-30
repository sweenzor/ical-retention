### Creates persistent calendars (historical entries) from forward looking ical streams

Useful for things like TV calendars which may be syndicated in a "forward looking" ical, but might be refrenced when looking for what you've missed

Notes on generating ical files for import into google calendar (or this script):

>[TV Calendar](http://www.pogdesign.co.uk/cat/)
>
>How can I generate an ICS for google calendar?
>Currently, the link you see on the top bar when logged in to 'Download iCal File', forces your browser to download the iCal to file directly rather than showing the contents of the file in your browser. This is the desired behaviour if you want to import it manually into a calendar program which may not have an import-from-url feature. Unfortunately, the way the file is forced to download (by telling your browser the file is an attachment) is not compatible with google calendar; for some reason, it is unable to read the data (this used to work, strangely).
>
>If you copy the URL given to you from the 'Download iCal File' link and change 'download_ics' to 'generate_ics', you should be able to use the new link within google calendar and most calendar programs with an import-from-url feature. By telling the server to generate the ics rather than download it, the file is sent without an attachment header and can be read correctly by google.
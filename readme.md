## ios-over-air-distribute ##

A python command to generate files for over the air adhoc distribution and enterprise distribution.

Device Registration Sample:
http://gngrwzrd.com/apps/MyApp

Installation Sample:
http://gngrwzrd.com/apps/MyApp/install.html

It generates and creates:

1. html/php/mobileconfig to obtain a user's UDID from mobile Safari.
2. devices.txt file written on the server.
3. html/plist for users to install the app.

## ADHOC ##

Example generating files for step 1:

	python distribute.py -n --appname=MyApp --organization=com.gngrwzrd --bundleid=com.gngrwzrd.MyApp --version=1.0 --baseurl=http://mywebsite.com/apps/MyApp --icon=sampleapps/MyApp/icon.png --destination=/Users/aaronsmith/Desktop/MyApp

The files generated can be uploaded to mywebsite.com/apps/MyApp. Navigate to mywebsite.com/apps/MyApp/ to see the device registration page.

After users have registered their devices, use the "devices.txt" file written to disk on your server. That file will be at mywebsite.com/apps/MyApp/devices.txt.

Example generating the install files for step 2:

	python distribute.py -r --appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp \

The generated files can be uploaded to mywebsite/apps/. Navigate to mywebsite.com/apps/com.myapp.MyAwesomeApp/install.html to see the installation page.

This script will also keep older installation html files if you wish to install a previous version. Make sure to name your IPA with a version number in it. EX MyApp-1.0.1.ipa. Then you'll get an install file named MyApp-1.0.1.html.

## ENTERPRISE ##

With enterprise certificates and provisions you don't need to obtain user's device UDIDs. You can instaed  skip to generating the install files.

Example gnerating files for step 2 enterprise:

	python distribute.py -r --appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp

The generated files can be uploaded to mywebsite/apps/. Navigate to mywebsite.com/apps/com.myapp.MyAwesomeApp/install.html to see the installation page.

This script will also keep older installation html files if you wish to install a previous version. Make sure to name your IPA with a version number in it. EX MyApp-1.0.1.ipa. Then you'll get an install file named MyApp-1.0.1.html.

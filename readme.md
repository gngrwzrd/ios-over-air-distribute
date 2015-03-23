## ios-over-air-distribute ##

A python command to generate files for over the air adhoc distribution and enterprise distribution.

Device Registration Sample:
http://gngrwzrd.com/apps/MyApp

Devices txt sample:
http://gngrwzrd.com/apps/MyApp/devices.txt

Installation Sample:
http://gngrwzrd.com/apps/MyApp/install.html

It generates and creates:

1. html/php/mobileconfig to obtain a user's UDID from mobile Safari.
2. html/plist for users to install the app.

*Apple requires HTTPS for the ipa installation over the air. You will need it!*

## ADHOC ##

Adhoc requires these steps:

1. Generate files to obtain UDID from users.
2. Use devices.txt file from server and add devices to your adhoc distribution provision in the apple member center.
3. In Xcode, archive ane export adhoc distribution. Save the IPA for step 4.
4. Generate installation files.

Example generating files for step 1:

	python distribute.py -n --appname=MyApp \
	--organization=com.gngrwzrd \
	--bundleid=com.gngrwzrd.MyApp \
	--version=1.0 \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--destination=/Users/aaronsmith/Desktop/MyApp

Uploaded files to mywebsite.com/apps/MyApp. Navigate to mywebsite.com/apps/MyApp/ to see the device registration page.

Example generating the install files for step 4:

	python distribute.py -r --appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp \

Uploaded to mywebsite.com/apps/MyApp. Navigate to mywebsite.com/apps/MyApp/install.html to see the installation page.

This script will also keep older installation html files if you wish to install a previous version. Make sure to name your IPA with a version number in it, like "MyApp-1.0.1.ipa". Then you'll get an install file named MyApp-1.0.1.html generated also.

## ENTERPRISE ##

With enterprise certificates and provisions you don't need to obtain user's device UDIDs. You can instaed  skip to generating the install files.

Enterprise requires only 2 steps:

1. In Xcode, archive and export for Enterprise Distribution. Save the IPA for step 2.
2. Generate the installation files:

	python distribute.py -r -e --appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp

The generated files can be uploaded to mywebsite/apps/. Navigate to mywebsite.com/apps/com.myapp.MyAwesomeApp/install.html to see the installation page.

This script will also keep older installation html files if you wish to install a previous version. Make sure to name your IPA with a version number in it. EX MyApp-1.0.1.ipa. Then you'll get an install file named MyApp-1.0.1.html.

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

**Apple requires HTTPS for IPA installation over the air. You will need it!**

## ADHOC ##

Adhoc requires these steps:

1. Generate files to obtain UDID from users.
2. Upload generated files to your server.
3. Email users the device registration link.
4. Use devices.txt file from server; add them to your adhoc distribution provision in the apple member center.
5. In Xcode, archive and export adhoc distribution. Save the IPA for step 6.
6. Generate installation files.
7. Upload generated files to your server.

Example generating files for step 1:

	python distribute.py -n \
	--appname=MyApp \
	--organization=com.gngrwzrd \
	--bundleid=com.gngrwzrd.MyApp \
	--version=1.0 \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--destination=/Users/aaronsmith/Desktop/MyApp

Example generating the install files for step 6:

	python distribute.py -r \
	--appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp \

This script will also keep installation files for each version of your IPA. Name your IPA with the version number in - MyApp-1.0.1.ipa.

## ENTERPRISE ##

With enterprise certificates and provisions you don't need to obtain user's device UDIDs. You can instaed  skip to generating the install files.

Enterprise requires only 3 steps:

1. In Xcode, archive and export for Enterprise Distribution. Save the IPA for step 2.
2. Generate the installation files:
3. Upload generated files to your server.

	python distribute.py -r -e \
	--appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp

This script will also keep installation files for each version of your IPA. Name your IPA with the version number in - MyApp-1.0.1.ipa.

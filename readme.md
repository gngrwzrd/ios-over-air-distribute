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
7. Upload generated files and IPA to your server.

Example generating files for step 1:

	python distribute.py -n \
	--appname=MyApp \
	--org=com.gngrwzrd \
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
	--destination=/Users/aaronsmith/Desktop/MyApp

This script will also keep installation files for each version of your IPA. Name your IPA with the version number in it (MyApp-1.0.1.ipa) so it doesn't get overwritten the next time you generate files.

You can also do step 1 and 6 all at once if you have all files required:

	python distribute.py -r -n \
	--appname=MyApp \
	--bundleid=com.gngrwzrd.MyApp \
	--org=com.gngrwzrd \
	--version=1.0 \
	--baseurl=http://gngrwzrd.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--ipa=sampleapps/MyApp/MyApp-1.0.1.ipa \
	--destination=apps/MyApp/

## Signing Mobileprofile for Adhoc ##

By default your mobileprofile will not be signed. In iOS, users will see a warning when installing the profile. This requires an extra step from the user in order to allow the unsigned profile to be installed.

Using your servers SSL certificates you can sign the mobileprofile so it's trusted when it opens in the iOS settings app.

Example generating files for Adhoc Step 1 with signed mobileprofile:

	python distribute.py -n \
	--appname=MyApp \
	--org=com.gngrwzrd \
	--bundleid=com.gngrwzrd.MyApp \
	--version=1.0 \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--destination=/Users/aaronsmith/Desktop/MyApp \
	-s \
	--sslcrt=server.crt \
	--sslkey=server.key \
	--sslchain=cert_chain.crt

## ENTERPRISE ##

With enterprise certificates and provisions you don't need to obtain user's device UDIDs. You can instead  skip to generating the install files.

Enterprise requires only 3 steps:

1. In Xcode, archive and export for Enterprise Distribution. Save the IPA for step 2.
2. Generate the installation files.
3. Upload generated files to your server.

Example generating the install files for step 2.

	python distribute.py -r -e \
	--appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--version=1.0 \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp

This script will also keep installation files for each version of your IPA. Name your IPA with the version number in it (MyApp-1.0.1.ipa) so it doesn't get overwritten the next time you generate files.


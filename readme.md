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

**Apple requires HTTPS (trusted ssl, not self signed) for IPA installation over the air. You will need it!**

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
	--bundleid=com.myapp.MyApp \
	--org=com.myapp \
	--version=1.0 \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--ipa=sampleapps/MyApp/MyApp-1.0.1.ipa \
	--destination=/Users/aaronsmith/Desktop/MyApp

## Signing Mobileprofile for Adhoc ##

By default your mobileprofile will not be signed. In iOS, users will see a warning when installing the profile. This requires an extra step from the user in order to allow the unsigned profile to be installed.

Using your servers SSL certificates you can sign the mobileprofile so it's trusted when it opens in the iOS settings app.

Example generating files for Adhoc Step 1 with signed mobileprofile:

	python distribute.py -n \
	--appname=MyApp \
	--org=com.myapp \
	--bundleid=com.myapp.MyApp \
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

**Apple requires HTTPS (trusted ssl, not self signed) for IPA installation over the air. You will need it!**

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

## Extra Information ##

The profile delivery system is very picky. If you attempt to change anything in this script such as moving files into different directories, I can't guarantee it'll work.

Over the air IPA installation is also very picky. I recommend the baseurl be as short as possible, try to eliminate special characters. Generally I'd try and stick to a-Z,0-9,-_/.

## Common Profile Delivery Errors ##

Unsupported URL. This is your URL callback in the profile.mobileconfig file. Make sure everything is URL encoded properly.

Can't connect to server. If your URL callback returns 404, or any errors, chances are you'll see this error.

## Common Installation Errors ##

Can't connect to mysite.com - this is most likely because your server doesn't have HTTPS, or have trusted SSL certificate.


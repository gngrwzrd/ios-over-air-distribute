## ios-over-air-distribute ##

Python script for generating static ios over the air distribution files. And a simple read-only PHP dashboard for viewing those files.

**Apple requires HTTPS (trusted ssl, not self signed) for IPA installation over the air. You will need it!**

## Dashboard ##

Dashboard Sample:
http://gngrwzrd.com/dist/dashboard.php

The dashboard is intended to be a private utility for you to view all the static files generated. When you're distributing the application, you'd instead send direct links to the registration page or install page.

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
	
	python simpledist.py -n \
	--appname=MyApp \
	--bundleid=com.gngrwzrd.MyApp \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--destination=/Users/aaronsmith/Desktop/MyApp

Example generating the install files for step 6:

	python simpledist.py -r \
	--appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp

This script will also keep installation files for each version of your IPA. Name your IPA with the version number in it (MyApp-1.0.1.ipa) so it doesn't get overwritten the next time you generate files.

You can also do step 1 and 6 all at once if you have all files required:

	python simpledist.py -r -n \
	--appname=MyApp \
	--bundleid=com.myapp.MyApp \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--icon=sampleapps/MyApp/icon.png \
	--ipa=sampleapps/MyApp/MyApp-1.0.1.ipa \
	--destination=/Users/aaronsmith/Desktop/MyApp

## Signing Mobileprofile for Adhoc ##

By default your mobileprofile will not be signed. In iOS, users will see a warning when installing the profile. This requires an extra step from the user in order to allow the unsigned profile to be installed.

Using your servers SSL certificates you can sign the mobileprofile so it's trusted when it opens in the iOS settings app.

Example generating files for Adhoc Step 1 with signed mobileprofile:

	python simpledist.py -n \
	--appname=MyApp \
	--bundleid=com.myapp.MyApp \
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

	python simpledist.py -r -e \
	--appname=MyApp \
	--bundleid=com.myapp.MyAwesomeApp \
	--ipa=MyAppIPA-1.0.1.ipa \
	--icon=MyIcon.png \
	--baseurl=http://mywebsite.com/apps/MyApp \
	--destination=/Users/aaronsmith/Desktop/MyApp

This script will also keep installation files for each version of your IPA. Name your IPA with the version number in it (MyApp-1.0.1.ipa) so it doesn't get overwritten the next time you generate files.

## Crashes ##

You can accept crashes from plcrashreporter. Example:

	- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
		PLCrashReporter * crash = [PLCrashReporter sharedReporter];
		if([crash hasPendingCrashReport]) {
			NSData * crashData = [crash loadPendingCrashReportData];
			if(crashData) {
				NSURL * url = [NSURL URLWithString:@"http://gngrwzrd.com/dist/apps/MyCrashingApp/crash/log.php"];
				NSMutableURLRequest * request = [NSMutableURLRequest requestWithURL:url];
				[request setHTTPMethod:@"POST"];
				PLCrashReport *report = [[PLCrashReport alloc] initWithData:crashData error:nil];
				NSString * log = [PLCrashReportTextFormatter stringValueForCrashReport:report withTextFormat:PLCrashReportTextFormatiOS];
				NSData * logData = [log dataUsingEncoding:NSUTF8StringEncoding];
				NSURLSessionUploadTask * upload = [[NSURLSession sharedSession] uploadTaskWithRequest:request fromData:logData completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
				}];
				[upload resume];
			}
		}
		[crash enableCrashReporter];
		return YES;
	}

## Symbolicate Crash ##

Find the symbolicatecrash command like this:

	find /Applications/Xcode.app -name symbolicatecrash -type f

Export DEVELOPER_DIR:
	
	export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer

CD to the directory containing the command and run it:

	cd /path/to/symbolicatecrash/
	./symbolicatecrash /path/to/MyCrashLogFile.txt /path/to/my.dSYM

The symbolicated crashlog is printed to stdout.

## Extra Information ##

The profile delivery system is very picky. If you attempt to change anything in this script such as moving files into different directories, I can't guarantee it'll work.

Over the air IPA installation is also very picky. I recommend the baseurl be as short as possible, try to eliminate special characters. Generally I'd try and stick to a-Z,0-9,-_/.

## Common Profile Delivery Errors ##

Unsupported URL. This is your URL callback in the profile.mobileconfig file. Make sure everything is URL encoded properly.

Can't connect to server. If your URL callback returns 404, or any errors, chances are you'll see this error.

## Common Installation Errors ##

Can't connect to mysite.com - this is most likely because your server doesn't have HTTPS, or have trusted SSL certificate.


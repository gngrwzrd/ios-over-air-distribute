import argparse,re,os,shutil,urllib

parser = argparse.ArgumentParser(description="Template file generator for iOS over the air distribution and profile installation.")
parser.add_argument("-n","--newapp",action="store_true",help="Make a new app directory with all profile templates prepared.")
parser.add_argument("-r","--release",action="store_true",help="Release a new IPA, making a new directory in an existing application directory.")
parser.add_argument("-e","--enterprise",action="store_true",help="The app being released is signed with enterprise certs and provisions.")
parser.add_argument("--appname",help="The application name, ex: Tales Untold, DOcumentr, etc.")
parser.add_argument("--organization",help="An organization identifier, ex: com.apptitude, com.gngrwzrd, com.pixelrevision, etc.")
parser.add_argument("--bundleid",help="THe application's bundle id. ex: com.talesuntold.TalesUntold")
parser.add_argument("--version",help="The application's CFBundleShortStringVersion value.")
parser.add_argument("--bundleversion",help="The application's CFBundleVersion value.")
parser.add_argument("--baseurl",help="The base HTTP URL where files will be uploaded to.")
parser.add_argument("--ipa",help="The IPA file to release.")

"""
** Adhoc and Enterprise Distribution with Safari requires HTTPS. **
"""

"""
For Adhoc Distribution, these are generally the steps:

Step 1:
Make a new app with distribute.py for users to register their devices:
python distribute.py -n --appname="Tales Untold" --organization="com.gngrwzrd" --bundleid=com.talesuntold.TalesUntold --baseurl="http://l.gngrwzrd.com/apps" --version=1.0

Step 2:
Upload the generated files to the Base URL chosen above.

Step 3:
Email users the link:
http://l.gngrwzrd.com/apps/com.talesuntold.TalesUntold/

Step 4:
After users have been to step 2. Grab the devices.txt file in the application folder - com.talesuntold.TalesUntold.
Add those devices to your ad hoc distribution provision.

Step 5:
Archive and distribute a build for ad hoc from Xcode, them release it with distribute.py:
python distribute.py -r --baseurl="http://l.gngrwzrd.com/apps" --ipa=TalesUntold-1.0.18.ipa --bundleid=com.talesuntold.TalesUntold --version=1.0 --bundleversion=18

Step 6:
Email users this link:
http://l.gngrwzrd.com/apps/com.talesuntold.TalesUntold/install.html
"""

"""
For Enterprise Distribution, these are generally the steps:

Step 1:
Archive and distribute for enterprise in Xcode. Then create the required files with distribute.py
python distribute.py -r --ipa=TalesUntold-1.0.18.ipa --bundleid="com.talesuntold.TalesUntoldEnter" --baseurl="http://l.gngrwzrd.com/apps" --version=1.0 --bundleversion=18

Step 3:
Email users this link:
http://l.gngrwzrd.com/apps/com.talesuntold.TalesUntold/install.html
"""

args = parser.parse_args()

if args.ipa:
	ipaname = args.ipa
	pieces = args.ipa.split("/")
	if len(pieces) > 0: ipa = pieces[0]
	ipaname = re.sub(".ipa","",ipa)
	args.ipaname = ipaname
	print "ipaname:" + ipaname

def replace_args(args,others,content,outfile,urlencode=False):
	if args.appname: content = re.sub("{{appname}}",args.appname,content)
	if args.baseurl: content = re.sub("{{baseurl}}",args.baseurl,content)
	if args.bundleid: content = re.sub("{{bundleid}}",args.bundleid,content)
	if args.organization: content = re.sub("{{organization}}",args.organization,content)
	if args.version: content = re.sub("{{version}}",args.version,content)
	if args.bundleversion: content = re.sub("{{bundleversion}}",args.bundleversion,content)
	if args.ipa: content = re.sub("{{ipa}}",args.ipa,content)
	#if args.ipaname: content = re.sub("{{ipaname}}",args.ipaname,content)
	if urlencode and args.appname: content = re.sub("{{encoded_appname}}",urllib.quote_plus(args.appname,''),content)
	if urlencode and  args.baseurl: content = re.sub("{{encoded_baseurl}}",urllib.quote_plus(args.baseurl,''),content)
	if urlencode and args.bundleid: content = re.sub("{{encoded_bundleid}}",urllib.quote_plus(args.bundleid,''),content)
	if urlencode and args.organization: content = re.sub("{{encoded_organization}}",urllib.quote_plus(args.organization,''),content)
	if urlencode and args.version: content = re.sub("{{encoded_version}}",urllib.quote_plus(args.version,''),content)
	if urlencode and args.bundleversion: content = re.sub("{{encoded_bundleversion}}",urllib.quote_plus(args.bundleversion,''),content)
	if urlencode and args.ipa: content = re.sub("{{encoded_ipa}}",urllib.quote_plus(args.ipa,''),content)
	if urlencode and args.ipaname: content = re.sub("{{encoded_ipaname}}",urllib.quote_plus(args.ipaname,''),content)
	for key in others: content = re.sub("{{"+key+"}}",others[key],content)
	outfile.write(content)
	outfile.close()

def write_mobileconfig(args):
	replace_args(args,{},
		open("templates/template.mobileconfig","r").read(),
		open(args.bundleid+"/profile.mobileconfig","w")
	)

def write_index(args):
	replace_args(args,{},
		open("templates/template.index.html","r").read(),
		open(args.bundleid+"/index.html","w")
	)

def write_registered(args):
	try: os.mkdir("%s/registered" % (args.bundleid))
	except: pass
	replace_args(args,{},
		open("templates/template.registered.html","r").read(),
		open(args.bundleid+"/registered/index.html","w")
	)

def write_retrieve(args):
	replace_args(args,{},
		open("templates/template.retrieve.php","r").read(),
		open(args.bundleid+"/retrieve.php","w")
	)

def secure_baseurl(baseurl):
	if baseurl[0:5] != "https" and baseurl[0:4] == "http":
		print "** Base URL was changed to HTTPS - this is required by Apple. Your server will have to support HTTPS."
		baseurl = baseurl[4:]
		baseurl = "https" + baseurl
	return baseurl

def write_default_install(args):
	args.baseurl = secure_baseurl(args.baseurl)
	dest = args.bundleid + "/" + args.ipaname + ".html"
	replace_args(args,{},
		open("templates/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def write_app_plist(args):
	args.baseurl = secure_baseurl(args.baseurl)
	dest = args.bundleid + "/" + args.ipaname + ".plist"
	replace_args(args,{},
		open("templates/template.app.plist","r").read(),
		open(dest,"w")
	)

def copy_ipa(args):
	shutil.copyfile(args.ipa, "%s/%s" % (args.bundleid,args.ipaname+".ipa"))

def newapp(args):
	try: os.mkdir(args.bundleid)
	except: pass
	write_mobileconfig(args)
	write_index(args)
	write_registered(args)
	write_retrieve(args)

def release(args):
	try: os.mkdir(args.bundleid)
	except: pass
	if not args.enterprise: write_app_plist(args)
	write_default_install(args)
	copy_ipa(args)

if args.newapp:
	if not args.appname or not args.organization or not args.bundleid or not args.baseurl:
		print "New app requires at least appname, organization, bundleid, and baseurl parameters"
	else:
		newapp(args)

if args.release:
	if not args.baseurl or not args.bundleid or not args.version or not args.bundleversion or not args.ipa:
		print "Release app requires at least baseurl, bundleid, version, bundleversion, and ipa parameters"
	else:
		release(args)

import argparse,re,os,shutil,urllib,subprocess

parser = argparse.ArgumentParser(description="Template file generator for iOS over the air distribution and profile installation.")
parser.add_argument("-n","--newapp",action="store_true",help="Make a new app directory with all profile templates prepared.")
parser.add_argument("-r","--release",action="store_true",help="Release a new IPA, making a new directory in an existing application directory.")
parser.add_argument("-e","--enterprise",action="store_true",help="The app being released is signed with enterprise certs and provisions.")
parser.add_argument("-s","--sign",action="store_true",help="(Optional) sign the mobileconfig with your servers ssl certificates.")
parser.add_argument("-d","--destination",help="(Optional) Destination directory where to create all files.")
parser.add_argument("--appname",help="The application name, ex: Tales Untold, DOcumentr, etc.")
parser.add_argument("--org",help="An organization identifier, ex: com.apptitude, com.gngrwzrd, com.pixelrevision, etc.")
parser.add_argument("--bundleid",help="THe application's bundle id. ex: com.talesuntold.TalesUntold.")
parser.add_argument("--version",help="The application's CFBundleShortVersionString value.")
parser.add_argument("--baseurl",help="The base HTTP URL where files will be uploaded to.")
parser.add_argument("--ipa",help="The IPA file to release.")
parser.add_argument("--icon",help="An icon to display in generated templates.")
parser.add_argument("--sslcrt",help="Your servers crt file.")
parser.add_argument("--sslkey",help="Your servers key file. (Passwords not supported).")
parser.add_argument("--sslchain",help="Your servers cert chain file.")

"""
** Adhoc and Enterprise Distribution with Safari requires HTTPS. **
"""

"""
For Adhoc Distribution, these are generally the steps:

Step 1:
Make a new app with distribute.py for users to register their devices:
python distribute.py -n --appname="Tales Untold" --org="com.gngrwzrd" --bundleid=com.talesuntold.TalesUntold --baseurl="http://l.gngrwzrd.com/apps" --version=1.0

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
python distribute.py -r --baseurl="http://l.gngrwzrd.com/apps" --ipa=TalesUntold-1.0.18.ipa --bundleid=com.talesuntold.TalesUntold --version=1.0

Step 6:
Email users this link:
http://l.gngrwzrd.com/apps/com.talesuntold.TalesUntold/install.html
"""

"""
For Enterprise Distribution, these are generally the steps:

Step 1:
Archive and distribute for enterprise in Xcode. Then create the required files with distribute.py
python distribute.py -r --ipa=TalesUntold-1.0.18.ipa --bundleid="com.talesuntold.TalesUntoldEnter" --baseurl="http://l.gngrwzrd.com/apps" --version=1.0

Step 3:
Email users this link:
http://l.gngrwzrd.com/apps/com.talesuntold.TalesUntold/install.html
"""

args = parser.parse_args()

if args.ipa:
	ipaname = args.ipa
	pieces = args.ipa.split("/")
	if len(pieces) > 0: ipa = pieces[-1]
	ipaname = re.sub(".ipa","",ipa)
	args.ipaname = ipaname

if getattr(args,"icon",None):
	iconname = args.icon
	pieces = args.icon.split("/")
	if len(pieces) > 0: iconname = pieces[-1]
	args.iconname = iconname

if not getattr(args,"destination",False):
	if getattr(args,"bundleid",None):
		args.destination = args.bundleid

def replace_args(args,others,content,outfile,urlencode=False):
	if getattr(args,"appname",None): content = re.sub("{{appname}}",args.appname,content)
	if getattr(args,"baseurl",None): content = re.sub("{{baseurl}}",args.baseurl,content)
	if getattr(args,"bundleid",None): content = re.sub("{{bundleid}}",args.bundleid,content)
	if getattr(args,"org",None): content = re.sub("{{org}}",args.org,content)
	if getattr(args,"version",None): content = re.sub("{{version}}",args.version,content)
	if getattr(args,"ipa",None): content = re.sub("{{ipa}}",args.ipa,content)
	if getattr(args,"ipaname",None): content = re.sub("{{ipaname}}",args.ipaname,content)
	if getattr(args,"iconname",None): content = re.sub("{{iconname}}",args.iconname,content)
	if urlencode and getattr(args,"appname",None): content = re.sub("{{encoded_appname}}",urllib.quote_plus(args.appname,''),content)
	if urlencode and getattr(args,"baseurl",None): content = re.sub("{{encoded_baseurl}}",urllib.quote_plus(args.baseurl,''),content)
	if urlencode and getattr(args,"bundleid",None): content = re.sub("{{encoded_bundleid}}",urllib.quote_plus(args.bundleid,''),content)
	if urlencode and getattr(args,"org",None): content = re.sub("{{encoded_org}}",urllib.quote_plus(args.org,''),content)
	if urlencode and getattr(args,"version",None): content = re.sub("{{encoded_version}}",urllib.quote_plus(args.version,''),content)
	if urlencode and getattr(args,"ipa",None): content = re.sub("{{encoded_ipa}}",urllib.quote_plus(args.ipa,''),content)
	if urlencode and getattr(args,"ipaname",None): content = re.sub("{{encoded_ipaname}}",urllib.quote_plus(args.ipaname,''),content)
	for key in others: content = re.sub("{{"+key+"}}",others[key],content)
	outfile.write(content)
	outfile.close()

def write_mobileconfig(args):
	replace_args(args,{},
		open("templates/template.mobileconfig","r").read(),
		open(args.destination+"/profile.mobileconfig","w")
	)

def write_index(args):
	replace_args(args,{},
		open("templates/template.index.html","r").read(),
		open(args.destination+"/index.html","w")
	)

def write_registered(args):
	try: os.mkdir("%s/registered" % (args.destination))
	except: pass
	replace_args(args,{},
		open("templates/template.registered.html","r").read(),
		open(args.destination+"/registered/index.html","w")
	)

def write_retrieve(args):
	replace_args(args,{},
		open("templates/template.retrieve.php","r").read(),
		open(args.destination+"/retrieve.php","w")
	)

def secure_baseurl(baseurl):
	if baseurl[0:5] != "https" and baseurl[0:4] == "http":
		print "** Base URL was changed to HTTPS - this is required by Apple. Your server will have to support HTTPS."
		baseurl = baseurl[4:]
		baseurl = "https" + baseurl
	return baseurl

def write_install(args):
	args.baseurl = secure_baseurl(args.baseurl)
	dest = args.destination + "/" + "install.html"
	replace_args(args,{},
		open("templates/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def write_ipa_install(args):
	args.baseurl = secure_baseurl(args.baseurl)
	dest = args.destination + "/" + args.ipaname + ".html"
	replace_args(args,{},
		open("templates/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def write_app_plist(args):
	args.baseurl = secure_baseurl(args.baseurl)
	dest = args.destination + "/" + args.ipaname + ".plist"
	replace_args(args,{},
		open("templates/template.app.plist","r").read(),
		open(dest,"w")
	)

def write_enterprise_index(args):
	args.baseurl = secure_baseurl(args.baseurl)
	dest = args.destination + "/" + "index.html"
	replace_args(args,{},
		open("templates/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def sign_mobileconfig(args):
	unsignedconfig = args.destination + "/profile.mobileconfig"
	signedconfig = args.destination + "/signed.profile.mobileconfig"
	crt = args.sslcrt
	key = args.sslkey
	chain = args.sslchain
	command = "/usr/bin/openssl smime -sign -in %s -out %s " % (unsignedconfig,signedconfig)
	command = command + "-signer %s -inkey %s " % (crt,key)
	command = command + "-certfile %s -outform der -nodetach" % (chain)
	subprocess.call(command,shell=True)
	os.unlink(unsignedconfig)
	shutil.move(signedconfig,unsignedconfig)

def copy_ipa(args):
	shutil.copyfile(args.ipa, "%s/%s" % (args.destination,args.ipaname+".ipa"))

def copy_icon(args):
	if getattr(args,"iconname",None):
		shutil.copyfile(args.icon,"%s/%s"%(args.destination,args.iconname))

def copy_js(args):
	shutil.copyfile("scripts/main.js","%s/main.js"%(args.destination))
	shutil.copyfile("scripts/jquery-1.8.3.min.js","%s/jquery.min.js"%(args.destination))

def newapp(args):
	try: os.mkdir(args.destination)
	except: pass
	write_mobileconfig(args)
	write_index(args)
	write_registered(args)
	write_retrieve(args)
	copy_icon(args)
	copy_js(args)
	if args.sign: sign_mobileconfig(args)

def release(args):
	try: os.mkdir(args.destination)
	except: pass
	if args.enterprise: write_enterprise_index(args)
	write_app_plist(args)
	write_ipa_install(args)
	write_install(args)
	copy_ipa(args)
	copy_icon(args)
	copy_js(args)

if args.newapp:
	if not args.appname or not args.org or not args.bundleid or not args.baseurl:
		print "New app requires at least appname, org, bundleid, and baseurl parameters"
	else:
		newapp(args)

if args.release:
	if not args.appname or not args.baseurl or not args.bundleid or not args.version or not args.ipa:
		print "Release app requires at least appname, baseurl, bundleid, version, and ipa parameters"
	else:
		release(args)

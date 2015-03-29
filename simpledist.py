import argparse,re,os,shutil,urllib,subprocess

parser = argparse.ArgumentParser(description="Template file generator for iOS over the air distribution and profile installation.")
parser.add_argument("-n","--newapp",action="store_true",help="Make a new app directory with all profile templates prepared.")
parser.add_argument("-r","--release",action="store_true",help="Release a new IPA, making a new directory in an existing application directory.")
parser.add_argument("-e","--enterprise",action="store_true",help="The app being released is signed with enterprise certs and provisions.")
parser.add_argument("-s","--sign",action="store_true",help="(Optional) sign the mobileconfig with your servers ssl certificates.")
parser.add_argument("-d","--destination",help="(Optional) Destination directory where to create all files.")
parser.add_argument("-g","--regen",action="store_true",help="Create a simpledist.sh file in {destination} to easly release more IPAs.")
parser.add_argument("--appname",help="The application name, ex: Tales Untold, DOcumentr, etc.")
parser.add_argument("--bundleid",help="THe application's bundle id. ex: com.talesuntold.TalesUntold.")
parser.add_argument("--baseurl",help="The base HTTP URL where files will be uploaded to.")
parser.add_argument("--ipa",help="The IPA file to release.")
parser.add_argument("--icon",help="An icon to display in generated templates.")
parser.add_argument("--rnotes",help="Release notes to add to the install page.")
parser.add_argument("--sslcrt",help="Your servers crt file.")
parser.add_argument("--sslkey",help="Your servers key file. (Passwords not supported).")
parser.add_argument("--sslchain",help="Your servers cert chain file.")
args = parser.parse_args()

if args.ipa:
	ipaname = args.ipa
	pieces = args.ipa.split("/")
	if len(pieces) > 0: ipa = pieces[-1]
	ipaname = re.sub(".ipa","",ipa)
	args.ipaname = ipaname

if getattr(args,"icon",None):
	args.iconname = "icon.png"

if not getattr(args,"destination",False):
	if getattr(args,"bundleid",None):
		args.destination = "apps/"+args.bundleid

def replace_args(args,others,content,outfile,urlencode=False):
	if getattr(args,"appname",None): content = re.sub("{{appname}}",args.appname,content)
	if getattr(args,"secure_baseurl",None): content = re.sub("{{secure_baseurl}}",args.secure_baseurl,content)
	if getattr(args,"baseurl",None):
		content = re.sub("{{baseurl}}",args.baseurl,content)
		content = re.sub("{{install_baseurl}}",args.baseurl,content)
	if getattr(args,"bundleid",None): content = re.sub("{{bundleid}}",args.bundleid,content)
	if getattr(args,"ipa",None): content = re.sub("{{ipa}}",args.ipa,content)
	if getattr(args,"ipaname",None): content = re.sub("{{ipaname}}",args.ipaname,content)
	if getattr(args,"iconname",None): content = re.sub("{{iconname}}",args.iconname,content)
	
	if urlencode and getattr(args,"appname",None): content = re.sub("{{encoded_appname}}",urllib.quote_plus(args.appname,''),content)
	if urlencode and getattr(args,"baseurl",None):
		content = re.sub("{{encoded_baseurl}}",urllib.quote_plus(args.baseurl,''),content)
		content = re.sub("{{encoded_install_baseurl}}",urllib.quote_plus(args.baseurl+'/install',''),content)
		content = re.sub("{{encoded_install_secure_baseurl}}",urllib.quote_plus(args.secure_baseurl+'/install',''),content)
	if urlencode and getattr(args,"secure_baseurl",None): content = re.sub("{{secure_baseurl}}",urllib.quote_plus(args.secure_baseurl,''),content)
	if urlencode and getattr(args,"bundleid",None): content = re.sub("{{encoded_bundleid}}",urllib.quote_plus(args.bundleid,''),content)
	if urlencode and getattr(args,"ipa",None): content = re.sub("{{encoded_ipa}}",urllib.quote_plus(args.ipa,''),content)
	if urlencode and getattr(args,"ipaname",None): content = re.sub("{{encoded_ipaname}}",urllib.quote_plus(args.ipaname,''),content)
	for key in others: content = re.sub("{{"+key+"}}",others[key],content)
	outfile.write(content)
	outfile.close()

def write_mobileconfig(args):
	replace_args(args,{},
		open("assets/template.mobileconfig","r").read(),
		open(args.destination+"/profile.mobileconfig","w")
	)

def write_recruit(args):
	replace_args(args,{},
		open("assets/template.recruit.php","r").read(),
		open(args.destination+"/recruit/index.php","w")
	)

def write_registered(args):
	replace_args(args,{},
		open("assets/template.registered.html","r").read(),
		open(args.destination+"/registered/index.html","w")
	)

def write_retrieve(args):
	replace_args(args,{},
		open("assets/template.retrieve.php","r").read(),
		open(args.destination+"/retrieve.php","w")
	)

def secure_baseurl(baseurl):
	if baseurl[0:5] != "https" and baseurl[0:4] == "http":
		print "** Base URL was changed to HTTPS - this is required by Apple. Your server will have to support HTTPS."
		baseurl = baseurl[4:]
		baseurl = "https" + baseurl
	return baseurl

def write_install(args):
	dest = args.destination + "/install/" + "index.html"
	replace_args(args,{},
		open("assets/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def write_ipa_install(args):
	dest = args.destination + "/install/" + args.ipaname + ".html"
	replace_args(args,{},
		open("assets/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def write_app_plist(args):
	args.baseurl = args.baseurl
	dest = args.destination + "/install/" + args.ipaname + ".plist"
	replace_args(args,{},
		open("assets/template.app.plist","r").read(),
		open(dest,"w")
	)

def write_enterprise_index(args):
	args.baseurl = args.baseurl
	dest = args.destination + "/" + "index.html"
	replace_args(args,{},
		open("assets/template.install.html","r").read(),
		open(dest,"w"),
		True
	)

def write_bundleid_txt(args):
	f = open(args.destination + "/bundleid.txt","w")
	f.write(args.bundleid)
	f.close()

def write_crash_receiver(args):
	shutil.copy("assets/template.crash.php",args.destination+"/crash/log.php")

def write_regen(args):
	line = "#!/bin/bash\npython simpledist.py "
	if args.release: line += "-r "
	if args.newapp: line += "-n "
	if args.enterprise: line += "-e "
	if args.sign: line += "-s "
	if args.destination: line += "--destination='%s' " %(args.destination)
	if args.appname: line += "--appname='%s' " %(args.appname)
	if args.bundleid: line += "--bundleid='%s' " % (args.bundleid)
	if args.baseurl: line += "--baseurl='%s' " %(args.baseurl)
	if args.icon: line += "--icon='%s' " %(args.icon)
	if args.rnotes: line += "--rnotes='%s' " %(args.rnotes)
	if args.sslcrt: line += "--sslcrt='%s' " %(args.sslcrt)
	if args.sslkey: line += "--sslkey='%s' " %(args.sslkey)
	if args.sslchain: line += "--sslchain='%s' " %(args.sslchain)
	line += "--ipa=\"$1\""
	handle = open("%s/simpledist.sh"%args.destination,"w")
	handle.write(line)
	handle.close()

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
	shutil.copyfile(args.ipa, "%s/install/%s" % (args.destination,args.ipaname+".ipa"))

def copy_icon(args):
	if getattr(args,"iconname",None):
		shutil.copyfile(args.icon,"%s/assets/%s"%(args.destination,args.iconname))

def copy_js(args):
	shutil.copyfile("assets/main.js","%s/assets/main.js"%(args.destination))
	shutil.copyfile("assets/jquery-1.8.3.min.js","%s/assets/jquery.min.js"%(args.destination))

def copy_css(args):
	shutil.copyfile("assets/main.css","%s/assets/main.css"%(args.destination))
	shutil.copyfile("assets/buttons.css","%s/assets/buttons.css"%(args.destination))

def newapp(args):
	try: os.mkdir(args.destination)
	except: pass
	try: os.mkdir(args.destination + "/recruit")
	except: pass
	try: os.mkdir(args.destination + "/assets")
	except: pass
	try: os.mkdir(args.destination + "/registered")
	except: pass
	try: os.mkdir(args.destination + "/crash")
	except: pass
	write_regen(args)
	write_mobileconfig(args)
	write_recruit(args)
	write_registered(args)
	write_retrieve(args)
	write_bundleid_txt(args)
	write_crash_receiver(args)
	copy_icon(args)
	copy_js(args)
	copy_css(args)
	if args.sign: sign_mobileconfig(args)

def release(args):
	try: os.mkdir(args.destination)
	except: pass
	try: os.mkdir(args.destination + "/assets")
	except: pass
	try: os.mkdir(args.destination + "/recruit")
	except: pass
	try: os.mkdir(args.destination + "/install")
	except: pass
	args.secure_baseurl = secure_baseurl(args.baseurl)
	if args.enterprise: write_enterprise_index(args)
	write_app_plist(args)
	write_ipa_install(args)
	write_install(args)
	copy_ipa(args)
	copy_icon(args)
	copy_js(args)
	copy_css(args)
	
if args.newapp:
	if not args.appname or not args.bundleid or not args.baseurl:
		print "New app requires at least appname, bundleid, and baseurl parameters"
	else:
		newapp(args)

if args.release:
	if not args.appname or not args.baseurl or not args.bundleid or not args.ipa:
		print "Release app requires at least appname, baseurl, bundleid, and ipa parameters"
	else:
		release(args)

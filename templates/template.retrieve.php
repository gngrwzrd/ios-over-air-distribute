<?php

error_reporting(E_ALL & ~E_NOTICE);

$basedir = realpath(dirname(__FILE__));
$devicestxt = $basedir . "/" . "devices.txt";
$data = file_get_contents('php://input');

//<string>bab9ecb7cc2cfbd2d3912e2a892faccc176937f9</string>

$device = NULL;
$model = NULL;

if($_GET['device'] != FALSE) {
	//for testing, put device in get vars
	$device = $_GET['device'];
} else {
	//search data from safari callback

	//device id
	$matches = array();
	preg_match('/[a-zA-Z0-9]{40}/',$data,$matches);
	$device = $matches[0];

	//iPhone
	$matches = array();
	preg_match('/iPhone[0-9]{1,2}\,[0-9]{1,2}/',$data,$matches);
	if(count($matches) > 0) {
		$model = $matches[0];
	}
	
	//iPad
	$matches = array();
	preg_match('/iPad[0-9]{1,2}\,[0-9]{1,2}/',$data,$matches);
	if(count($matches) > 0) {
		$model = $matches[0];
	}

	//iPod
	$matches = array();
	preg_match('/iPod[0-9]{1,2}\,[0-9]{1,2}/',$data,$matches);
	if(count($matches) > 0) {
		$model = $matches[0];
	}
}

$devices = NULL;

//if file doesn't exist, write first line as the columns for apple device import online.
if(!file_exists($devicestxt)) {
	$devices = fopen($devicestxt,"w");
	fwrite($devices,"deviceIdentifier\tdeviceName\n");
	fclose($devices);
}

//wether to write device info to file.
$write = True;

//read line by line searching for existing device
$devices = fopen($devicestxt,"r+");
while(!feof($devices)) {
	$line = fgets($devices);
	if(preg_match('/'.$device.'/',$line)) {
		$write = False;
		break;
	}
}

$size = filesize($devicestxt);
fseek($devices,$size,SEEK_SET);

//write device if necessary
if($write) {
	if($model) {
		fwrite($devices,$device."\t".$model."\n");
	} else {
		fwrite($devices,$device."\t"."unknown"."\n");
	}
}

fclose($devices);

$raw = fopen("raw-device.txt","w");
fwrite($raw,$data);
fclose($raw);

header("Location: {{baseurl}}/{{bundleid}}/registered");

?>

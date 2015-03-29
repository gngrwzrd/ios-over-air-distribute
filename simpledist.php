<?php

session_start();
date_default_timezone_set('America/Los_Angeles');

require_once("assets/uuid.php");

function sortcrashes($a, $b) {
	return $a['mtime'] < $b['mtime'];
}

class SimpleDist {
	
	var $baseURL;
	var $secureBaseURL;
	var $basePath;
	var $appsPath;
	var $assetsPath;
	var $appsDirName;
	var $usersDirName;
	var $userJsonFileName;
	var $devicesFileName;
	var $noIconFileName;
	var $iconFileName;

	function __construct() {
		$this->baseURL = "http://gngrwzrd.com/dist";
		$this->secureBaseURL = "http://gngrwzrd.com/dist";
		$this->appsDirName = "apps";
		$this->usersDirName = "users";
		$this->userJsonFileName = 'user.json';
		$this->devicesFileName = "devices.txt";
		$this->basePath = realpath(dirname(__FILE__));
		$this->appsPath = $this->basePath . '/' . $this->appsDirName;
		$this->assetsPath = $this->basePath . '/assets';
		$this->iconFileName = "icon.png";
		$this->noIconFileName = "default-icon.png";
	}
	
	function uuid() {
		return UUID::v4();
	}

	function fullescape($in) {
		$out = '';
		for ($i=0;$i<strlen($in);$i++)  { 
			$hex = dechex(ord($in[$i])); 
			if($hex=='')  {
				$out = $out.urlencode($in[$i]); 
			} else  {
				$out = $out .'%'.((strlen($hex)==1) ? ('0'.strtoupper($hex)):(strtoupper($hex))); 
			}
		} 
		$out = str_replace('+','%20',$out); 
		$out = str_replace('_','%5F',$out); 
		$out = str_replace('.','%2E',$out); 
		$out = str_replace('-','%2D',$out);
		return $out;
	}

	function rrmdir($dir) { 
		if(is_dir($dir)) { 
			$objects = scandir($dir);
			foreach($objects as $object) { 
				if($object != "." && $object != "..") { 
					if(filetype($dir."/".$object) == "dir") {
						$this->rrmdir($dir."/".$object);
					} else {
						unlink($dir."/".$object);
					}
				}
	     	}
			reset($objects);
			rmdir($dir);
		}
	}

	function readFileContent($path) {
		$size = filesize($path);
		$fhandle = fopen($path,"r");
		$content = fread($fhandle,$size);
		fclose($fhandle);
		return $content;
	}

	function writeFileContent($path,$content) {
		$fhandle = fopen($path,"w");
		fwrite($fhandle,$content);
		fclose($fhandle);
	}

	function joinPaths($paths) {
		$out = $paths[0];
		for($i = 0; $i < count($paths); $i++) {
			if($i == 0) {
				continue;
			}
			$out .= '/' . $paths[$i];
		}
		return $out;
	}

	function getActionFromURL($default='') {
		if(isset($_GET['a'])) {
			return $_GET['a'];
		}
		return $default;
	}

	function getAppNameFromURL() {
		if($_GET['app']) {
			return urldecode($_GET['app']);
		}
		$url = $_SERVER['PHP_SELF'];
		$matches = array();
		preg_match('/\/'.$this->appsDirName.'\/([a-zA-Z0-9._%\-]+)\/?/',$url,$matches);
		return urldecode($matches[1]);
	}

	function getDeviceUDIDFromData($data) {
		//device id
		$matches = array();
		preg_match('/[a-zA-Z0-9]{40}/',$data,$matches);
		$device = $matches[0];
		return $device;
	}

	function getDeviceModelFromData($data) {
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

		return $model;
	}

	function getDirsAtPath($path) {
		$rawfiles = scandir($path);
		$realfiles = array();
		for($i = 0; $i < count($rawfiles); $i++) {
			if($rawfiles[$i] != "." && $rawfiles[$i] != "..") {
				$fullpath = $path . "/" . $rawfiles[$i];
				if(is_dir($fullpath)) {
					array_push($realfiles,$rawfiles[$i]);
				}
			}
		}
		return $realfiles;
	}

	function getFilesAtPath($path, $ext=False, $ignore=array()) {
		$rawfiles = scandir($path);
		$realfiles = array();
		for($i = 0; $i < count($rawfiles); $i++) {
			if($rawfiles[$i] != "." && $rawfiles[$i] != "..") {
				$fullpath = $path . "/" . $rawfiles[$i];
				if(is_dir($fullpath)) {
					continue;
				}
				if($ext) {
					$info = pathinfo($fullpath);
					if($info['extension'] == $ext) {
						if(!array_search($info['filename'],$ignore)) {
							array_push($realfiles,$info['filename']);
						}
					}
				} else {
					if(!array_search($rawfiles[$i],$ignore)) {
						array_push($realfiles,$rawfiles[$i]);
					}
				}
			}
		}
		return $realfiles;
	}

	function getAppNames() {
		return $this->getDirsAtPath($this->appsPath);
	}

	function getAppVersions($app) {
		$path = $this->joinPaths(array($this->appsPath,$app,"install"));
		return $this->getFilesAtPath($path,"html",array("install","index"));
	}

	function getCrashesForApp($app) {
		$path = $this->joinPaths( array($this->appsPath,$app,"crash") );
		if(!file_exists($path)) {
			return array();
		}
		$rawfiles = scandir($path);
		$crashes = array();
		for($i = 0; $i < count($rawfiles); $i++) {
			if($rawfiles[$i] != '.' && $rawfiles[$i] != '..') {
				$fullpath = $path . '/' . $rawfiles[$i];
				$info = pathinfo($fullpath);
				if($info['extension'] == 'txt') {
					$mtime = filemtime($fullpath);
					$crash = array("crash"=>$rawfiles[$i],"mtime"=>$mtime);
					array_push($crashes,$crash);
				}
			}
		}
		usort($crashes,'sortcrashes');
		return $crashes;
	}

	function getBundleIdForApp($app) {
		$path = $this->joinPaths(array($this->appsPath,$app,"bundleid.txt"));
		$size = filesize($path);
		$fhandle = fopen($path,"r");
		$content = fread($fhandle,$size);
		fclose($fhandle);
		return $content;
	}

	function hasIconForApp($app) {
		$path = $this->joinPaths(array($this->appsPath,$app,"assets",$this->iconFileName));
		return file_exists($path);
	}

	function getIconPathForApp($app) {
		if(!$this->hasIconForApp($app)) {
			return $this->joinPaths(array('assets',$this->noIconFileName));
		}
		return $this->joinPaths(array($this->appsDirName,$app,"assets",$this->iconFileName));
	}

	function getRecruitLinkForApp($app) {
		return $this->joinPaths(array($this->appsDirName,$app,"recruit"));
	}
	
	function getDevicesLinkForApp($app) {
		return $this->joinPaths(array($this->appsDirName,$app,"devices.txt"));
	}

	function getInstallLinkForApp($app) {
		return $this->joinPaths(array($this->appsDirName,$app,"install"));
	}

	function getMobileConfigPathForApp($app) {
		return $this->joinPaths(array($this->appsDirName,$app,"profile.mobileconfig"));
	}

	function getCrashesLinkForApp($app) {
		return "?a=clist&app=" . $app;
	}

	function getCrashLogPathForApp($app,$crashlogname) {
		return $this->joinPaths(array($this->appsDirName,$app,"crash",$crashlogname));
	}

	function saveDevice() {
		$data = file_get_contents('php://input');
		$device = $this->getDeviceUDIDFromData($data);
		$model = $this->getDeviceModelFromData($data);
		$app = $this->getAppNameFromURL();
		$devices = $this->joinPaths(array($this->appsPath,$app,$this->devicesFileName));

		if(!file_exists($devices)) {
			$handle = fopen($devices,"w");
			fwrite($handle,"deviceIdentifier\tdeviceName\n");
			fclose($handle);
		}
		
		$size = filesize($devices);
		$handle = fopen($devices,"r+");
		$write = TRUE;
		while(($line=fgets($handle))) {
			if(preg_match('/'.$device.'/',$line)) {
				$write = FALSE;
			}
		}
		
		$line = $device . "\t" . $model . "\n";
		if($write) {
			fseek($handle,$size);
			fwrite($handle,$line);
		}
		
		return $this->joinPaths(array($this->baseURL,$this->appsDirName,$app,"registered"));
	}

	function saveCrashForApp($app,$data) {
		$path = $this->joinPaths(array($this->appsPath,$app,"crash",$this->uuid().'.txt'));
		$this->writeFileContent($path,$data);
	}

	function getCrashCountForApp($app) {
		$path = $this->joinPaths(array($this->appsPath,$app,"crash"));
		$files = $this->getFilesAtPath($path,"txt",array());
		return count($files);
	}

	function getDevicesCountForApp($app) {
		$devices = $this->joinPaths(array($this->appsPath,$app,"devices.txt"));
		if(!file_exists($devices)) {
			return 0;
		}
		$handle = fopen($devices,"r");
		$count = -1;
		while(fgets($handle)) {
			$count++;
		}
		return $count;
	}
}

?>

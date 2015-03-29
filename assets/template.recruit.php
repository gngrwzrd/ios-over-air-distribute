<?php
require_once("../../../simpledist.php");
$helper = new SimpleDist();
$app = $helper->getAppNameFromURL();
$config = $helper->getMobileConfigPathForApp($app);
$bundleId = $helper->getBundleIdForApp($app);
?>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>Register Your Device</title>
<link rel="stylesheet" href="../assets/main.css"/>
<link rel="stylesheet" href="../assets/buttons.css"/>
<script type="text/javascript" src="../assets/jquery.min.js"></script>
<script type="text/javascript" src="../assets/main.js"></script>
</head>
<body>
<div class="content">
	<div class="sectionHeader">
		<table cellspacing=0 cellpadding=0><tr>
		<td width="75"><img class="sectionHeaderIcon" src="../assets/{{iconname}}" width="50" height="50" /></td>
		<td>{{appname}}
		<div class="sectionHeaderAppBundleId">{{bundleid}}</div></td>
		</tr></table>
	</div>
	<div class="desktop">
		<div class="sectionRow center">
			Open this page on your iOS device.
		</div>
	</div>
	<div class="mobile">
		<div class="sectionRow center">
			<a style="width:190px;" class="button black" href="../profile.mobileconfig">Tap to register your device</a>
		</div>
	</div>
</div>

<pre style="display:none;">
<?php
var_dump($_SESSION);
?>
</pre>
</body>
</html>

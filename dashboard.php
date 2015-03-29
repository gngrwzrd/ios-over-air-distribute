<?php
require_once("simpledist.php");
error_reporting(E_ALL);
$helper = new SimpleDist();
$action = $helper->getActionFromURL("alist");
?>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, user-scalable = no">
<script type="text/javascript" src="assets/jquery-1.8.3.min.js"></script>
<script type="text/javascript" src="assets/main.js" /></script>
<link rel="stylesheet" type="text/css" href="assets/main.css">
<link rel="stylesheet" type="text/css" href="assets/buttons.css">
<title>Dashboard</title>
</head>
<body>
<div class="content">
	
	<?php if($action == "alist") {
		/************************* alist action **/ ?>
		<div class="sectionHeader">Applications</div>
		<?php
		$appnames = $helper->getAppNames();
		foreach($appnames as $app) {
			$recruit = $helper->getRecruitLinkForApp($app);
			$devices = $helper->getDevicesLinkForApp($app);
			$install = $helper->getInstallLinkForApp($app);
			$crashes = $helper->getCrashesLinkForApp($app);
			$bundleid = $helper->getBundleIdForApp($app);
			$icon = $helper->getIconPathForApp($app);
		?>
		<div class="sectionRow">
			<table><tr>
			<td>
				<img class="sectionRowIcon" src="<?php echo $icon; ?>" width="50" height="50" />
			</td>
			<td>
				<a href="?a=vlist&app=<?php echo $app;?>"><?php echo $app;?></a>
				<div class="sectionRowAppLinks">
					<a class="alink" href="<?php echo $recruit ?>">Register</a>&nbsp;
					<a class="alink" href="<?php echo $install ?>">Install</a>&nbsp;
					<a class="alink" href="<?php echo $devices ?>">Device UDIDs</a>&nbsp;
					<a class="alink" href="<?php echo $crashes ?>">Crashes</a>
				</div>
			</td></tr></table>
		</div>
		<?php } ?>
		</div>
	<?php } ?>

	<?php if($action == "vlist") {
		/************************* vlist action **/
		$appname = $helper->getAppNameFromURL();
		$appversions = $helper->getAppVersions($appname);
		$icon = $helper->getIconPathForApp($appname);
		$bundleid = $helper->getBundleIdForApp($appname);
		?>
		<div class="sectionHeader">
			<table cellspacing=0 cellpadding=0><tr>
			<td width="75"><img class="sectionHeaderIcon" src="<?php echo $icon; ?>" width="50" height="50" /></td>
			<td><?php echo $appname; ?> Versions
			<div class="sectionHeaderAppBundleId"><?php echo $bundleid ?></div></td>
			</tr></table>
		</div>
		<div class="sectionMenu">
			<a href="?">Dashboard</a>
		</div>
		<?php if(count($appversions) < 1) { ?>
			<div class="sectionRow">No versions.</div>
		<?php } else { 
			foreach($appversions as $version) {
				$versionencoded = urlencode($version);
				$url = $helper->appsDirName . '/' . $appname . '/install/' . $version . '.html';
				?>
				<div class="sectionRow">
					<table cellspacing=0 cellpadding=0><tr>
						<td width="50%"><a href=" <?php echo $url; ?>"><?php echo $version?></a></td>
					</tr></table>
				</div>
			<?php } ?>
		<?php } ?>
	<?php } ?>

	<?php if($action == "clist") {
		/********************* crash list **/
		$app = urldecode($_GET['app']);
		$bundleid = $helper->getBundleIdForApp($app);
		$icon = $helper->getIconPathForApp($app);
		$crashes = $helper->getCrashesForApp($app);
		?>
		<div class="sectionHeader">
			<table cellspacing=0 cellpadding=0><tr>
			<td width="75"><img class="sectionHeaderIcon" src="<?php echo $icon; ?>" width="50" height="50" /></td>
			<td><?php echo $app; ?> Crashes
			<div class="sectionHeaderAppBundleId"><?php echo $bundleid ?></div></td>
			</tr></table>
		</div>
		<div class="sectionMenu">
			<a href="?">Dashboard</a>
		</div>
		<?php
		if(count($crashes) < 1) { ?>
			<div class="sectionRow">No Crash Reports</div>
		<?php
		} else {
			foreach($crashes as $crash) {
				$crashurl = $helper->getCrashLogPathForApp($app,$crash['crash']);
				?>
				<div class="sectionRow">
					<table cellpadding=0 cellspacing=0><tr>
					<td><a href="<?php echo $crashurl; ?>"><?php echo $crash['crash']; ?></a></td>
					<td align="right"><?php echo date('m/d/Y - g:i:sa',$crash['mtime']); ?></td>
					</tr></table>
				</div>
			<?php }
		} ?>
	<?php }?>
</div>
<pre class="session">
<?php var_dump($_SESSION); ?>
</pre>
</body>
</html>

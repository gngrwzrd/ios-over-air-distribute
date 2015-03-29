<?php
require_once("../../../simpledist.php");
$helper = new SimpleDist();
$app = $helper->getAppNameFromURL();
$data = file_get_contents('php://input');
$helper->saveCrashForApp($app,$data);
?>
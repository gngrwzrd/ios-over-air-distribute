<?php
require_once("../../simpledist.php");
$helper = new SimpleDist();
$location = $helper->saveDevice();
header("Location: " . $location);
?>

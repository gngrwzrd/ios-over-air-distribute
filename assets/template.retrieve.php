<?php
require_once("../../simpledist.php");
$helper = new SimpleDist();
$helper->saveDevice();
header("Location: {{baseurl}}/registered");
?>

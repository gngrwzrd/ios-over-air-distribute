<?php
$data = file_get_contents('php://input');
$crashfile = fopen("crashes/1.crash");
fwrite($crashfile,$data);
fclose($crashfile);
?>
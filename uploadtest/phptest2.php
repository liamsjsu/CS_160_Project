<?php
	define("LOG_FILE", "uploads/syslogClassShare.5");;
	$output = shell_exec('format.py ' . escapeshellarg(LOG_FILE));
	readfile('output.html');
?>
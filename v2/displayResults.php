<?php
	if (isset($_COOKIE["id_number"])){
    	$owner = $_COOKIE["id_number"];
		$path = "uploads/" . $owner . "/results";
    }
    else{
    	echo "Please log in to view your uploaded files.";
    	die();
    }
	$dh = opendir($path);
	$i=1;
	echo "<h3>View Past Results:</h3>";
	while (($file = readdir($dh)) !== false) {
	    if($file != "." && $file != ".." && $file != "index.php" && $file != ".htaccess" && $file != "error_log" && $file != "cgi-bin") {
	        echo "<a href='$path/$file'>$file</a><br /><br />";
	        $i++;
	    }
	}
	closedir($dh);
?> 
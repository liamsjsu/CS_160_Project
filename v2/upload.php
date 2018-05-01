<?php

$file_name = basename($_FILES["logFile"]["name"]); // saved to db
// Changed from uniqid() to a cookie based on the user's Google Account
//$unique_id = uniqid();
if (isset($_COOKIE["id_number"])){
    $unique_id = $_COOKIE["id_number"];
}
else{
    echo "Sorry, there was an error uploading your file.";
    die();
}
$file_dir = 'uploads/'.$unique_id.'/';
$file_path = $file_dir.$file_name; // saved to db
$uploadOk = 1;
$fileExtension = strtolower(pathinfo($file_path,PATHINFO_EXTENSION));

/* don't want to deal with this right now
// FILE RESTRICTIONS

// Check file size
if ($_FILES["logFile"]["size"] > 500000) {
    echo "File too large.<br>";
    $uploadOk = 0;
}

// change to switch statement for easy reading
// Allow certain file formats
if($fileExtension != "5" && $fileExtension != "csv" && $fileExtension != "flag" && $fileExtension != "txt" ) {
    echo "File must be of type 5, csv, flag, or txt.<br>";
    $uploadOk = 0;
}

*/

if ($uploadOk == 0) {
    echo "File not uploaded.<br>";
// if everything is ok, try to upload file
} else {

    // if directory doesnt exist, create it
    if (! is_dir($file_dir)) {
        mkdir($file_dir);
    }

    // upload file to directory $file_path
    if (move_uploaded_file($_FILES["logFile"]["tmp_name"], $file_path)) {

        // Process the file after uploading it
        $output = shell_exec('python format.py ' . escapeshellarg($file_dir) . " " . escapeshellarg($file_path) . " " . escapeshellarg($file_name));

        // file successfully uploaded to server, insert file into database
        // connect to mysql database
        $host = 'localhost';
        $user = 'root';
        $pass = 'root';
        $db = 'testdb';
        $conn = new mysqli($host, $user, $pass, $db);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        
        // DON'T FORGET \/ \/ \/
        // once i check out html session details, i can insert the session's userID into the SQL statement below

        // insertion into db
        $statement = "insert into logFiles (file_name, file_path, owner) 
        values ('$file_name', '$file_path', $unique_id)";
        //'$_COOKIE['id_number]'
        if ($conn->query($statement) === TRUE) {
            echo "New log inserted successfully<br>";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error . "<br>";
        }
        $conn->close();

        // no longer any need for the generated index
        /*
        // create new index for graph stuff
        $index = fopen($file_dir."index.php", "w") or die("Unable to create file!");
        fwrite($index,
            // edit $content to insert graphs
            '<?php

            $content = "'."this is a test index for file $file_name".'";

            echo \'<link href="../../eggplant.css" rel="stylesheet" type="text/css">\';
            include "../../Template.php"; ?>');
        fclose($index);
        */

        // confirmation
        echo "The file ".$file_name. " has been uploaded to $file_dir.<br>";
        echo "<a href='/uploadtest/files.php'>See your files</a><br>";
        
        // file successfully uploaded, redirect to files
        header("Location: files.php");
        die();
    } else {
        echo "Sorry, there was an error uploading your file.";
    }

}

?>
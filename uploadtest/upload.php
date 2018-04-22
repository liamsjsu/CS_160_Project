<?php

$file_name = basename($_FILES["logFile"]["name"]); // saved to db
$unique_id = uniqid();
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

    $statement = "insert into logFiles (file_name, file_path, owner) 
    values ('$file_name', '$file_path', 'test_owner')";
    if ($conn->query($statement) === TRUE) {
        echo "New log inserted successfully<br>";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error . "<br>";
    }
    $conn->close();

    // if directory doesnt exist, create it
    if (! is_dir($file_dir)) {
        mkdir($file_dir);
    }

    // upload file to directory $file_path
    if (move_uploaded_file($_FILES["logFile"]["tmp_name"], $file_path)) {
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
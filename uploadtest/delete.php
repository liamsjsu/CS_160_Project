<?php

$host = 'localhost';
$user = 'root';
$pass = 'root';
$db = 'testdb';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$statement = "select * from logfiles";
$result = $conn->query($statement);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        // print_r($_POST['data']); //for testing purposes
        // $_POST['data'][$row['file_name']] <- this took me soooo long to get right
        $statement = "delete from logfiles where file_path = '".$_POST['data'][$row['file_name']]."'";
        if ($conn->query($statement) === TRUE) {
            echo "File deleted successfully<br>";
        } else {
            echo "Error deleting file from database: " . $conn->error . "<br>";
        }
    }
} else { // no data found to delete
  echo "Nothing to delete.<br>";
}

// Once file is deleted, go back to file manager
header("Location: files.php");
die();
?>
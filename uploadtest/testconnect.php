<?php
$host = 'localhost';
$user = 'root';
$pass = 'root';
$db = 'testdb';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$statement = "insert into logFiles (file_name, file_path, owner) 
values ('test_file_name', 'test_file_path', 'test_owner')";
if ($conn->query($statement) === TRUE) {
    echo "New log inserted successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
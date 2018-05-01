<?php
echo 
'<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Files</title>
<link href="eggplant.css" rel="stylesheet" type="text/css">
<script src="eggplant.js"></script>
<meta name="google-signin-scope" content="profile email">
<meta name="google-signin-client_id" content="773730468254-82509noo29h6q37nbepago8ksko4a2as.apps.googleusercontent.com">
<script src="https://apis.google.com/js/platform.js" async defer></script>
</head>

<body>
<div class="container">
    <div class="nav">
        <a href="index.html">HOME</a>
        <a href="#about">ABOUT</a>
        <div class = "drop">
            <a onclick="drop()">ACCOUNT</a>
            <div id="dropdown" class="drop-menu">
                <div class="g-signin2" data-onsuccess="onSignIn"></div>
                <a href="" onclick="signOut();">Sign Out</a>
            </div>
        </div>
    </div>
<div class="header">
    <div class="image"><img src="header.jpg"/></div>
    <h2 class="txt1">THIS IS <span class="txt2">EGGPLANT</span></h2>
    <p class="txt3">A FREE LOG PROCESSING TOOL</p>
</div>

<div class="list">';

//Set owner to Google id
if (isset($_COOKIE["id_number"])){
    $owner = $_COOKIE["id_number"];
}
else{
    echo "Sorry, an error has occured.";
    die();
}

echo "<a href='upload.html'>Back to Upload</a><br><br>";
echo "Logs belonging to " . $_COOKIE["user_name"] . ":<br>";
echo "<form action='delete.php' method='post'>";
echo "<table border='1'>";
$host = 'localhost';
$user = 'root';
$pass = 'root';
$db = 'testdb';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$statement = "select * from logfiles where owner = '" . $owner . "'";
$result = $conn->query($statement);

// Delete button has not been tested yet, view analysis button needs to be redone later
if ($result->num_rows > 0) { // data found (at least 1 row)
  while ($row = $result->fetch_assoc()) {
      echo "<tr>";
      echo "<td>".$row["file_name"]."</td>";
      echo "<td><a href='".dirname(substr($row['file_path'], 0, -3)).'/results/'.$row['file_name'].'.html'."'>View Analysis</a></td>";
      echo "<td><button type='submit' value='".$row["file_path"]."' name='data[".$row["file_name"]."]'>Delete File</button></td>";
      echo "</tr>";
  }
} else {
  echo "No log files uploaded yet.<br>";
}

$conn->close();
echo "</table>";
echo "</form>";

echo
'<section class="about" id="about">
<h2 class="parallax">ABOUT EGGPLANT</h2>
<p class="parallax_description">Eggplant is a free tool written in Python 3.0 for analyzing log files. It is a web-based tool, so the frontend is developed with html. It is only for educational use.</p>
</section>
<section class="footer_banner">
<h4>Team Eggplant</h4>
<p>(Blanchy Polancos, Gabriella Qiu, Henry Ngo, Patrick Leung)</p>
<h4><a href="https://github.com/liamsjsu/CS_160_Project/">Explore on Github</a></h4>
</section>

<!-- Copyrights Section -->
<div class="copyright">&copy;2018 - Team eggplant<strong></strong></div>
</div>
</body>
</html>';
?>

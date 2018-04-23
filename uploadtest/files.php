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
<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="YOUR_CLIENT_ID.apps.googleusercontent.com">
</head>

<body>
<div class="container">
<header>
    <nav>
      <ul>
        <li><a href="index.html">HOME</a></li>
        <li><a href="#about">ABOUT</a></li>
		<li><a href="" id="sign">ACCOUNT</a></li>
		<div class="g-signin2" data-onsuccess="onSignIn" id="gsign" style="display: none"></div>
      </ul>
    </nav>
</header>
<section class="banner">
    <h2 class="banner_header">THIS IS <span class="banner2">EGGPLANT</span></h2>
    <p class="tagline">A FREE LOG PROCESSING TOOL</p>
  </section>
  <div class="list">';

$owner = 'test_owner';

echo "<a href='upload.html'>Back to Upload</a><br><br>";
echo "Logs belonging to " . $owner . ":<br>";
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

if ($result->num_rows > 0) { // data found (at least 1 row)
  while ($row = $result->fetch_assoc()) {
      echo "<tr>";
      echo "<td>".$row["file_name"]."</td>";
      echo "<td><button type='submit' value='".$row["file_path"]."' name='data[".$row["file_name"]."]'>Delete</button></td>";
      echo "</tr>";
  }
} else {
  echo "No log files uploaded yet.<br>";
}

$conn->close();
echo "</table>";
echo "</form>";

echo
'</div>
<section class="about" id="about">
  <h2 class="parallax">ABOUT EGGPLANT</h2>
  <p class="parallax_description">Eggplant is a free tool written in Python 3.0 for analyzing log files. It is a web-based tool, so the frontend is developed with html. It is only for educational use.</p>
</section>
<section class="footer_banner">
  <h2>A TOOL CREATED BY </h2>
	<h4>Team Eggplant</h4>
	<p>(Liam Jensen, Gabriella Qiu, Patrick Leung, Henry Ngo, Blanchy Polancos)</p>
	<h4><a href="https://github.com/liamsjsu/CS_160_Project/">Explore on Github</a></h4>
	</section>
  <!-- Copyrights Section -->
  <div class="copyright">&copy;2018 - Team eggplant<strong></strong></div>
</div>
</body>
</html>';
?>
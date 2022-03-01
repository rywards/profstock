<!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" href="style.css">
</head>

<body>

<?php
// https://www.w3schools.com/php/php_mysql_insert.asp
// This is where I learned how to connect and insert into a mysql table
$servername = "localhost";
$username = "root";
$password = "wwcVs5kt";
$dbname = "profstock";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

?>

<h1>Entering and Retreiving from Database</h1>
<br />

<div class="text-fields">
<label for="firstName">First name:</label>
<input type="text" id="firstName" name="firstName">
<br />

<label for="lastName">Last name:</label>
<input type="text" id="lastName" name="lastName">
<br />

<button onclick="sendToDatabase()">Submit</button>
</div>

<script>
function sendToDatabase() {
    firstName = document.getElementById("firstName").value;
    lastName = document.getElementById("lastName").value;

  <?php
    // Get info from database
    $sql = "SELECT firstname, lastname ";
    $sql .= "FROM users;";
    $stmt = $conn->prepare($sql);
    $stmt->execute();

    // Display the data received from database
    foreach($stmt->fetchAll() as $row) {
      echo '$row[firstname] . $row[lastname]\n';
    }

    // Insert statement
    $sql = "INSERT INTO users(firstname, lastname) ";
    $sql .= "VALUES (firstName, lastName);";
    
    // Run the insert
    if ($conn->query($sql) === TRUE) {
      // Insert was successful, display data again to show it went through
      $sql = "SELECT firstname, lastname ";
      $sql .= "FROM users;";
      $stmt = $conn->prepare($sql);
      $stmt->execute();

      // Display the data received from database
      foreach($stmt->fetchAll() as $row) {
        echo '$row[firstname] . $row[lastname]\n';
      }
    } else {
      // Insert did not go through
      echo "Error";
    }

  ?>
}

</script>

</body>
</html>

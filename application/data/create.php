<?php

/**
  * Use an HTML form to create a new entry in the
  * users table.
  *
  */


if (isset($_POST['submit'])) {
  require "../config.php";
  require "../common.php";

  try {
    $connection = new PDO($dsn, $username, $password, $options);

    $new_user = array(
      "firstname" => $_POST['firstname'],
      "lastname"  => $_POST['lastname'],
      "email"     => $_POST['email'],
      "age"       => $_POST['age'],
      "location"  => $_POST['location']
    );

    $sql = sprintf(
"INSERT INTO %s (%s) values (%s)",
"users",
implode(", ", array_keys($new_user)),
":" . implode(", :", array_keys($new_user))
    );

    $statement = $connection->prepare($sql);
    $statement->execute($new_user);
  } catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
  }

}
?>

<?php require "templates/header.php"; ?>

<?php if (isset($_POST['submit']) && $statement) { ?>
  > <?php echo $_POST['username']; ?> successfully added.
<?php } ?>

<h2>Add a user</h2>

<form method="post">
  <label for="name">First Name</label>
  <input type="text" name="name" id="name">
  <label for="username">Username</label>
  <input type="text" name="username" id="username">
  <label for="password">Password</label>
  <input type="text" name="password" id="password">
  <label for="gender">Gender</label>
  <input type="text" name="gender" id="gender">
  <label for="weight">Current Weight</label>
  <input type="text" name="weight" id="weight">
  <label for="weight_goal">Current Weight Goal</label>
  <input type="text" name="weight_goal" id="weight_goal">
  <label for="budget">Desired Budget</label>
  <input type="text" name="budget" id="budget">
  <label for="location">Current City</label>
  <input type="text" name="location" id="location">
  <input type="submit" name="submit" value="Submit">
</form>

<a href="index.php">Back to home</a>

<?php require "templates/footer.php"; ?>

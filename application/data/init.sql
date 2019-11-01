CREATE DATABASE test;

  use test;

  CREATE TABLE users (
    id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(50) NOT NULL,
    gender VARCHAR(1),
    weight FLOAT,
    weight_goal FLOAT,
    budget FLOAT,
    location VARCHAR(50),
  );

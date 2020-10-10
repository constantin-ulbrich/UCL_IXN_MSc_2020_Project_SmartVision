/* Make sure the database does not exist */
DROP DATABASE IF EXISTS SmartVisionDatabase;

/* Creating the Database for the Website ubit*/
CREATE DATABASE SmartVisionDatabase
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;


/* Make sure the user does not exist */
DROP USER IF EXISTS "smartVisionUser"@"localhost";

/* Create a user on the server*/
CREATE USER "smartVisionUser"@"localhost" IDENTIFIED BY "12345SmartVision";

/* Assign privileges to the user (still Add WITH MAX QUERIES PER HOUR)*/
GRANT SELECT, UPDATE, INSERT, DELETE
ON SmartVisionDatabase.*
TO "smartVisionUser"@"localhost" IDENTIFIED BY "12345SmartVision";


/*Create customers table*/
CREATE TABLE SmartVisionDatabase.frameAnalysis
(
    frame_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    occupied BOOLEAN NOT NULL,
    occupation_score INT NOT NULL,
    person_detected BOOLEAN NOT NULL,
    dominant_emotion VARCHAR(100),
    smile BOOLEAN,
    time_recorded TIMESTAMP NOT NULL
)
ENGINE = InnoDB;


CREATE TABLE SmartVisionDatabase.actionAnalysis
(
    action_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    action_identified BOOLEAN NOT NULL,
    action_name VARCHAR(200),
    time_recorded TIMESTAMP NOT NULL
)
ENGINE = InnoDB;


CREATE TABLE SmartVisionDatabase.probabilityThresholds
(
    threshold_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    analysed_item VARCHAR(200) NOT NULL,
    prob_threshold FLOAT(5,3) NOT NULL
)
ENGINE = InnoDB;


CREATE TABLE SmartVisionDatabase.customVisionObjectScore
(
    object_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    object_name VARCHAR(200) NOT NULL,
    object_score INT NOT NULL
)
ENGINE = InnoDB;


CREATE TABLE SmartVisionDatabase.developer
(
    developer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    institution VARCHAR(300) NOT NULL,
    department VARCHAR(300) NOT NULL,
    email VARCHAR(200) NOT NULL,
    password VARCHAR(100) NOT NULL
)
ENGINE = InnoDB;



/*Inserting a root admin account (The password is "rootAdmin" and the username is "root.admin@smile.com") */
INSERT INTO SmartVisionDatabase.developer (first_name, last_name, institution, department, email, password) 
VALUES ('RootDeveloper', 'RootDeveloper', 'Developer', 'Developer', 'root.developer@smartvision.com', 'SmartVision12345');

/*Inserting key objects of the SmartVision Algorithm and Key Emotions into the table "probabilityThresholds" */
INSERT INTO SmartVisionDatabase.probabilityThresholds (analysed_item, prob_threshold) 
VALUES 
    ('customVisionObjects', 0.2),
    ('emotions', 0.5),
    ('smile', 0.5),
    ('accessories', 0.5),
    ('facialHair', 0.5),
    ('hair', 0.5),
    ('computerVisionObjects', 0.1);

/*Inserting key objects of the Custom Vision Algorithm with associated occupation score into the table "customVisionObjectScore" */
INSERT INTO SmartVisionDatabase.customVisionObjectScore (object_name, object_score) 
VALUES 
    ("pencil", 2),
    ("Office supplies", 5),
    ("Laptop", 60),
    ("person", 100),
    ("jacket", 35),
    ("smartphone", 50),
    ("computer mouse", 2),
    ("computer keyboard", 2),
    ("Tableware", 10),
    ("drinking glass", 10),
    ("Bottle", 15),
    ("folder", 20),
    ("paper", 5),
    ("notebook", 20),
    ("Luggage and bags", 35),
    ("key", 60),
    ("key chain", 60),
    ("car key", 60),
    ("credit card", 60),
    ("pen", 2),
    ("Box", 5),
    ("fork", 10),
    ("knife", 10),
    ("Spoon", 10),
    ("badminton racket", 15),
    ("Racket", 15),
    ("suit", 20),
    ("tie", 15),
    ("handbag", 35),
    ("headphones", 40),
    ("in-ear headphones", 40),
    ("Eyeglasses", 40),
    ("Glasses", 40),
    ("wallet", 60),
    ("book", 15),
    ("Banana", 25),
    ("Apple", 25);

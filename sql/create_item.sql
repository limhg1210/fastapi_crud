CREATE TABLE item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(64),
    content LONGTEXT
);
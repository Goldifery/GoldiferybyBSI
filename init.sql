USE goldify_db;

CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (username, password)
VALUES ('irsal', 'hashed_password_di_sini');

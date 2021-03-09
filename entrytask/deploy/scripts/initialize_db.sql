DROP TABLE IF EXISTS user_tab;
DROP TABLE IF EXISTS role_tab;
DROP TABLE IF EXISTS user_role_tab;
DROP TABLE IF EXISTS event_tab;
DROP TABLE IF EXISTS comment_tab;
DROP TABLE IF EXISTS like_tab;
DROP TABLE IF EXISTS participation_tab;
DROP TABLE IF EXISTS image_tab;
DROP TABLE IF EXISTS event_image_tab;
DROP TABLE IF EXISTS channel_tab;
DROP TABLE IF EXISTS event_channel_tab;



-- USER TABLE
CREATE TABLE user_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    fullname NVARCHAR(100) NOT NULL,
    email VARCHAR(70) NOT NULL UNIQUE,
    salt VARCHAR(60) NOT NULL,
    salted_password VARCHAR(120) NOT NULL,
    create_time INT UNSIGNED NOT NULL,
    update_time INT UNSIGNED NOT NULL,

    INDEX (username)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- ROLE TABLE
CREATE TABLE role_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    rolename VARCHAR(30) NOT NULL UNIQUE
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- USER ROLE TABLE
CREATE TABLE user_role_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    role_id BIGINT UNSIGNED NOT NULL,
    INDEX (user_id)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- EVENT TABLE
CREATE TABLE event_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    title NVARCHAR(100)  NOT NULL,
    content NVARCHAR(1000) NOT NULL,
    start_date INT UNSIGNED NOT NULL,
    end_date INT UNSIGNED NOT NULL,
    create_uid BIGINT UNSIGNED NOT NULL,
    create_time INT UNSIGNED NOT NULL,
    update_time INT UNSIGNED NOT NULL,
    location NVARCHAR(100),

    INDEX (create_time),
    INDEX (start_date, end_date),
    INDEX (location)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- IMAGE TABLE
CREATE TABLE image_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    image_url VARCHAR(255) NOT NULL
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- EVENT IMAGE TABLE
CREATE TABLE event_image_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    event_id BIGINT UNSIGNED NOT NULL,
    image_id BIGINT UNSIGNED NOT NULL,
    INDEX (event_id)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- CHANNEL TABLE
CREATE TABLE channel_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    INDEX (name)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- EVENT CHANNEL TABLE
CREATE TABLE event_channel_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    event_id BIGINT UNSIGNED NOT NULL,
    channel_id BIGINT UNSIGNED NOT NULL,
    INDEX (event_id),
    INDEX (channel_id)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;


-- COMMENT TABLE
CREATE TABLE comment_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    event_id BIGINT UNSIGNED NOT NULL,
    content NVARCHAR(255) NOT NULL,
    create_time INT UNSIGNED NOT NULL,
    update_time INT UNSIGNED NOT NULL,

    INDEX (event_id, create_time)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;

-- LIKE TABLE
CREATE TABLE like_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    event_id BIGINT UNSIGNED NOT NULL UNIQUE,

    INDEX (event_id),
    INDEX (user_id)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;


-- PARTICIPATION TABLE
CREATE TABLE participation_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    event_id BIGINT UNSIGNED NOT NULL UNIQUE,
    create_time INT UNSIGNED NOT NULL,

    INDEX (event_id),
    INDEX (user_id)
) COLLATE='utf8mb4_unicode_ci' ENGINE=INNODB;
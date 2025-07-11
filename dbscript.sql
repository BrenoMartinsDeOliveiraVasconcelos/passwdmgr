

CREATE TABLE IF NOT EXISTS `data`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `entity` TEXT,
    `username` TEXT,
    `encrypted_password` BLOB,
    `nonce` BLOB,
    `tag` BLOB
);
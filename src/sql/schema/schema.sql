CREATE TABLE `users` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `username` varchar(50) UNIQUE NOT NULL,
  `email` varchar(200) UNIQUE NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) DEFAULT "",
  `date_created` datetime NOT NULL DEFAULT NOW(),
  `date_updated` datetime NOT NULL DEFAULT NOW(),
  `hashed_key` text NOT NULL,
  `is_active` boolean NOT NULL DEFAULT true
);

CREATE TABLE `threads` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `creator_id` int NOT NULL,
  `date_created` datetime NOT NULL,
  `name` text NOT NULL
);

CREATE TABLE `messages` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `thread_id` int NOT NULL,
  `date_created` datetime NOT NULL,
  `message` text NOT NULL,
  `role` varchar(100) NOT NULL
);

ALTER TABLE `threads` ADD FOREIGN KEY (`creator_id`) REFERENCES `users` (`id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`thread_id`) REFERENCES `threads` (`id`);
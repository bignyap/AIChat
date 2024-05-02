CREATE TABLE `users` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) UNIQUE NOT NULL,
  `username` varchar(50) UNIQUE NOT NULL,
  `email` varchar(200) UNIQUE NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) DEFAULT "",
  `date_created` datetime NOT NULL DEFAULT NOW(),
  `date_updated` datetime NOT NULL DEFAULT NOW()
);

CREATE TABLE `user_prompt` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(250) NOT NULL,
  `prompt` text NOT NULL
);

CREATE TABLE `user_setting` (
  `user_id` int NOT NULL,
  `default_model` varchar(250) NOT NULL,
  `prompt_id` int DEFAULT NULL
);

CREATE TABLE `threads` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `creator_id` int NOT NULL,
  `date_created` datetime NOT NULL,
  `name` text NOT NULL,
  `prompt_id` int DEFAULT NULL,
  `prompt` text DEFAULT NULL
);

CREATE TABLE `messages` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `message_group` varchar(50) NOT NULL,
  `thread_id` int NOT NULL,
  `date_created` datetime NOT NULL,
  `message` text NOT NULL,
  `role` varchar(100) NOT NULL
);

ALTER TABLE `user_prompt` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `user_setting` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `user_setting` ADD FOREIGN KEY (`prompt_id`) REFERENCES `user_prompt` (`id`);

ALTER TABLE `threads` ADD FOREIGN KEY (`creator_id`) REFERENCES `users` (`id`);

ALTER TABLE `threads` ADD FOREIGN KEY (`prompt_id`) REFERENCES `user_prompt` (`id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`thread_id`) REFERENCES `threads` (`id`);

INSERT INTO `user_prompt` (`name`, `prompt`) VALUES 
('ChatAssistant', 'You are a helpful chat assistant. Help with the questions asked as much as possible.');
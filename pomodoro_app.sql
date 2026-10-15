-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 15 juin 2025 à 15:36
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `pomodoro_app`
--

-- --------------------------------------------------------

--
-- Structure de la table `app_settings`
--

CREATE TABLE `app_settings` (
  `id` int(11) NOT NULL,
  `work_duration` int(11) DEFAULT 25,
  `short_break_duration` int(11) DEFAULT 5,
  `long_break_duration` int(11) DEFAULT 15,
  `long_break_interval` int(11) DEFAULT 4,
  `notifications_enabled` tinyint(1) DEFAULT 1,
  `daily_pomodoro_goal` int(11) DEFAULT 8
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `pomodoro_sessions`
--

CREATE TABLE `pomodoro_sessions` (
  `id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `session_type` enum('work','short_break','long_break') NOT NULL,
  `duration` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `completed` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `projects`
--

CREATE TABLE `projects` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `target_pomodoros` int(11) DEFAULT 8,
  `completed_pomodoros` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `app_settings`
--
ALTER TABLE `app_settings`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `pomodoro_sessions`
--
ALTER TABLE `pomodoro_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_id` (`project_id`);

--
-- Index pour la table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `app_settings`
--
ALTER TABLE `app_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `pomodoro_sessions`
--
ALTER TABLE `pomodoro_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=144;

--
-- AUTO_INCREMENT pour la table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `pomodoro_sessions`
--
ALTER TABLE `pomodoro_sessions`
  ADD CONSTRAINT `pomodoro_sessions_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

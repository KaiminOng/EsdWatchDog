-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: mysqldb
-- Generation Time: Apr 02, 2020 at 03:59 PM
-- Server version: 5.7.29
-- PHP Version: 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `watchdog`
--
CREATE DATABASE IF NOT EXISTS `watchdog` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `watchdog`;

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id` varchar(120) NOT NULL,
  `username` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `username`) VALUES
('176814266', 'Kae97x'),
('308563716', 'kohwayne');

-- --------------------------------------------------------

--
-- Table structure for table `accountEndpoint`
--

CREATE TABLE `accountEndpoint` (
  `id` int(11) NOT NULL,
  `account_id` varchar(120) NOT NULL,
  `endpoint_url` varchar(120) NOT NULL,
  `chat_id` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `chat_id` varchar(120) NOT NULL,
  `chat_owner_id` varchar(120) NOT NULL,
  `chat_title` varchar(120) DEFAULT NULL,
  `chat_type` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `endpoint`
--

CREATE TABLE `endpoint` (
  `endpoint_url` varchar(120) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `last_checked` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `monitoring`
--

CREATE TABLE `monitoring` (
  `event_id` int(11) NOT NULL,
  `endpoint_url` varchar(120) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `accountEndpoint`
--
ALTER TABLE `accountEndpoint`
  ADD PRIMARY KEY (`id`),
  ADD KEY `endpoint_url` (`endpoint_url`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`chat_id`,`chat_owner_id`),
  ADD KEY `chat_owner_id` (`chat_owner_id`);

--
-- Indexes for table `endpoint`
--
ALTER TABLE `endpoint`
  ADD PRIMARY KEY (`endpoint_url`);

--
-- Indexes for table `monitoring`
--
ALTER TABLE `monitoring`
  ADD PRIMARY KEY (`event_id`),
  ADD UNIQUE KEY `endpoint_url` (`endpoint_url`,`timestamp`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accountEndpoint`
--
ALTER TABLE `accountEndpoint`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `monitoring`
--
ALTER TABLE `monitoring`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accountEndpoint`
--
ALTER TABLE `accountEndpoint`
  ADD CONSTRAINT `accountEndpoint_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  ADD CONSTRAINT `accountEndpoint_ibfk_2` FOREIGN KEY (`endpoint_url`) REFERENCES `endpoint` (`endpoint_url`),
  ADD CONSTRAINT `accountEndpoint_unique` UNIQUE (`account_id`, `endpoint_url`, `chat_id`);

--
-- Constraints for table `contact`
--
ALTER TABLE `contact`
  ADD CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`chat_owner_id`) REFERENCES `account` (`id`);

--
-- Constraints for table `monitoring`
--
ALTER TABLE `monitoring`
  ADD CONSTRAINT `monitoring_ibfk_1` FOREIGN KEY (`endpoint_url`) REFERENCES `endpoint` (`endpoint_url`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

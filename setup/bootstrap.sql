-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 30, 2020 at 05:21 PM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `watchdog`
--
DROP DATABASE IF EXISTS `watchdog`;
CREATE DATABASE IF NOT EXISTS `watchdog` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `watchdog`;

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `id` varchar(120) NOT NULL,
  `username` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `username`) VALUES
('176814266', 'Kae97x'),
('308563716', 'kohwayne'),
('1234567', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `accountendpoint`
--

DROP TABLE IF EXISTS `accountendpoint`;
CREATE TABLE IF NOT EXISTS `accountendpoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(120) NOT NULL,
  `endpoint_url` varchar(120) NOT NULL,
  `chat_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_id` (`account_id`,`endpoint_url`,`chat_id`),
  KEY `endpoint_url` (`endpoint_url`),
  KEY `chat_id` (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accountendpoint`
--

INSERT INTO `accountendpoint` (`id`, `account_id`, `endpoint_url`, `chat_id`) VALUES
(7, '308563716', 'http://facebook.com', -393119922),
(5, '308563716', 'http://finance.yahoo.com', -393119922),
(3, '308563716', 'http://google.com', -393119922),
(8, '308563716', 'www.twitter.com', -393119922),
(9, '308563716', 'www.twitter.com', 308563716);

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
CREATE TABLE IF NOT EXISTS `contact` (
  `chat_id` int(11) NOT NULL,
  `chat_owner_id` varchar(120) NOT NULL,
  `chat_title` varchar(120) DEFAULT NULL,
  `chat_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`chat_id`,`chat_owner_id`),
  KEY `chat_owner_id` (`chat_owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`chat_id`, `chat_owner_id`, `chat_title`, `chat_type`) VALUES
(-393119922, '1234567', 'ESD AIM NO ZERO G5T6', 'group'),
(-393119922, '308563716', 'ESD AIM NO ZERO G5T6', 'group'),
(176814266, '176814266', 'private', 'private'),
(308563716, '308563716', 'private', 'private');

-- --------------------------------------------------------

--
-- Table structure for table `endpoint`
--

DROP TABLE IF EXISTS `endpoint`;
CREATE TABLE IF NOT EXISTS `endpoint` (
  `endpoint_url` varchar(120) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `last_checked` int(11) DEFAULT NULL,
  PRIMARY KEY (`endpoint_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `endpoint`
--

INSERT INTO `endpoint` (`endpoint_url`, `status`, `last_checked`) VALUES
('http://facebook.com', NULL, NULL),
('http://finance.yahoo.com', NULL, NULL),
('http://google.com', NULL, NULL),
('http://youtube.com', NULL, NULL),
('www.twitter.com', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `monitoring`
--

DROP TABLE IF EXISTS `monitoring`;
CREATE TABLE IF NOT EXISTS `monitoring` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint_url` varchar(120) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `endpoint_url` (`endpoint_url`,`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `monitoring`
--

INSERT INTO `monitoring` (`event_id`, `endpoint_url`, `timestamp`, `status`) VALUES
(2, 'http://google.com', 123456, 'unhealthy'),
(4, 'http://google.com', 56789, 'healthy');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accountendpoint`
--
ALTER TABLE `accountendpoint`
  ADD CONSTRAINT `accountendpoint_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  ADD CONSTRAINT `accountendpoint_ibfk_2` FOREIGN KEY (`endpoint_url`) REFERENCES `endpoint` (`endpoint_url`),
  ADD CONSTRAINT `accountendpoint_ibfk_3` FOREIGN KEY (`chat_id`) REFERENCES `contact` (`chat_id`);

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

mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: watchdog
-- ------------------------------------------------------
-- Server version	5.7.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `watchdog`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `watchdog` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `watchdog`;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` varchar(120) NOT NULL,
  `username` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('176814266','Kae97x'),('308563716','kohwayne');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accountEndpoint`
--

DROP TABLE IF EXISTS `accountEndpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accountEndpoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(120) NOT NULL,
  `endpoint_url` varchar(120) NOT NULL,
  `chat_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_id` (`account_id`,`endpoint_url`,`chat_id`),
  KEY `endpoint_url` (`endpoint_url`),
  CONSTRAINT `accountEndpoint_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `accountEndpoint_ibfk_2` FOREIGN KEY (`endpoint_url`) REFERENCES `endpoint` (`endpoint_url`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accountEndpoint`
--

LOCK TABLES `accountEndpoint` WRITE;
/*!40000 ALTER TABLE `accountEndpoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `accountEndpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `chat_id` int(11) NOT NULL,
  `chat_owner_id` varchar(120) NOT NULL,
  `chat_title` varchar(120) DEFAULT NULL,
  `chat_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`chat_id`,`chat_owner_id`),
  KEY `chat_owner_id` (`chat_owner_id`),
  CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`chat_owner_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `endpoint`
--

DROP TABLE IF EXISTS `endpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `endpoint` (
  `endpoint_url` varchar(120) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `last_checked` int(11) DEFAULT NULL,
  PRIMARY KEY (`endpoint_url`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endpoint`
--

LOCK TABLES `endpoint` WRITE;
/*!40000 ALTER TABLE `endpoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `endpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitoring`
--

DROP TABLE IF EXISTS `monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint_url` varchar(120) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `endpoint_url` (`endpoint_url`,`timestamp`),
  CONSTRAINT `monitoring_ibfk_1` FOREIGN KEY (`endpoint_url`) REFERENCES `endpoint` (`endpoint_url`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitoring`
--

LOCK TABLES `monitoring` WRITE;
/*!40000 ALTER TABLE `monitoring` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitoring` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-01 16:06:49

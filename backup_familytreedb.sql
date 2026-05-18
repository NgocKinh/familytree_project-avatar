-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: familytreedb
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gene_log`
--

DROP TABLE IF EXISTS `gene_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gene_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `executor` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `old_prefix` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `new_prefix` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `affected_count` int DEFAULT NULL,
  `action_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gene_log`
--

LOCK TABLES `gene_log` WRITE;
/*!40000 ALTER TABLE `gene_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `gene_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lineage`
--

DROP TABLE IF EXISTS `lineage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lineage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `original_place` varchar(200) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_lineage_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lineage`
--

LOCK TABLES `lineage` WRITE;
/*!40000 ALTER TABLE `lineage` DISABLE KEYS */;
/*!40000 ALTER TABLE `lineage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marriage`
--

DROP TABLE IF EXISTS `marriage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marriage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `spouse_a_id` int NOT NULL,
  `spouse_b_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status enum('married','separated','divorced','widowed','cohabiting') DEFAULT ...married',
  `ceremony_type` enum('civil','traditional','religious') DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `notes` text,
  `consanguineous` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_marriage_spouses` (`spouse_a_id`,`spouse_b_id`),
  UNIQUE KEY `uq_marriage_pair` (`spouse_a_id`,`spouse_b_id`,`start_date`),
  KEY `idx_m_a` (`spouse_a_id`),
  KEY `idx_m_b` (`spouse_b_id`),
  KEY `idx_marriage_a` (`spouse_a_id`),
  KEY `idx_marriage_b` (`spouse_b_id`),
  CONSTRAINT `fk_m_a` FOREIGN KEY (`spouse_a_id`) REFERENCES `person` (`person_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_m_b` FOREIGN KEY (`spouse_b_id`) REFERENCES `person` (`person_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marriage`
--

LOCK TABLES `marriage` WRITE;
/*!40000 ALTER TABLE `marriage` DISABLE KEYS */;
INSERT INTO `marriage` VALUES (15,5,8,'1990-11-03',NULL,'married',NULL,'','Xuân Thịnh',0),(16,11,13,NULL,NULL,'married',NULL,NULL,NULL,NULL),(18,7,10,NULL,NULL,'married',NULL,NULL,NULL,NULL),(19,30,31,NULL,NULL,'married',NULL,NULL,NULL,NULL),(20,34,35,NULL,NULL,'married',NULL,NULL,NULL,NULL),(21,36,37,NULL,NULL,'married',NULL,NULL,NULL,NULL),(22,18,40,NULL,NULL,'married',NULL,NULL,NULL,NULL),(23,21,32,NULL,NULL,'married',NULL,NULL,NULL,NULL),(24,12,33,NULL,NULL,'married',NULL,NULL,NULL,NULL),(25,22,45,NULL,NULL,'married',NULL,NULL,NULL,NULL),(26,15,47,NULL,NULL,'married',NULL,NULL,NULL,NULL),(27,5,70,NULL,NULL,'separated',NULL,NULL,NULL,NULL),(30,67,71,NULL,NULL,'married',NULL,NULL,NULL,NULL),(31,72,73,NULL,NULL,'married',NULL,NULL,NULL,NULL),(32,75,76,NULL,NULL,'married',NULL,NULL,NULL,NULL),(33,79,41,NULL,NULL,'divorced',NULL,'','',0),(36,89,90,NULL,NULL,NULL,NULL,NULL,NULL,0),(37,83,84,NULL,NULL,NULL,NULL,NULL,NULL,0),(40,19,69,NULL,NULL,'married',NULL,'','',0),(45,92,93,NULL,NULL,'married',NULL,'','',0),(50,97,98,NULL,NULL,'',NULL,'','',0),(51,108,109,NULL,NULL,'married',NULL,'','',0),(52,103,99,NULL,NULL,'married',NULL,'','',0),(53,104,105,NULL,NULL,'married',NULL,'','',0);
/*!40000 ALTER TABLE `marriage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `marriage_pair`
--

DROP TABLE IF EXISTS `marriage_pair`;
/*!50001 DROP VIEW IF EXISTS `marriage_pair`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `marriage_pair` AS SELECT 
 1 AS `id`,
 1 AS `a`,
 1 AS `b`,
 1 AS `start_date`,
 1 AS `end_date`,
 1 AS `status`,
 1 AS `ceremony_type`,
 1 AS `location`,
 1 AS `notes`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `parent_child`
--

DROP TABLE IF EXISTS `parent_child`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parent_child` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_id` int NOT NULL,
  `child_id` int NOT NULL,
  `marriage_id` int DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_parent_child` (`parent_id`,`child_id`,`type`),
  UNIQUE KEY `uq_child_parent_type` (`child_id`,`type`),
  KEY `idx_pc_parent` (`parent_id`),
  KEY `idx_pc_child` (`child_id`),
  KEY `fk_parent_child_marriage` (`marriage_id`),
  KEY `idx_parent_child_parent` (`parent_id`),
  CONSTRAINT `fk_parent_child_marriage` FOREIGN KEY (`marriage_id`) REFERENCES `marriage` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_pc_child` FOREIGN KEY (`child_id`) REFERENCES `person` (`person_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pc_parent` FOREIGN KEY (`parent_id`) REFERENCES `person` (`person_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_parent_type` CHECK ((`type` in (_utf8mb4'father',_utf8mb4'mother')))
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent_child`
--

LOCK TABLES `parent_child` WRITE;
/*!40000 ALTER TABLE `parent_child` DISABLE KEYS */;
INSERT INTO `parent_child` VALUES (1,5,11,NULL,'father',NULL),(2,5,12,NULL,'father',NULL),(3,5,41,NULL,'father',NULL),(4,7,4,NULL,'father',NULL),(5,7,5,NULL,'father',NULL),(6,7,15,NULL,'father',NULL),(7,7,18,NULL,'father',NULL),(8,7,19,NULL,'father',NULL),(9,7,21,NULL,'father',NULL),(10,7,22,NULL,'father',NULL),(11,7,39,NULL,'father',NULL),(12,8,11,NULL,'mother',NULL),(13,8,12,NULL,'mother',NULL),(14,10,4,NULL,'mother',NULL),(15,10,5,NULL,'mother',NULL),(16,10,15,NULL,'mother',NULL),(17,10,18,NULL,'mother',NULL),(18,10,19,NULL,'mother',NULL),(19,10,21,NULL,'mother',NULL),(20,10,22,NULL,'mother',NULL),(21,10,39,NULL,'mother',NULL),(22,11,14,NULL,'father',NULL),(23,13,14,NULL,'mother',NULL),(24,18,24,NULL,'father',NULL),(25,18,25,NULL,'father',NULL),(26,18,42,NULL,'father',NULL),(27,30,8,NULL,'mother',NULL),(28,31,8,NULL,'father',NULL),(29,34,7,NULL,'father',NULL),(30,35,7,NULL,'mother',NULL),(31,36,10,NULL,'father',NULL),(32,37,10,NULL,'mother',NULL),(33,40,24,NULL,'mother',NULL),(34,40,25,NULL,'mother',NULL),(35,40,42,NULL,'mother',NULL),(36,67,72,NULL,'father',NULL),(37,67,75,NULL,'father',NULL),(38,70,41,NULL,'mother',NULL),(39,71,72,NULL,'mother',NULL),(40,71,75,NULL,'mother',NULL),(41,72,74,NULL,'father',NULL),(42,73,74,NULL,'mother',NULL),(43,36,65,NULL,'father',NULL),(44,37,65,NULL,'mother',NULL),(45,15,82,NULL,'father',NULL),(46,47,82,NULL,'mother',NULL),(47,83,91,NULL,'father',NULL),(48,84,91,NULL,'mother',NULL),(50,97,33,NULL,'father',NULL),(51,98,33,NULL,'mother',NULL),(52,21,100,NULL,'father',NULL),(53,32,100,NULL,'mother',NULL),(54,21,99,NULL,'father',NULL),(55,32,99,NULL,'mother',NULL),(56,21,101,NULL,'father',NULL),(57,32,101,NULL,'mother',NULL),(58,21,102,NULL,'father',NULL),(59,32,102,NULL,'mother',NULL),(60,103,104,NULL,'father',NULL),(61,99,104,NULL,'mother',NULL),(62,103,107,NULL,'father',NULL),(63,99,107,NULL,'mother',NULL),(64,104,106,NULL,'father',NULL),(65,105,106,NULL,'mother',NULL),(66,108,105,NULL,'father',NULL),(67,109,105,NULL,'mother',NULL);
/*!40000 ALTER TABLE `parent_child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parent_child_backup`
--

DROP TABLE IF EXISTS `parent_child_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parent_child_backup` (
  `id` int NOT NULL DEFAULT '0',
  `parent_id` int NOT NULL,
  `child_id` int NOT NULL,
  `type` enum('father','mother') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent_child_backup`
--

LOCK TABLES `parent_child_backup` WRITE;
/*!40000 ALTER TABLE `parent_child_backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `parent_child_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person` (
  `person_id` int NOT NULL AUTO_INCREMENT,
  `lineage_id` int DEFAULT NULL,
  `sur_name` varchar(150) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `gender` enum('male','female','other') NOT NULL DEFAULT 'other',
  `birth_date` date DEFAULT NULL,
  `birth_date_precision` enum('unknown','year','month','exact') DEFAULT 'unknown',
  `death_date` date DEFAULT NULL,
  `death_date_precision` enum('unknown','year','month','exact') DEFAULT 'unknown',
  `asian_birth_date` text,
  `asian_birth_precision` enum('exact','month','year','unknown') NOT NULL DEFAULT 'unknown',
  `asian_death_date` text,
  `asian_death_precision` enum('exact','month','year','unknown') NOT NULL DEFAULT 'unknown',
  `birth_place` varchar(200) DEFAULT NULL,
  `death_place` varchar(200) DEFAULT NULL,
  `grave_info` varchar(255) DEFAULT NULL,
  `anniversary_death` varchar(10) DEFAULT '',
  `nationality` varchar(100) DEFAULT NULL,
  `ethnic_group` varchar(100) DEFAULT NULL,
  `religion` varchar(200) DEFAULT NULL,
  `languages_spoken` json DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(32) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `school_attended` varchar(255) DEFAULT NULL,
  `degree_earned` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL,
  `delete_status` tinyint(1) NOT NULL DEFAULT '0',
  `notes` text,
  `full_name_vn` varchar(350) GENERATED ALWAYS AS (trim(concat_ws(_utf8mb4' ',`last_name`,`middle_name`,`first_name`))) STORED,
  `blood_code` varchar(20) DEFAULT NULL COMMENT 'Mã huyết thống kỹ thuật (cha|mẹ), sinh tự động',
  `role_in_marriage` enum('husband','wife','unknown') DEFAULT 'unknown',
  `avatar_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`person_id`),
  KEY `idx_person_lineage` (`lineage_id`),
  KEY `idx_person_name` (`last_name`,`middle_name`,`first_name`),
  KEY `idx_person_fullname` (`full_name_vn`),
  KEY `idx_person_birth_date` (`birth_date`),
  KEY `idx_person_gender` (`gender`),
  FULLTEXT KEY `ftx_person_names` (`first_name`,`middle_name`,`last_name`,`sur_name`,`notes`),
  CONSTRAINT `fk_person_lineage` FOREIGN KEY (`lineage_id`) REFERENCES `lineage` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` (`person_id`, `lineage_id`, `sur_name`, `last_name`, `middle_name`, `first_name`, `gender`, `birth_date`, `birth_date_precision`, `death_date`, `death_date_precision`, `asian_birth_date`, `asian_birth_precision`, `asian_death_date`, `asian_death_precision`, `birth_place`, `death_place`, `grave_info`, `anniversary_death`, `nationality`, `ethnic_group`, `religion`, `languages_spoken`, `address`, `phone_number`, `email`, `avatar`, `school_attended`, `degree_earned`, `created_at`, `updated_at`, `deleted_at`, `delete_status`, `notes`, `blood_code`, `role_in_marriage`, `avatar_path`) VALUES (4,NULL,'Giuse','Trần','Ngọc','Quí','male','1958-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(5,NULL,'Andre','Trần','Ngọc','Kính','male','1956-05-19','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 12:34:06',NULL,0,NULL,NULL,'unknown',NULL),(7,NULL,'Phanxicô','Trần',NULL,'Tấn','male','1930-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(8,NULL,'Maria','Trần','Thị','Thủy','female','1963-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'8.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 10:26:59',NULL,0,NULL,NULL,'unknown',NULL),(10,NULL,'Maria','Trần','Thị','Lượng','female','1926-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(11,NULL,'Ephrem','Trần','Bửu','Tân','male','1991-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'11.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 15:51:48',NULL,0,NULL,NULL,'unknown',NULL),(12,NULL,'Gioan Maria Vianey','Trần','Bảo','Truyền','male','1996-07-02','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'12.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 12:38:03',NULL,0,NULL,NULL,'unknown',NULL),(13,NULL,'Anna','Phan','Hồng','Nhi','female','1991-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'13.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 15:53:48',NULL,0,NULL,NULL,'unknown',NULL),(14,NULL,'Augustinô','Trần','Quy','Nguyên Khôi','male','2025-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'14.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 15:59:23',NULL,0,NULL,NULL,'unknown',NULL),(15,NULL,'Dominico','Trần','Ngọc','Dũng','male','1964-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(18,NULL,'Giuse','Trần','Ngọc','Chánh','male','1962-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(19,NULL,'Marthia','Trần','Ngọc','Trí','male','1967-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(21,NULL,'Luca','Trần','Ngọc','Tin','male','1953-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(22,NULL,'Anna','Trần','Thị','Minh Tâm','female','1960-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(24,NULL,'Giuse','Trần','Bửu','Văn Bình','male','1990-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(25,NULL,'Elizabeth','Trần','Bửu','Trúc Linh','female','1988-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(30,NULL,'Têrêxa','Nguyễn','Thị','Hà','female','1932-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(31,NULL,'An-tôn','Trần','Tuấn','Mậu','male','1935-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(32,NULL,'Maria','Nguyễn','Thị','Hoa','female','1956-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(33,NULL,'Maria','Đào','Thị','Anh Thư','female','1999-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'33.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-12 10:25:19',NULL,0,NULL,NULL,'unknown',NULL),(34,NULL,NULL,'Trần','Văn','Pháp','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(35,NULL,'Diệu Tích','Nguyễn','Thị','Bốn','female','1902-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(36,NULL,NULL,'Trần',NULL,'Xuyên','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(37,NULL,NULL,'Dương','Thị','Mẹo','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(39,NULL,'Hellen','Trần','Thị','Thu Thủy','female','1969-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(40,NULL,'Têrêxa Maria','Trần','Thị','Diễm Ly','female','1963-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(41,NULL,'','Trần','Ngọc','Thanh Nga','female','1976-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'41.jpg',NULL,NULL,'2026-02-07 13:21:21','2026-03-11 21:58:31',NULL,0,NULL,NULL,'unknown',NULL),(42,NULL,NULL,'Trần','Bửu','Quỳnh Anh','female','1994-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(45,NULL,NULL,'Hồ','Văn','Vui','male','1955-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(47,NULL,'Maria','Nguyễn','Thị','Thanh','female','1965-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(50,NULL,NULL,'Trần',NULL,'Kỳ','male','1957-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(51,NULL,NULL,'Trần',NULL,'Kỷ','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(54,NULL,NULL,'Trần',NULL,'Lực','male','1924-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(55,NULL,NULL,'Trần',NULL,'Lự','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(60,NULL,NULL,'Trần','Thị','Lục','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(63,NULL,NULL,'Trần','Thị','Lục','female','1930-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(64,NULL,NULL,'Trần',NULL,'Lự','male','1928-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(65,NULL,NULL,'Trần','Công','Lựu','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(66,NULL,NULL,'Trần','Thị','Lệ','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(67,NULL,'An-tôn','Trần','Văn','Du','male','1962-03-17','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-03-07 09:36:15',NULL,0,NULL,NULL,'unknown',NULL),(68,NULL,NULL,'t','Văn','Du','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-21 21:26:15','2026-02-21 21:26:15',1,NULL,NULL,'unknown',NULL),(69,NULL,'Maria','Thái','Thị','Tám','female','1978-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(70,NULL,NULL,'Nguyễn','Thanh','Hằng','female','1955-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(71,NULL,'Maria','Cao','Thị','Kim Tuyền','female','1964-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(72,NULL,'Giuse','Trần','Cao','Anh Duy','male','1989-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(73,NULL,NULL,'Phạm','Trang','Anh Thư','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(74,NULL,NULL,'Trần','Thiên','Diệp','male','2017-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(75,NULL,'Giuse','Trần','Cao','Minh Tân','male','1990-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(76,NULL,'Maria','Lê','Thị','Thùy Dương','female','1991-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(77,NULL,'Têrêxa','Trần','Khánh','Vy','female','2020-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(78,NULL,'Anton','Trần','Cao','Quang Lâm','male','2002-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(79,NULL,NULL,'Huỳnh','Văn','Khải','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(80,NULL,NULL,'Huỳnh','Ngọc','Vân Nhi','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(81,NULL,NULL,'Huỳnh','Ngọc','Vân Thiên','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(82,NULL,'Maria','Trần','Bửu','Hiền Hòa','female','2005-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-22 09:30:06',NULL,0,NULL,NULL,'unknown',NULL),(83,NULL,NULL,'Nguyễn','Kiến','Thơ','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(84,NULL,NULL,'Bùi','Thị','Ánh Tuyết','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(85,NULL,NULL,'Trần',NULL,'Lự','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-07 13:21:21','2026-02-07 13:21:21',NULL,0,NULL,NULL,'unknown',NULL),(86,NULL,'','Nguyễn','Tường','Mai','male','1908-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-01 06:03:24','2026-03-01 06:03:24',NULL,0,NULL,NULL,'unknown',NULL),(87,NULL,'','Nguyễn','Tường','Ninh','male','1930-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-01 14:30:43','2026-03-02 08:32:07',NULL,0,NULL,'0|86','unknown',NULL),(88,NULL,'Test','Nguyen','Van','Demo','male','1995-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-01 16:08:38','2026-03-01 18:16:48',NULL,0,NULL,NULL,'unknown',NULL),(89,NULL,'','Nguyễn','Tường','Mạnh','male','1951-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-01 18:52:23','2026-03-01 18:52:23',NULL,0,NULL,NULL,'unknown',NULL),(90,NULL,'','Lương','Thị','Ngọc Lạng','female','1954-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-01 18:53:50','2026-03-01 18:53:50',NULL,0,NULL,NULL,'unknown',NULL),(91,NULL,'','Nguyễn','Kiến','Thức','male','2006-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-02 07:30:35','2026-03-02 08:29:28',NULL,0,NULL,'83|84','unknown',NULL),(92,NULL,'An-tôn ','Trần','Văn','Diền','male','1965-06-06','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-02 21:50:05','2026-03-02 21:50:05',NULL,0,NULL,NULL,'unknown',NULL),(93,NULL,'Anna','Nguyễn','Thị','Cúc','female','1968-04-16','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-02 21:51:17','2026-03-02 21:51:17',NULL,0,NULL,NULL,'unknown',NULL),(94,NULL,'An-tôn','Trần','Nguyễn','Hoàng Dinh','male','1990-12-25','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'94_cb50ab67.png',NULL,NULL,'2026-03-04 10:28:37','2026-03-09 04:46:12',NULL,0,NULL,NULL,'unknown',NULL),(95,NULL,'Maria','Nguyễn','Thị','Huyền Trân','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-05 14:08:50','2026-03-09 04:51:46',NULL,0,NULL,NULL,'unknown',NULL),(96,NULL,'An-tôn ','Trần','Nguyễn','Đăng Khoa','male','2024-10-17','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-05 14:09:53','2026-03-09 04:41:46',NULL,0,NULL,NULL,'unknown',NULL),(97,NULL,'','Đào','Văn','Thành','male','1979-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'97.jpg',NULL,NULL,'2026-03-12 11:57:00','2026-03-12 12:19:14',NULL,0,NULL,NULL,'unknown',NULL),(98,NULL,'','Nguyễn','Thị','Hiền','female','1981-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'98.jpg',NULL,NULL,'2026-03-12 11:57:59','2026-03-12 12:20:55',NULL,0,NULL,NULL,'unknown',NULL),(99,NULL,'','Trần','Bửu','Hoàng Thư','female','1978-06-16','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'99.jpg',NULL,NULL,'2026-03-12 21:10:22','2026-03-12 21:21:47',NULL,0,NULL,NULL,'unknown',NULL),(100,NULL,'','Trần','Bửu','Hoài Nhân','male','1976-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-12 21:11:23','2026-03-12 21:11:23',NULL,0,NULL,NULL,'unknown',NULL),(101,NULL,'','Trần','Bửu','Hoài Nghĩa','male','1982-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-12 21:12:25','2026-03-12 21:12:25',NULL,0,NULL,NULL,'unknown',NULL),(102,NULL,'','Trần','Bửu','Hoài Phúc','male','1986-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-12 21:13:18','2026-03-12 21:13:18',NULL,0,NULL,NULL,'unknown',NULL),(103,NULL,'','Huỳnh','Quốc','Nhật','male','1977-02-02','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'103.jpg',NULL,NULL,'2026-03-12 21:14:40','2026-03-12 21:20:44',NULL,0,NULL,NULL,'unknown',NULL),(104,NULL,'','Huỳnh','Trần','Quốc Vỹ','male','1999-11-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'104.jpg',NULL,NULL,'2026-03-12 21:15:59','2026-03-12 21:23:50',NULL,0,NULL,NULL,'unknown',NULL),(105,NULL,'','Nguyễn','Thị','Phương','female','2000-11-24','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'105.jpg',NULL,NULL,'2026-03-12 21:17:01','2026-03-12 21:25:32',NULL,0,NULL,NULL,'unknown',NULL),(106,NULL,'','Huỳnh','Ngọc','Thiên An','male','2024-11-24','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-12 21:18:28','2026-03-12 21:18:28',NULL,0,NULL,NULL,'unknown',NULL),(107,NULL,'','Huỳnh','Trần','Nhật Vỹ','male','1999-11-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-12 21:19:23','2026-03-12 21:19:23',NULL,0,NULL,NULL,'unknown',NULL),(108,NULL,'','Nguyễn','','BaPhg','male','1980-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'108.jpg',NULL,NULL,'2026-03-12 21:27:16','2026-03-12 21:29:03',NULL,0,NULL,NULL,'unknown',NULL),(109,NULL,'','Ng','','MePhg','female','1980-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'109.jpg',NULL,NULL,'2026-03-12 21:28:00','2026-03-12 21:30:31',NULL,0,NULL,NULL,'unknown',NULL),(110,NULL,'','Trần','Thị','Minh','female','1963-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-18 11:00:24','2026-03-18 11:00:24',NULL,0,NULL,NULL,'unknown',NULL),(111,NULL,'','Trần','Văn','Hào','male','1965-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-18 11:01:05','2026-03-18 11:01:05',NULL,0,NULL,NULL,'unknown',NULL),(112,NULL,'','Trần','Văn','Hải','male','1967-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-18 11:01:42','2026-03-18 11:01:42',NULL,0,NULL,NULL,'unknown',NULL),(113,NULL,'','Trần','Thị','Trâm','female','1969-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-18 11:02:30','2026-03-18 11:02:30',NULL,0,NULL,NULL,'unknown',NULL),(114,NULL,'','Trần','Thị','Thu','female','1971-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-18 11:03:05','2026-03-18 11:03:05',NULL,0,NULL,NULL,'unknown',NULL),(115,NULL,'','Trần','Thị','Duyên','female','1973-01-01','unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-18 11:03:37','2026-03-18 11:03:37',NULL,0,NULL,NULL,'unknown',NULL);
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_gene_backup`
--

DROP TABLE IF EXISTS `person_gene_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person_gene_backup` (
  `backup_id` int NOT NULL AUTO_INCREMENT,
  `person_id` int DEFAULT NULL,
  `blood_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `backup_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`backup_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_gene_backup`
--

LOCK TABLES `person_gene_backup` WRITE;
/*!40000 ALTER TABLE `person_gene_backup` DISABLE KEYS */;
INSERT INTO `person_gene_backup` VALUES (51,115,'0|0','2026-02-28 14:04:23'),(52,91,'83|0','2026-03-02 08:28:33'),(53,91,'83|84','2026-03-02 08:29:28'),(54,87,'0|86','2026-03-02 08:32:07');
/*!40000 ALTER TABLE `person_gene_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_pending`
--

DROP TABLE IF EXISTS `person_pending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person_pending` (
  `pending_id` int NOT NULL AUTO_INCREMENT,
  `submitter_id` int NOT NULL,
  `sur_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `middle_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `first_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` enum('male','female','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth_date` date DEFAULT NULL,
  `death_date` date DEFAULT NULL,
  `asian_birth_date` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Trùng họ, tên và giới tính',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'waiting',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `approved` tinyint DEFAULT '0',
  `approved_by` int DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `approved_person_id` int DEFAULT NULL,
  `approved_date` datetime DEFAULT NULL,
  PRIMARY KEY (`pending_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_pending`
--

LOCK TABLES `person_pending` WRITE;
/*!40000 ALTER TABLE `person_pending` DISABLE KEYS */;
/*!40000 ALTER TABLE `person_pending` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_account`
--

DROP TABLE IF EXISTS `user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_account` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `person_id` int DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('viewer','member_basic','member_close','co_operator','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'viewer',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `last_login` datetime DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_user_person` (`person_id`),
  CONSTRAINT `fk_user_person` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_account`
--

LOCK TABLES `user_account` WRITE;
/*!40000 ALTER TABLE `user_account` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_log`
--

DROP TABLE IF EXISTS `user_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `target_id` int DEFAULT NULL,
  `target_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_log`
--

LOCK TABLES `user_log` WRITE;
/*!40000 ALTER TABLE `user_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `marriage_pair`
--

/*!50001 DROP VIEW IF EXISTS `marriage_pair`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `marriage_pair` AS select `marriage`.`id` AS `id`,least(`marriage`.`spouse_a_id`,`marriage`.`spouse_b_id`) AS `a`,greatest(`marriage`.`spouse_a_id`,`marriage`.`spouse_b_id`) AS `b`,`marriage`.`start_date` AS `start_date`,`marriage`.`end_date` AS `end_date`,`marriage`.`status` AS `status`,`marriage`.`ceremony_type` AS `ceremony_type`,`marriage`.`location` AS `location`,`marriage`.`notes` AS `notes` from `marriage` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-20  8:27:33

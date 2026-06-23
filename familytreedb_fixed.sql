-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: familytreedb
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `event_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `calendar_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `solar_date` date DEFAULT NULL,
  `lunar_day` int DEFAULT NULL,
  `lunar_month` int DEFAULT NULL,
  `lunar_year` int DEFAULT NULL,
  `repeat_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'yearly',
  `person_id` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (5,'Thông báo mời họp','Mời các thành viên chúng ta họp vào ngày thuận lợi','custom','solar',NULL,NULL,NULL,NULL,'none',NULL,1,'2026-06-12 13:32:46','2026-06-12 14:27:11'),(6,'Test CRUD','Test CRUD Announcement','custom','solar',NULL,NULL,NULL,NULL,'none',NULL,1,'2026-06-12 13:58:53','2026-06-12 13:58:53');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'new',
  `admin_note` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (2,NULL,'bug','Avatar','Không sửa được hình','','0900000000','new',NULL,'2026-05-28 23:40:35','2026-05-28 23:40:35'),(3,NULL,'bug','Avatar','Không chỉnh sửa được hình','','090000000','resolved','Đã ghi nhận lỗi avatar, sẽ kiểm tra phần upload/chỉnh sửa hình.','2026-05-28 23:43:10','2026-05-29 01:03:09'),(4,NULL,'feature','Tắt saved info','Tắt các saved info khi mở form điền thông tin','trangocking1956@gmail.com','0903108696','reviewing',NULL,'2026-06-13 00:09:43','2026-06-13 00:11:18'),(5,NULL,'bug','Test Feedback CRUD','Đây là feedback kiểm thử chức năng Feedback CRUD.','test@example.com','','resolved','Đã xử lý hoàn tất.\nFeedback #2\nPopup: Đã cập nhật feedback. đang dùng alert(). Sau deploy có thể đổi sang: Toast xanh góc phải cho hiện đại hơn.','2026-06-13 02:24:47','2026-06-13 02:34:03'),(6,NULL,'feature','Hôn nhân','Backlog:\n- Cảnh báo mềm tuổi hiện tại < 18\n- Không kiểm tra nếu thiếu năm sinh\n- Vẫn cho phép lưu nếu người dùng xác nhận','test@example.com','','new',NULL,'2026-06-13 07:00:48','2026-06-13 07:00:48'),(7,NULL,'feature','Thêm chú thích giải nghĩa loaih phản hồi','| Loại phản hồi              | Khi nào nên chọn                                                                                                     |\n| -------------------------- | -------------------------------------------------------------------------------------------------------------------- |\n| 🐞 Báo lỗi hệ thống        | Chức năng hoạt động sai, xuất hiện lỗi.                                                                              |\n| 💡 Góp ý cải tiến          | Đề xuất tính năng hoặc cải thiện giao diện.                                                                          |\n| 🌳 Báo sai dữ liệu gia phả | Sai quan hệ, ngày sinh, ngày mất, thông tin thành viên.                                                              |\n| 👤 Hỗ trợ tài khoản        | Quên mật khẩu, đổi email, đổi tên đăng nhập, tài khoản bị khóa, không đăng nhập được, xin nâng quyền hoặc cấp quyền. |\n| ❓ Khác                     | Những vấn đề chưa thuộc các nhóm trên.                                                                               |\n','','0900000000','resolved','đang kiểm tra, chuyển admin góp ý','2026-06-21 14:27:41','2026-06-22 02:27:20');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marriages`
--

DROP TABLE IF EXISTS `marriages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marriages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `spouse_a_id` int NOT NULL,
  `spouse_b_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('married','separated','divorced','widowed','cohabiting') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ceremony_type` enum('civil','religious','customary') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `consanguineous` tinyint(1) DEFAULT '0',
  `ended_by` enum('divorced','death','annulment') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status_changed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `priority` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `spouse_a_id` (`spouse_a_id`),
  KEY `spouse_b_id` (`spouse_b_id`),
  CONSTRAINT `marriages_ibfk_1` FOREIGN KEY (`spouse_a_id`) REFERENCES `persons` (`person_id`),
  CONSTRAINT `marriages_ibfk_2` FOREIGN KEY (`spouse_b_id`) REFERENCES `persons` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marriages`
--

LOCK TABLES `marriages` WRITE;
/*!40000 ALTER TABLE `marriages` DISABLE KEYS */;
INSERT INTO `marriages` VALUES (1,1,2,'1990-11-03',NULL,'married',NULL,'',NULL,0,NULL,'2026-05-10 04:20:28','2026-04-26 19:36:34',3),(2,3,4,NULL,NULL,'married',NULL,NULL,'Test JWT guard update marriage',0,NULL,NULL,'2026-04-29 12:36:26',0),(3,5,6,NULL,NULL,'married',NULL,'','Nhà thờ Pleiku',0,NULL,'2026-06-20 03:56:11','2026-04-29 14:24:28',0),(4,8,10,'2019-11-02',NULL,'married',NULL,'','',0,NULL,'2026-05-24 08:02:31','2026-05-05 05:33:28',0),(5,9,11,'2025-12-07',NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-05 05:35:09',0),(6,13,14,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-05 08:35:17',0),(7,15,16,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-05 08:35:50',0),(9,21,26,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-05 15:40:55',0),(10,1,29,'1975-05-31','2026-05-07','separated',NULL,'','',0,NULL,'2026-05-28 04:18:38','2026-05-06 04:45:35',2),(12,42,19,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-17 07:39:26',0),(13,44,45,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-17 12:46:26',0),(14,40,46,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-19 07:00:07',0),(15,17,47,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-05-19 07:03:01',0),(17,30,33,NULL,NULL,'divorced',NULL,NULL,NULL,0,NULL,NULL,'2026-05-20 23:44:17',0),(18,49,48,'1999-08-20',NULL,'married',NULL,'','',0,NULL,'2026-06-19 03:05:36','2026-05-22 01:04:29',0),(21,50,61,'2024-07-07',NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-05 02:42:33',0),(22,63,64,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-05 02:53:28',0),(23,69,70,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-06 03:33:35',2),(24,69,72,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-06 06:04:53',1),(25,78,43,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-07 10:23:19',0),(26,81,41,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-08 03:50:51',0),(27,73,85,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-08 16:13:54',0),(28,75,74,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-08 16:34:38',0),(34,22,23,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-20 05:15:17',0),(35,20,97,NULL,NULL,'married',NULL,NULL,NULL,0,NULL,NULL,'2026-06-20 12:14:15',0);
/*!40000 ALTER TABLE `marriages` ENABLE KEYS */;
UNLOCK TABLES;

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
  `type` enum('father','mother') COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  KEY `child_id` (`child_id`),
  KEY `marriage_id` (`marriage_id`),
  CONSTRAINT `parent_child_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `persons` (`person_id`),
  CONSTRAINT `parent_child_ibfk_2` FOREIGN KEY (`child_id`) REFERENCES `persons` (`person_id`),
  CONSTRAINT `parent_child_ibfk_3` FOREIGN KEY (`marriage_id`) REFERENCES `marriages` (`id`),
  CONSTRAINT `chk_parent_type` CHECK ((`type` in (_utf8mb4'father',_utf8mb4'mother')))
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent_child`
--

LOCK TABLES `parent_child` WRITE;
/*!40000 ALTER TABLE `parent_child` DISABLE KEYS */;
INSERT INTO `parent_child` VALUES (5,5,2,NULL,'father',NULL),(6,6,2,NULL,'mother',NULL),(7,3,1,NULL,'father',NULL),(8,4,1,NULL,'mother',NULL),(9,1,8,NULL,'father',NULL),(10,2,8,NULL,'mother',NULL),(11,1,9,NULL,'father',NULL),(12,2,9,NULL,'mother',NULL),(13,8,12,NULL,'father',NULL),(14,10,12,NULL,'mother',NULL),(15,13,3,NULL,'father',NULL),(16,14,3,NULL,'mother',NULL),(17,15,4,NULL,'father',NULL),(18,16,4,NULL,'mother',NULL),(19,3,22,NULL,'father',NULL),(20,4,22,NULL,'mother',NULL),(21,3,21,NULL,'father',NULL),(22,4,21,NULL,'mother',NULL),(23,3,20,NULL,'father',NULL),(24,4,20,NULL,'mother',NULL),(25,3,19,NULL,'father',NULL),(26,4,19,NULL,'mother',NULL),(27,22,24,NULL,'father',NULL),(28,23,24,NULL,'mother',NULL),(29,21,27,NULL,'father',NULL),(30,26,27,NULL,'mother',NULL),(31,22,25,NULL,'father',NULL),(32,23,25,NULL,'mother',NULL),(33,3,17,NULL,'father',NULL),(34,4,17,NULL,'mother',NULL),(35,3,18,NULL,'father',NULL),(36,4,18,NULL,'mother',NULL),(37,1,33,NULL,'father',NULL),(38,29,33,NULL,'mother',NULL),(39,17,28,NULL,'father',NULL),(40,5,40,NULL,'father',NULL),(41,6,40,NULL,'mother',NULL),(42,5,41,NULL,'father',NULL),(43,6,41,NULL,'mother',NULL),(44,5,43,NULL,'father',NULL),(45,6,43,NULL,'mother',NULL),(46,5,45,NULL,'father',NULL),(47,6,45,NULL,'mother',NULL),(55,30,31,NULL,'father',NULL),(56,33,31,NULL,'mother',NULL),(57,30,32,NULL,'father',NULL),(58,33,32,NULL,'mother',NULL),(59,49,50,NULL,'father',NULL),(60,48,50,NULL,'mother',NULL),(61,49,51,NULL,'father',NULL),(62,48,51,NULL,'mother',NULL),(63,17,52,NULL,'father',NULL),(64,47,52,NULL,'mother',NULL),(65,17,53,NULL,'father',NULL),(66,47,53,NULL,'mother',NULL),(67,47,28,NULL,'mother',NULL),(68,17,48,NULL,'father',NULL),(69,47,48,NULL,'mother',NULL),(72,63,5,NULL,'father',NULL),(73,64,5,NULL,'mother',NULL),(74,63,65,NULL,'father',NULL),(75,64,65,NULL,'mother',NULL),(76,63,66,NULL,'father',NULL),(77,63,67,NULL,'father',NULL),(78,64,67,NULL,'mother',NULL),(79,63,68,NULL,'father',NULL),(80,64,68,NULL,'mother',NULL),(81,64,66,NULL,'mother',NULL),(82,69,71,NULL,'father',NULL),(83,69,6,NULL,'father',NULL),(84,70,71,NULL,'mother',NULL),(85,70,6,NULL,'mother',NULL),(86,44,60,NULL,'father',NULL),(87,45,60,NULL,'mother',NULL),(88,44,58,NULL,'father',NULL),(89,45,58,NULL,'mother',NULL),(90,5,73,NULL,'father',NULL),(91,6,73,NULL,'mother',NULL),(92,5,74,NULL,'father',NULL),(93,6,74,NULL,'mother',NULL),(94,43,76,NULL,'mother',NULL),(95,78,76,NULL,'father',NULL),(96,78,77,NULL,'father',NULL),(97,43,77,NULL,'mother',NULL),(98,40,79,NULL,'father',NULL),(99,46,79,NULL,'mother',NULL),(100,40,80,NULL,'father',NULL),(101,46,80,NULL,'mother',NULL),(102,81,82,NULL,'father',NULL),(103,41,82,NULL,'mother',NULL),(104,81,84,NULL,'father',NULL),(105,41,84,NULL,'mother',NULL),(106,81,83,NULL,'father',NULL),(107,41,83,NULL,'mother',NULL),(108,73,86,NULL,'father',NULL),(109,85,86,NULL,'mother',NULL),(110,44,59,NULL,'father',NULL),(111,45,59,NULL,'mother',NULL),(112,18,104,NULL,'father',NULL),(113,101,103,NULL,'father',NULL),(114,102,103,NULL,'mother',NULL),(115,96,105,NULL,'mother',NULL),(116,18,105,NULL,'father',NULL),(117,96,104,NULL,'mother',NULL),(118,75,87,NULL,'father',NULL),(119,74,87,NULL,'mother',NULL),(120,75,88,NULL,'father',NULL),(121,74,88,NULL,'mother',NULL),(148,54,106,NULL,'father',NULL),(149,55,106,NULL,'mother',NULL),(150,54,57,NULL,'father',NULL),(151,54,107,NULL,'father',NULL),(152,55,107,NULL,'mother',NULL),(153,54,56,NULL,'father',NULL),(154,55,56,NULL,'mother',NULL),(155,55,57,NULL,'mother',NULL),(156,69,89,NULL,'father',NULL),(157,72,108,NULL,'mother',NULL),(158,20,98,NULL,'father',NULL),(159,97,98,NULL,'mother',NULL),(160,20,100,NULL,'father',NULL),(161,97,100,NULL,'mother',NULL),(162,72,89,NULL,'mother',NULL),(163,69,108,NULL,'father',NULL);
/*!40000 ALTER TABLE `parent_child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_marriage_priority`
--

DROP TABLE IF EXISTS `person_marriage_priority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person_marriage_priority` (
  `id` int NOT NULL AUTO_INCREMENT,
  `person_id` int NOT NULL,
  `marriage_id` int NOT NULL,
  `priority` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_person_marriage` (`person_id`,`marriage_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_marriage_priority`
--

LOCK TABLES `person_marriage_priority` WRITE;
/*!40000 ALTER TABLE `person_marriage_priority` DISABLE KEYS */;
INSERT INTO `person_marriage_priority` VALUES (12,5,3,0,'2026-05-09 16:38:21'),(14,1,10,1,'2026-05-10 01:26:13');
/*!40000 ALTER TABLE `person_marriage_priority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persons`
--

DROP TABLE IF EXISTS `persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persons` (
  `person_id` int NOT NULL AUTO_INCREMENT,
  `lineage_id` int DEFAULT NULL,
  `sur_name` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `middle_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` enum('male','female','other') COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth_date` date DEFAULT NULL,
  `birth_date_precision` enum('unknown','year','month','exact') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `death_date` date DEFAULT NULL,
  `death_date_precision` enum('unknown','year','month','exact') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `asian_birth_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `asian_birth_precision` enum('exact','month','year','unknown') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `asian_death_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `asian_death_precision` enum('exact','month','year','unknown') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_place` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `death_place` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `grave_info` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anniversary_death` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anniversary_type` enum('lunar','solar') COLLATE utf8mb4_unicode_ci DEFAULT 'lunar',
  `nationality` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ethnic_group` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `religion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `languages_spoken` json DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_number` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `school_attended` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `degree_earned` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `blood_code` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role_in_marriage` enum('husband','wife','unknown') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `delete_status` tinyint(1) DEFAULT '0',
  `full_name_vn` varchar(350) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_order` int DEFAULT NULL,
  PRIMARY KEY (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persons`
--

LOCK TABLES `persons` WRITE;
/*!40000 ALTER TABLE `persons` DISABLE KEYS */;
INSERT INTO `persons` VALUES (1,NULL,'Andre','Trần','Ngọc','Kính','male','1956-05-19','exact',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'1.jpg',NULL,NULL,NULL,NULL,'3|4',NULL,'2026-04-25 20:48:56','2026-05-01 15:57:23',NULL,0,NULL,NULL),(2,NULL,'Maria','Trần','Thị','Thủy','female','1963-09-10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2.jpg',NULL,NULL,NULL,NULL,'5|6',NULL,'2026-04-26 19:22:03','2026-05-02 04:25:22',NULL,0,NULL,2),(3,NULL,'Phanxicô Xaviê','Trần','','Tấn','male','1930-01-01','year','2013-08-18','exact',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'3.jpg',NULL,NULL,NULL,NULL,'13|14','unknown','2026-04-27 13:55:11','2026-05-05 18:41:08',NULL,0,NULL,NULL),(4,NULL,'Maria','Trần','Thị','Lượng','female','1926-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'4.jpg',NULL,NULL,NULL,NULL,'15|16','unknown','2026-04-28 02:10:26','2026-05-02 04:18:48',NULL,0,NULL,NULL),(5,NULL,'An-tôn ','Trần','Tuấn','Mậu','male','1935-01-01','year','1974-12-25','exact',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'5.jpg',NULL,NULL,NULL,NULL,'63|64','unknown','2026-04-29 14:22:33','2026-05-01 15:37:24',NULL,0,NULL,3),(6,NULL,'Têrêxa','Nguyễn','Thị','Thái Hà','female','1932-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'69|70','unknown','2026-04-29 14:23:44','2026-04-29 14:23:44',NULL,0,NULL,2),(8,NULL,'Ephrem','Trần','Bửu','Tân','male','1991-06-09','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'8.jpg',NULL,NULL,NULL,NULL,'1|2','unknown','2026-05-02 06:47:22','2026-05-02 14:10:04',NULL,0,NULL,NULL),(9,NULL,'Gioan Maria Vianey','Trần','Bảo','Truyền','male','1996-07-02','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'9.jpg',NULL,NULL,NULL,NULL,'1|2','unknown','2026-05-02 07:11:56','2026-05-02 14:12:47',NULL,0,NULL,NULL),(10,NULL,'Anna','Phạm','Hồng','Nhi','female','1991-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'10.jpg',NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-03 14:36:33','2026-05-04 05:58:59',NULL,0,NULL,NULL),(11,NULL,'Maria','Đào','Thị','Anh Thư','female','1999-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'11.jpg',NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-04 14:14:18','2026-05-04 21:41:05',NULL,0,NULL,NULL),(12,NULL,'Augustinô','Trần','Quy ','Nguyên Khôi','male','2026-04-12','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'12.jpg',NULL,NULL,NULL,NULL,'8|10','unknown','2026-05-05 01:40:00','2026-05-05 08:41:01',NULL,0,NULL,NULL),(13,NULL,'','Trần','Văn','Pháp','male',NULL,'unknown',NULL,'unknown','','unknown','','unknown','','','','31/05','solar','','','','\"\"','','','','13.jpg',NULL,'','','','','unknown','2026-05-05 08:16:23','2026-05-05 19:13:39',NULL,0,'',NULL),(14,NULL,'Diệu Tích','Nguyễn','Thị','Bốn','female','1892-01-01','year','1981-12-29','exact','','unknown','','unknown','','','','17/04','lunar','','','','\"\"','','','',NULL,NULL,'','','Ngày đám giỗ là số liệu giả để test.','','unknown','2026-05-05 08:29:46','2026-05-05 08:29:46',NULL,0,'',NULL),(15,NULL,'Phanxicô Xaviê','Trần','','Xuyên','male',NULL,'unknown','1963-05-27','exact',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'11/04','lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-05 08:30:53','2026-05-05 08:30:53',NULL,0,NULL,NULL),(16,NULL,'Anna','Dương','Thị','Mẹo','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,'28/05','solar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-05 08:32:07','2026-05-05 08:32:07',NULL,0,NULL,NULL),(17,NULL,'Luca','Trần','Ngọc','Tin','male','1953-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3|4','unknown','2026-05-05 12:14:41','2026-05-05 12:14:41',NULL,0,NULL,NULL),(18,NULL,'Giuse','Trần','Ngọc','Quí','male','1958-05-31','exact',NULL,'unknown','','unknown','','unknown','','','',NULL,'lunar','','','','\"\"','','','',NULL,NULL,'','','Dữ liệu ngày sinh giả lập để test. Cần phải sửa lại theo dữ liệu thật','','unknown','2026-05-05 12:15:47','2026-05-05 12:15:47',NULL,0,'',NULL),(19,NULL,'Anna','Trần','Thị','Minh Tâm','female','1960-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3|4','unknown','2026-05-05 12:29:46','2026-05-05 12:29:46',NULL,0,NULL,NULL),(20,NULL,'Giuse','Trần','Ngọc','Chánh','male','1962-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3|4','unknown','2026-05-05 12:30:37','2026-05-05 12:30:37',NULL,0,NULL,NULL),(21,NULL,'Dominico','Trần','Ngọc','Dũng','male','1964-09-09','exact','2006-05-14','exact',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3|4','unknown','2026-05-05 14:11:43','2026-05-05 14:11:43',NULL,0,NULL,NULL),(22,NULL,'Matthia','Trần','Ngọc','Trí','male','1967-03-21','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'22.jpg',NULL,NULL,NULL,NULL,'3|4','unknown','2026-05-05 14:13:50','2026-06-04 12:10:08',NULL,0,NULL,NULL),(23,NULL,'Maria','Thái','Thị','Tám','female','1978-12-10','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'23.jpg',NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-05 14:14:54','2026-06-04 12:11:35',NULL,0,NULL,NULL),(24,NULL,'Matthia','Trần','Bửu','Trọng Tín','male','2002-10-08','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'24.jpg',NULL,NULL,NULL,NULL,'22|23','unknown','2026-05-05 14:17:01','2026-06-04 12:12:48',NULL,0,NULL,NULL),(25,NULL,'Matthia','Trần','Bửu','Thành Tín','male','2009-02-27','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'25.jpg',NULL,NULL,NULL,NULL,'22|23','unknown','2026-05-05 14:18:01','2026-06-04 12:13:57',NULL,0,NULL,NULL),(26,NULL,'Maria','Nguyễn','Thị','Thanh','female','1965-08-10','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-05 15:40:17','2026-05-05 15:40:17',NULL,0,NULL,NULL),(27,NULL,'Maria','Trần','Bửu','Hiền Hòa','female','2005-07-23','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'21|26','unknown','2026-05-05 15:43:27','2026-05-05 15:43:27',NULL,0,NULL,NULL),(28,NULL,'','Trần','Bửu','Hoài Nhân','male','1976-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'17|47','unknown','2026-05-06 02:31:29','2026-05-06 02:31:29',NULL,0,NULL,1),(29,NULL,'','Nguyễn','Thanh','Hằng','female','1955-05-20','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'29.jpg',NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-06 02:40:23','2026-06-04 18:22:25',NULL,0,NULL,NULL),(30,NULL,'','Huỳnh','Văn','Khải','male','1976-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-06 04:43:31','2026-05-06 04:43:31',NULL,0,NULL,NULL),(31,NULL,'','Huỳnh','Ngọc','Vân Nhi','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'31.jpg',NULL,NULL,NULL,NULL,'30|33','unknown','2026-05-06 04:44:04','2026-06-04 12:08:14',NULL,0,NULL,1),(32,NULL,'','Huỳnh','Ngọc','Vân Thiên','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'32.jpg',NULL,NULL,NULL,NULL,'30|33','unknown','2026-05-06 04:44:39','2026-06-04 12:09:03',NULL,0,NULL,2),(33,NULL,'','Trần','Ngọc','Thanh Nga','female','1976-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'33.jpg',NULL,NULL,NULL,NULL,'1|29','unknown','2026-05-06 04:46:40','2026-06-04 12:07:09',NULL,0,NULL,NULL),(40,NULL,'','Trần','Văn','Hào','male','1965-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5|6','unknown','2026-05-12 10:45:03','2026-05-12 10:45:03',NULL,0,NULL,3),(41,NULL,'','Trần','Thị','Mỹ Duyên','female','1972-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5|6','unknown','2026-05-12 10:45:54','2026-05-12 10:45:54',NULL,0,NULL,7),(42,NULL,'','Hồ','Văn','Vui','male','1955-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-17 07:38:20','2026-05-17 07:38:20',NULL,0,NULL,NULL),(43,NULL,'','Trần','Thị','Minh','female','1963-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5|6','unknown','2026-05-17 12:41:16','2026-05-17 12:41:16',NULL,0,NULL,1),(44,NULL,'','Đỗ','','An','male','1969-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-17 12:44:20','2026-05-17 12:44:20',NULL,0,NULL,NULL),(45,NULL,'','Trần','Thị','Trâm','female','1969-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5|6','unknown','2026-05-17 12:45:53','2026-05-17 12:45:53',NULL,0,NULL,5),(46,NULL,'','Dương','Thị','Như Nguyện','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-19 06:59:32','2026-05-19 06:59:32',NULL,0,NULL,NULL),(47,NULL,'','Nguyễn','Thị','Hoa','female','1956-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-19 07:02:40','2026-05-19 07:02:40',NULL,0,NULL,NULL),(48,NULL,'','Trần','Bửu','Hoàng Thư','female','1978-06-16','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'48.jpg',NULL,NULL,NULL,NULL,'17|47','unknown','2026-05-22 01:01:18','2026-06-05 08:09:21',NULL,0,NULL,2),(49,NULL,'','Huỳnh','Quốc','Nhật','male','1977-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'49.jpg',NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-22 01:02:08','2026-06-05 08:11:36',NULL,0,NULL,NULL),(50,NULL,'','Huỳnh ','Trần','Quốc Vỹ','male','1999-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,'50.jpg',NULL,NULL,NULL,NULL,'49|48','unknown','2026-05-22 01:03:03','2026-06-05 08:15:27',NULL,0,NULL,1),(51,NULL,'','Huỳnh','Trần','Nhật Vỹ','male','1999-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'49|48','unknown','2026-05-22 01:03:50','2026-05-22 01:03:50',NULL,0,NULL,2),(52,NULL,'','Trần','Bửu','Hoài Nghĩa','male','1982-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'17|47','unknown','2026-05-22 01:29:59','2026-05-22 01:29:59',NULL,0,NULL,3),(53,NULL,'','Trần','Bửu','Hoàng Phúc','male','1986-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,'lunar',NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'17|47','unknown','2026-05-22 01:30:39','2026-05-22 01:30:39',NULL,0,NULL,4),(54,NULL,'','Test','','Chồng','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-30 10:05:00','2026-05-30 10:05:00',NULL,0,NULL,NULL),(55,NULL,'','Test','','Vợ','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-05-30 10:05:28','2026-05-30 10:05:28',NULL,0,NULL,NULL),(56,NULL,'','Test','','Con 1','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'54|55','unknown','2026-05-30 23:58:47','2026-05-30 23:58:47',NULL,0,NULL,3),(57,NULL,'','Test','','Con 2','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'54|55','unknown','2026-05-30 23:59:16','2026-05-30 23:59:16',NULL,0,NULL,4),(58,NULL,'','Đỗ ','Minh','Hoàng','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'44|45','unknown','2026-06-01 04:16:37','2026-06-01 04:16:37',NULL,0,NULL,2),(59,NULL,'','Đỗ','Trần','Minh Hằng','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'44|45','unknown','2026-06-01 04:18:20','2026-06-01 04:18:20',NULL,0,NULL,3),(60,NULL,'','Đỗ','Minh','Huy','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'44|45','unknown','2026-06-01 04:19:26','2026-06-01 04:19:26',NULL,0,NULL,1),(61,NULL,'','Nguyễn','Thị','Phương','female','2000-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,'61.jpg',NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-05 01:18:36','2026-06-05 08:20:15',NULL,0,NULL,NULL),(62,NULL,'','Huỳnh','Ngọc','Thiên An','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-05 01:21:08','2026-06-05 01:21:08',NULL,0,NULL,NULL),(63,NULL,'','Trần','Văn','Tú','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-05 02:48:10','2026-06-05 02:48:10',NULL,0,NULL,NULL),(64,NULL,'','Trần ','Thị','Tròn','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-05 02:48:59','2026-06-05 02:48:59',NULL,0,NULL,NULL),(65,NULL,'','Trần','Thị','Sa','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'63|64','unknown','2026-06-05 02:59:00','2026-06-05 02:59:00',NULL,0,NULL,1),(66,NULL,'','Trần','Văn','Tuy','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'63|64','unknown','2026-06-05 02:59:37','2026-06-05 02:59:37',NULL,0,NULL,2),(67,NULL,'An-tôn','Trần','Văn','Bỗng','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'63|64','unknown','2026-06-05 08:23:23','2026-06-05 08:23:23',NULL,0,NULL,4),(68,NULL,'','Trần','Văn','Giác','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'63|64','unknown','2026-06-05 09:53:43','2026-06-05 09:53:43',NULL,0,NULL,5),(69,NULL,'','Nguyễn ','Tường','Mai','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-05 12:21:35','2026-06-05 12:21:35',NULL,0,NULL,NULL),(70,NULL,'','Nguyễn','Thị','Liễu','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-05 12:22:11','2026-06-05 12:22:11',NULL,0,NULL,NULL),(71,NULL,'','Nguyễn','Tường','Ninh','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'69|70','unknown','2026-06-05 12:23:33','2026-06-05 12:23:33',NULL,0,NULL,1),(72,NULL,'','Nguyễn','Thị','Bốn','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-06 04:33:10','2026-06-06 04:33:10',NULL,0,NULL,NULL),(73,NULL,'','Trần ','Văn','Hải','male','1966-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5|6','unknown','2026-06-07 05:42:18','2026-06-07 05:42:18',NULL,0,NULL,4),(74,NULL,'','Trần','Thị','Thu','female','1971-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'5|6','unknown','2026-06-07 05:42:52','2026-06-07 05:42:52',NULL,0,NULL,6),(75,NULL,'','Võ','Khắc','Thịnh','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-07 05:43:21','2026-06-07 05:43:21',NULL,0,NULL,NULL),(76,NULL,'','Lê','Thị','Minh Tâm','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'78|43','unknown','2026-06-07 08:34:58','2026-06-07 08:34:58',NULL,0,NULL,1),(77,NULL,'','Lê','Thị','Minh Thư','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'78|43','unknown','2026-06-07 08:36:29','2026-06-07 08:36:29',NULL,0,NULL,2),(78,NULL,'','Lê','Kim','Thành','male',NULL,'unknown','2019-12-10','exact',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-07 09:45:01','2026-06-07 09:45:01',NULL,0,NULL,NULL),(79,NULL,'','Trần','Tuấn','Mẫn','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'40|46','unknown','2026-06-07 12:48:03','2026-06-07 12:48:03',NULL,0,NULL,1),(80,NULL,'','Trần','Tuấn','Khoa','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'40|46','unknown','2026-06-07 13:35:08','2026-06-07 13:35:08',NULL,0,NULL,2),(81,NULL,'','Nguyễn','Văn','Điệp','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-08 03:45:49','2026-06-08 03:45:49',NULL,0,NULL,NULL),(82,NULL,'','Nguyễn','Ngọc','Duyên Anh','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'81|41','unknown','2026-06-08 03:46:41','2026-06-08 03:46:41',NULL,0,NULL,1),(83,NULL,'','Nguyễn','Ngọc','Bảo Nhi','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'81|41','unknown','2026-06-08 03:47:21','2026-06-08 03:47:21',NULL,0,NULL,3),(84,NULL,'','Nguyễn','Ngọc','Minh Châu','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'81|41','unknown','2026-06-08 03:53:51','2026-06-08 03:53:51',NULL,0,NULL,2),(85,NULL,'','Lê','Thị','Thanh Phượng','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-08 16:12:12','2026-06-08 16:12:12',NULL,0,NULL,NULL),(86,NULL,'','Trần','Thị','Quỳnh Như','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'73|85','unknown','2026-06-08 16:16:30','2026-06-08 16:16:30',NULL,0,NULL,NULL),(87,NULL,'','Võ','Thị','Thu Thảo','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'75|74','unknown','2026-06-08 16:35:56','2026-06-08 16:35:56',NULL,0,NULL,NULL),(88,NULL,'','Võ','Khắc','Thành','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'75|74','unknown','2026-06-08 16:36:20','2026-06-08 16:36:20',NULL,0,NULL,NULL),(89,NULL,'','Nguyễn','Tường','Mạnh','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'69|72','unknown','2026-06-08 17:00:12','2026-06-08 17:00:12',NULL,0,NULL,NULL),(90,NULL,'','Trần','','Test','other',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-08 17:15:46','2026-06-08 17:15:46',NULL,0,NULL,NULL),(91,NULL,'','Trần','','Lự','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-08 22:47:01','2026-06-08 22:47:01',NULL,0,NULL,NULL),(92,NULL,'','Trần','','Lực','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 01:50:10','2026-06-09 01:50:10',NULL,0,NULL,NULL),(93,NULL,'','Trần','Thị','Lục','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 01:51:18','2026-06-09 01:51:18',NULL,0,NULL,NULL),(94,NULL,'','Trần','','Lựu','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 01:51:55','2026-06-09 01:51:55',NULL,0,NULL,NULL),(95,NULL,'','Trần','Thị','Lê','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 02:05:46','2026-06-09 02:05:46',NULL,0,NULL,NULL),(96,NULL,'','Huỳnh','Thị','Hải','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 02:40:05','2026-06-09 02:40:05',NULL,0,NULL,NULL),(97,NULL,'Têrêxa ','Trần','Thị','Diễm Ly','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 02:44:13','2026-06-09 02:44:13',NULL,0,NULL,NULL),(98,NULL,'Êlizabeth','Trần','Bửu','Trúc Linh','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'20|97','unknown','2026-06-09 03:06:04','2026-06-09 03:06:04',NULL,0,NULL,1),(99,NULL,'','Trần','Bửu','Văn Bình','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-09 03:07:15','2026-06-09 03:07:15',NULL,0,NULL,NULL),(100,NULL,'','Trần','Bửu','Quỳnh Anh','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'20|97','unknown','2026-06-09 03:08:36','2026-06-09 03:08:36',NULL,0,NULL,2),(101,NULL,'','Trần','','Dũng','male','1970-06-18','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-13 02:53:08','2026-06-13 02:53:08',NULL,0,NULL,NULL),(102,NULL,'','Nguyễn','Thụy','Hoài Dung','female','1981-10-18','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-13 02:53:53','2026-06-13 02:53:53',NULL,0,NULL,NULL),(103,NULL,'','Trần','Nguyễn','Bửu Khang','male','2018-05-28','exact',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'101|102','unknown','2026-06-13 02:55:00','2026-06-13 02:55:00',NULL,0,NULL,NULL),(104,NULL,'','Trần','Bửu','Hoàng Trang','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'18|96','unknown','2026-06-13 13:46:25','2026-06-13 13:46:25',NULL,0,NULL,1),(105,NULL,'','Trần','Bửu','Hoàng Vũ','male',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'18|96','unknown','2026-06-13 13:46:54','2026-06-13 13:46:54',NULL,0,NULL,2),(106,NULL,'','Test','','BO 01','male','2000-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'54|55','unknown','2026-06-15 02:11:22','2026-06-15 02:11:22',NULL,0,NULL,1),(107,NULL,'','Test','','BO 02','female','2000-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'54|55','unknown','2026-06-15 02:12:06','2026-06-15 02:12:06',NULL,0,NULL,2),(108,NULL,'','Nguyễn','Thị','Lệ Quyên','female','1956-01-01','year',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'69|72','unknown','2026-06-20 03:21:57','2026-06-20 03:21:57',NULL,0,NULL,NULL),(109,NULL,'','Test','Delete','Deploy','female',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,'unknown',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'null',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'unknown','2026-06-20 03:28:01','2026-06-20 03:28:01',NULL,1,NULL,NULL);
/*!40000 ALTER TABLE `persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'viewer',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `person_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (10,'kinh1','$2b$12$L7ECn6EpHbMpWd3NazvDKOefp9k/jpAJ9jitd4zIqTsv2jPt8gOs2','','admin',1,'2026-06-22 12:47:54',1),(11,'dung101','$2b$12$c2nBfXSrCtDOkmgkXnqhEeaJyf3KOLPYIC7J8BzwXAM.h4zQ9uuX.','','co_operator',1,'2026-06-22 12:48:55',101),(12,'tri22','$2b$12$9fMleox4.tSGxqkzqsZUTuTzkqbHtI86G3INOGPCNq51DwR6hG8UG','','member_basic',1,'2026-06-22 12:50:37',22),(13,'viewer','$2b$12$tdL5igrgYzHd0p4M3lbMJ.gUYTpt8fiismC1EWPsJH3qha.Z7w6VG','','viewer',1,'2026-06-22 12:51:37',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-23 11:58:07

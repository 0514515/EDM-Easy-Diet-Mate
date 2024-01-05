-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: user_diet
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add nutrient',7,'add_nutrient'),(26,'Can change nutrient',7,'change_nutrient'),(27,'Can delete nutrient',7,'delete_nutrient'),(28,'Can view nutrient',7,'view_nutrient'),(29,'Can add usermealevaluation',8,'add_usermealevaluation'),(30,'Can change usermealevaluation',8,'change_usermealevaluation'),(31,'Can delete usermealevaluation',8,'delete_usermealevaluation'),(32,'Can view usermealevaluation',8,'view_usermealevaluation'),(33,'Can add usermeal',9,'add_usermeal'),(34,'Can change usermeal',9,'change_usermeal'),(35,'Can delete usermeal',9,'delete_usermeal'),(36,'Can view usermeal',9,'view_usermeal');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$mIZWsri1YeXWP89BpZeyjY$g06Jz7KyqGrt5uAM73NsPLwa851xwChH0q+J0kYGwYg=','2024-01-03 16:31:42.569442',1,'admin','','','test@test.com',1,1,'2024-01-03 02:11:51.191488');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-01-03 05:18:35.428298','1','Usermeal object (1)',1,'[{\"added\": {}}]',9,1),(2,'2024-01-03 06:42:12.534885','1','Usermealevaluation object (1)',3,'',8,1),(3,'2024-01-03 06:44:48.240504','2','Usermealevaluation object (2)',3,'',8,1),(4,'2024-01-03 08:34:36.904033','1','Usermeal object (1)',2,'[{\"changed\": {\"fields\": [\"Meal date\"]}}]',9,1),(5,'2024-01-03 08:34:53.286121','1','Usermeal object (1)',2,'[{\"changed\": {\"fields\": [\"Meal date\"]}}]',9,1),(6,'2024-01-03 08:35:19.702941','2','Usermeal object (2)',1,'[{\"added\": {}}]',9,1),(7,'2024-01-03 08:35:41.353758','3','Usermeal object (3)',1,'[{\"added\": {}}]',9,1),(8,'2024-01-03 08:36:00.316011','4','Usermeal object (4)',1,'[{\"added\": {}}]',9,1),(9,'2024-01-03 08:36:22.396422','5','Usermeal object (5)',1,'[{\"added\": {}}]',9,1),(10,'2024-01-03 08:36:46.153245','6','Usermeal object (6)',1,'[{\"added\": {}}]',9,1),(11,'2024-01-03 08:37:03.621117','7','Usermeal object (7)',1,'[{\"added\": {}}]',9,1),(12,'2024-01-03 08:37:33.565479','8','Usermeal object (8)',1,'[{\"added\": {}}]',9,1),(13,'2024-01-04 01:45:00.615327','22','Usermeal object (22)',3,'',9,1),(14,'2024-01-04 01:45:00.636671','21','Usermeal object (21)',3,'',9,1),(15,'2024-01-04 01:45:00.643465','20','Usermeal object (20)',3,'',9,1),(16,'2024-01-04 01:45:00.650966','19','Usermeal object (19)',3,'',9,1),(17,'2024-01-04 01:45:00.657806','18','Usermeal object (18)',3,'',9,1),(18,'2024-01-04 01:45:00.665571','17','Usermeal object (17)',3,'',9,1),(19,'2024-01-04 01:45:00.672161','16','Usermeal object (16)',3,'',9,1),(20,'2024-01-04 01:45:00.678550','15','Usermeal object (15)',3,'',9,1),(21,'2024-01-04 01:45:00.686785','14','Usermeal object (14)',3,'',9,1),(22,'2024-01-04 01:45:00.693889','13','Usermeal object (13)',3,'',9,1),(23,'2024-01-04 01:45:00.704426','12','Usermeal object (12)',3,'',9,1),(24,'2024-01-04 01:45:00.711120','11','Usermeal object (11)',3,'',9,1),(25,'2024-01-04 01:45:00.718431','10','Usermeal object (10)',3,'',9,1),(26,'2024-01-04 01:45:00.724528','9','Usermeal object (9)',3,'',9,1),(27,'2024-01-04 01:47:47.225792','24','Usermeal object (24)',3,'',9,1),(28,'2024-01-04 01:47:47.248311','23','Usermeal object (23)',3,'',9,1),(29,'2024-01-04 01:57:25.925983','39','Usermeal object (39)',3,'',9,1),(30,'2024-01-04 01:57:25.935708','38','Usermeal object (38)',3,'',9,1),(31,'2024-01-04 01:57:25.942788','37','Usermeal object (37)',3,'',9,1),(32,'2024-01-04 01:57:25.952822','36','Usermeal object (36)',3,'',9,1),(33,'2024-01-04 01:57:25.962166','35','Usermeal object (35)',3,'',9,1),(34,'2024-01-04 01:57:25.969251','34','Usermeal object (34)',3,'',9,1),(35,'2024-01-04 01:57:25.975501','33','Usermeal object (33)',3,'',9,1),(36,'2024-01-04 01:57:25.983003','32','Usermeal object (32)',3,'',9,1),(37,'2024-01-04 01:57:25.992139','31','Usermeal object (31)',3,'',9,1),(38,'2024-01-04 01:57:25.999943','30','Usermeal object (30)',3,'',9,1),(39,'2024-01-04 01:57:26.008237','29','Usermeal object (29)',3,'',9,1),(40,'2024-01-04 01:57:26.015380','28','Usermeal object (28)',3,'',9,1),(41,'2024-01-04 01:57:26.022791','27','Usermeal object (27)',3,'',9,1),(42,'2024-01-04 01:57:26.029933','26','Usermeal object (26)',3,'',9,1),(43,'2024-01-04 01:57:26.038429','25','Usermeal object (25)',3,'',9,1),(44,'2024-01-04 02:09:15.874936','53','Usermeal object (53)',3,'',9,1),(45,'2024-01-04 02:09:15.896841','52','Usermeal object (52)',3,'',9,1),(46,'2024-01-04 02:09:15.904107','51','Usermeal object (51)',3,'',9,1),(47,'2024-01-04 02:09:15.909102','50','Usermeal object (50)',3,'',9,1),(48,'2024-01-04 02:09:15.916617','49','Usermeal object (49)',3,'',9,1),(49,'2024-01-04 02:09:15.923078','48','Usermeal object (48)',3,'',9,1),(50,'2024-01-04 02:09:15.929018','47','Usermeal object (47)',3,'',9,1),(51,'2024-01-04 02:09:15.936548','46','Usermeal object (46)',3,'',9,1),(52,'2024-01-04 02:09:15.946057','45','Usermeal object (45)',3,'',9,1),(53,'2024-01-04 02:09:15.952847','44','Usermeal object (44)',3,'',9,1),(54,'2024-01-04 02:09:15.959882','43','Usermeal object (43)',3,'',9,1),(55,'2024-01-04 02:09:15.968030','42','Usermeal object (42)',3,'',9,1),(56,'2024-01-04 02:09:15.974729','41','Usermeal object (41)',3,'',9,1),(57,'2024-01-04 02:09:15.980636','40','Usermeal object (40)',3,'',9,1),(58,'2024-01-04 02:28:13.462685','60','Usermeal object (60)',3,'',9,1),(59,'2024-01-04 02:28:13.470406','59','Usermeal object (59)',3,'',9,1),(60,'2024-01-04 02:28:13.476920','58','Usermeal object (58)',3,'',9,1),(61,'2024-01-04 02:28:13.483639','57','Usermeal object (57)',3,'',9,1),(62,'2024-01-04 02:28:13.489895','56','Usermeal object (56)',3,'',9,1),(63,'2024-01-04 02:28:13.494953','55','Usermeal object (55)',3,'',9,1),(64,'2024-01-04 02:28:13.501165','54','Usermeal object (54)',3,'',9,1),(65,'2024-01-04 03:42:44.923964','3','Usermealevaluation object (3)',3,'',8,1),(66,'2024-01-04 03:44:10.914542','4','Usermealevaluation object (4)',3,'',8,1),(67,'2024-01-04 03:45:35.690725','5','Usermealevaluation object (5)',2,'[{\"changed\": {\"fields\": [\"Sum kcal\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'Meal_Date','nutrient'),(9,'Meal_Date','usermeal'),(8,'Meal_Date','usermealevaluation'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'Meal_Date','0001_initial','2024-01-03 00:43:40.903916'),(2,'contenttypes','0001_initial','2024-01-03 00:43:41.032028'),(3,'auth','0001_initial','2024-01-03 00:43:42.812572'),(4,'admin','0001_initial','2024-01-03 00:43:43.519294'),(5,'admin','0002_logentry_remove_auto_add','2024-01-03 00:43:43.535380'),(6,'admin','0003_logentry_add_action_flag_choices','2024-01-03 00:43:43.551014'),(7,'contenttypes','0002_remove_content_type_name','2024-01-03 00:43:43.898194'),(8,'auth','0002_alter_permission_name_max_length','2024-01-03 00:43:44.138280'),(9,'auth','0003_alter_user_email_max_length','2024-01-03 00:43:44.179623'),(10,'auth','0004_alter_user_username_opts','2024-01-03 00:43:44.195901'),(11,'auth','0005_alter_user_last_login_null','2024-01-03 00:43:44.310580'),(12,'auth','0006_require_contenttypes_0002','2024-01-03 00:43:44.319269'),(13,'auth','0007_alter_validators_add_error_messages','2024-01-03 00:43:44.333643'),(14,'auth','0008_alter_user_username_max_length','2024-01-03 00:43:44.490474'),(15,'auth','0009_alter_user_last_name_max_length','2024-01-03 00:43:44.676016'),(16,'auth','0010_alter_group_name_max_length','2024-01-03 00:43:44.719580'),(17,'auth','0011_update_proxy_permissions','2024-01-03 00:43:44.737585'),(18,'auth','0012_alter_user_first_name_max_length','2024-01-03 00:43:45.175456'),(19,'sessions','0001_initial','2024-01-03 00:43:45.297710'),(20,'Meal_Date','0002_nutrient_food_id_alter_usermeal_id_and_more','2024-01-03 00:48:54.832613'),(21,'Meal_Date','0003_alter_usermeal_user_id','2024-01-03 01:24:46.119763'),(22,'Meal_Date','0004_alter_usermeal_user_id_and_more','2024-01-03 01:26:18.583996'),(23,'Meal_Date','0005_alter_usermeal_id','2024-01-03 01:27:48.295857'),(24,'Meal_Date','0006_alter_usermeal_id_alter_usermealevaluation_id','2024-01-03 01:54:05.466069'),(25,'Meal_Date','0007_alter_usermeal_id_alter_usermealevaluation_id','2024-01-03 02:27:30.944620'),(26,'Meal_Date','0008_remove_nutrient_food_id_alter_usermeal_id_and_more','2024-01-03 05:14:51.679617'),(27,'Meal_Date','0009_delete_customuser','2024-01-03 05:14:51.799338'),(28,'Meal_Date','0010_remove_usermealevaluation_sys_config','2024-01-03 06:44:17.244110'),(29,'Meal_Date','0011_rename_sun_fat_usermealevaluation_sum_fat_and_more','2024-01-04 03:38:52.377610'),(30,'Meal_Date','0012_alter_usermeal_image_link','2024-01-04 04:06:22.913285'),(31,'Meal_Date','0013_usermealevaluation_sum_col_and_more','2024-01-04 06:19:30.806602'),(32,'Meal_Date','0014_rename_image_link_usermeal_imagelink_and_more','2024-01-04 15:06:41.924647');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6fpzmyy52spxa2f3in57s9tyhs8o5ze6','.eJxVjDsOwjAQBe_iGll2_Kek5wzWrneNAyiR4qRC3B0ipYD2zcx7iQzb2vLWeckjibPQ4vS7IZQHTzugO0y3WZZ5WpcR5a7Ig3Z5nYmfl8P9O2jQ27dmQ56jsRh8IqfYQqwuGFVDGLSzqHQyniJBQvJRh1LZesSBoFI0Xov3B9mUN-U:1rKwf1:UJMRoZ2ZEFlEWLK8eYbXRAmVCqii28NeHv2d8Ew_Ufg','2024-01-17 08:31:35.028556'),('it05anq564b12317001tbkj5vjc9lqcr','.eJxVjDsOwjAQBe_iGll2_Kek5wzWrneNAyiR4qRC3B0ipYD2zcx7iQzb2vLWeckjibPQ4vS7IZQHTzugO0y3WZZ5WpcR5a7Ig3Z5nYmfl8P9O2jQ27dmQ56jsRh8IqfYQqwuGFVDGLSzqHQyniJBQvJRh1LZesSBoFI0Xov3B9mUN-U:1rL49e:RlOBpYpolZMA5_S09jfM1G4Eq_OM1YMgOztEAXEwEzw','2024-01-17 16:31:42.582283'),('o1z3xkpow2zjfd0unvxtshmxjyomkz8a','.eJxVjDsOwjAQBe_iGll2_Kek5wzWrneNAyiR4qRC3B0ipYD2zcx7iQzb2vLWeckjibPQ4vS7IZQHTzugO0y3WZZ5WpcR5a7Ig3Z5nYmfl8P9O2jQ27dmQ56jsRh8IqfYQqwuGFVDGLSzqHQyniJBQvJRh1LZesSBoFI0Xov3B9mUN-U:1rKqjo:b41DZqhnhBTE2zSEiATrAV3NeqLiOKCxA0TUbi9oH0A','2024-01-17 02:12:08.762667');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nutrient`
--

DROP TABLE IF EXISTS `nutrient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutrient` (
  `Food_Name` varchar(45) NOT NULL,
  `weight_g` double DEFAULT NULL,
  `Energy_kcal` double DEFAULT NULL,
  `carbs_g` double DEFAULT NULL,
  `sugar_g` double DEFAULT NULL,
  `fat_g` double DEFAULT NULL,
  `protein_g` double DEFAULT NULL,
  `nat_mg` double DEFAULT NULL,
  `col_mg` double DEFAULT NULL,
  PRIMARY KEY (`Food_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutrient`
--

LOCK TABLES `nutrient` WRITE;
/*!40000 ALTER TABLE `nutrient` DISABLE KEYS */;
INSERT INTO `nutrient` VALUES ('(검은)콩조림',20,56.83,6.98,2.92,2.09,3.85,102.85,0),('가래떡',100,205.03999999999996,45.05,0,0.33,3.52,254.68,0),('가자미전',150,220.46,6.68,0,7.12,29.97,814.3700000000001,226.88000000000002),('가자미조림',300,301.29,20.339999999999996,5.99,6.9,40.7,1621.2299999999998,165),('가지나물',50,21.87,3.03,0,1.27,0.73,159.17,0),('간자장',650,807.7400000000001,121.75,6.79,26.38,29.279999999999998,2347.77,19.43),('간장게장',250,292.7,13.88,0.17,2.09,32.66,3075.53,223.11999999999998),('갈비삼각김밥',100,183.18,32.75,0,2.59,6.86,398.11999999999995,12.42),('갈비탕',600,240.39999999999998,8.21,0,14.33,18.67,1688.43,189.84),('갈치조림',100,99.39,5.49,0.5,3.92,10.68,463.82000000000005,42),('감자국',700,220.07,37.01,0,2.16,17,1734.15,87.78),('감자밥',200,308,68.64,0,0.08,5.68,5.2,0),('감자볶음',50,57.79999999999999,8.23,0.5,2.53,1.34,219.93999999999997,0),('감자전',200,366.16,53.81,0,13.61,9.67,456.53,0),('감자조림',50,39.01,8.4,0.79,0.2,1.55,265.92,0),('감자탕',900,963.71,49.64,0.9,58.28,60.55,2439.38,143.69),('감자튀김',150,462.11,50.099999999999994,0,25.76,6.24,374.22,0),('갓김치',50,27.64,5.21,0.42000000000000004,0.7,1.98,447.77,3.51),('건새우볶음',20,69.19,4.81,2.7,2.3,7.22,193.09,74.4),('게살죽',800,554.24,103.59,0,7.63,18.15,1533.96,40.87),('경단',100,303.79,67.04,0,0.54,6.58,186.36,0),('고구마맛탕',200,490.93,90.19,1.43,13.53,3.3,213.33,0),('고구마줄기나물',50,30.44,2.97,0,2.24,0.63,255.71,0),('고구마튀김',100,241.56999999999996,34.1,0,10.8,3.21,150.64,19),('고기만두',250,454.39,55.32999999999999,0,18.24,18.66,888.8,21),('고들빼기',50,55.38999999999999,11.99,0,0.56,2.21,733.75,0.55),('고등어조림',250,459.33000000000004,10.96,1.46,25.35,45.37,1177.95,170.15),('고등어찌개',600,605.31,32.03,0,28.2,59.16,2599.71,206.64),('고사리나물',50,43.51,3.8,0,3.26,1.97,251.52999999999997,0),('고추잡채',200,264.22,22.11,8.45,12.71,12.86,850.31,50.8),('고추장아찌',30,22.359999999999996,4.18,3,0.09,0.8,787.3,0),('고추장찌개',500,263.44,20.08,0,12.349999999999998,25.62,935.15,48.14999999999999),('고추전',150,261.44,17.78,0.75,14.86,13.94,359.88,160.65),('고추조림',100,105.88,14.83,2.99,4.18,2.86,802.4599999999999,0),('고추튀김',100,198.35,12.74,0,13.62,6.48,260.65,190),('곤드레밥',350,506.80000000000007,108.05,0,8.37,14.14,88.75,0),('골뱅이국수무침',230,256.42,39.63,0,7.01,10.52,911.74,39.98),('골뱅이무침',100,107.35,15.56,6.06,2.3,7.91,515.92,45.56),('곰탕',300,181.42,15.5,0,5.44,16.59,713.64,33.66),('곱창전골',600,532.65,26.89,0,34.73,38.35,1750.42,230.7),('광어초밥',300,471.6600000000001,72.53,5.23,3.21,33.74,951.2800000000001,126.49999999999999),('광어회 ',100,116.19999999999999,9.34,5.46,1.36,17.2,754.4,74.96),('국수전골',400,643.16,66.93,4,22.389999999999997,45.29,1524.63,81.6),('군만두',250,684.42,76.17,0,31.169999999999998,19.77,983.6999999999999,36),('굴국',450,194.42,11.44,0,8.65,22.8,1775.97,45),('굴전',100,192.80999999999997,13.919999999999998,0,9.07,12.56,331.02,123),('굴짬뽕',900,640.77,115.82,2,7.76,37.39,2385.35,178.2),('근대된장국',450,109.26,8.14,0,3.21,15.31,1453.19,112.86),('기스면',1000,645.61,98.3,0,11,43.52,2279.52,341.1),('기타잡곡밥',200,302.36,65.52,0,0.75,6.71,3.39,0),('김말이튀김',100,240.56000000000003,32.49,0,12.379999999999999,2.25,393.02,0),('김무침',30,81.01,12.189999999999998,6.93,4.12,4.71,498.63,0),('김치국',450,86,13.01,0,3.38,6.03,1646.15,0),('김치김밥',250,377.26,71.8,0,4.62,11.45,967.79,99.6),('김치라면',650,512.26,80.56999999999998,2.27,20.339999999999996,12.97,2628.29,15.4),('김치만두',250,424.63999999999993,60.79,0,13.1,18.43,961.97,20.28),('김치말이국수',600,310.38,60.76,3,2.47,10.42,2335.45,22.229999999999997),('김치볶음',200,189.97,21.83,8.96,12.13,5.29,1513.41,0),('김치볶음밥',500,656.98,79.29,4,5.06,8.74,1094.91,76),('김치우동',800,512.71,99.06,0,4.74,16.74,3003.05,33.44),('김치전',150,285.73,32.07,0,12.48,13.17,785.6,136),('김치찌개',400,243.03,11.93,3.02,15,15.07,1962.14,25.18),('깍두기',50,17.99,3.94,0.05,0.23000000000000004,1,338.88,4.07),('깐풍기',200,585.08,43.36,13.94,33.34,27.8,629.27,173),('깨강정',30,150.3,13.62,0,9.87,4.5,24.3,0),('깨죽',800,505.68,71.13,0,18.94,13.43,1212.27,0),('깻잎김치',150,124.49,23.27,2.99,3.16,6.1,1907.6399999999999,29.66),('깻잎나물볶음',200,212.39,17.33,0.2,16.37,8.03,1046.43,5.2),('깻잎장아찌',30,33.64,7.87,2.78,0.36,2.11,568.75,0.63),('깻잎전',150,357.62,16.65,0.75,24.64,18.3,464.94,171.38),('꼬리곰탕',700,750.69,10.93,0,52.79999999999999,54.87,764.73,361.23),('꽁치조림',150,280.09,8.36,1.39,16.67,22.59,679.42,67.2),('꽁치찌개',300,356.63,14.479999999999999,0.72,20.689999999999998,29.51,1296.33,84.48),('꽃게탕',600,240.64999999999998,20.77,0,5.49,31.7,2268.86,207.9),('꿀떡',100,225.92,50.35999999999999,9.58,0.76,3.24,251.33999999999997,0),('나박김치',100,14.75,2.25,0.01,0.42000000000000004,0.63,509.47,0),('낙지볶음',200,180.59,23.509999999999998,6.7,3,17.87,868.88,135.2),('낙지탕',600,186.1,11.77,0,2.73,29.21,1711.1200000000001,249.6),('내장탕',700,549.81,13.7,0,31.51,56.97,2383.07,467.03999999999996),('노각무침',150,81.35,16.43,5.09,2.07,3.09,822.1,0),('녹두빈대떡',100,200.70999999999998,18.64,0,8.32,9.96,246.03,13.75),('농어초밥',250,414.78000000000003,74.14,6.97,2.37,19.93,1385.46,43.46999999999999),('느타리버섯볶음',150,133.32,14.22,0.15,8.93,4.41,625.25,0),('다식',30,105.17,20.81,6.46,1.73,3.55,3.85,0),('단감',100,27,4.74,2.14,0.94,0.92,1671,0),('단무지',30,3.9,0.66,0.23000000000000004,0.16,0.11000000000000001,173.55,0),('단무지무침',50,19.19,3.22,0.97,0.9099999999999999,0.4699999999999999,447.86,0),('달걀국',450,193.04,5.35,0,11.11,16.19,1263.96,641.25),('달걀말이',100,172.24,4.67,0,11.23,12.04,323.32,475),('달걀장조림',100,133.72,10.03,3.17,6.39,8.75,636.61,308.75),('달걀찜',250,190,4.81,0,10.91,16.2,860.32,634.57),('달래나물무침',150,132.69,25.26,13.54,3.3,4.77,852.99,0),('닭갈비',300,562.1,24.539999999999996,3.51,28.89,52.3,975.55,224.10000000000002),('닭강정',100,323.25,24.21,1.74,15.56,18.34,413.14000000000004,107.5),('닭개장',700,317.07,19.18,0,14.95,33.74,1786.03,96.9),('닭곰탕',650,527.7,15.39,0,24.14,58.879999999999995,1005.19,230.48999999999998),('닭꼬치',70,177.51,12.9,8.58,7.9,12.349999999999998,287.26,47.599999999999994),('닭볶음탕',300,371.81,19.17,2.02,17.32,33.85,1030.45,119.24999999999999),('닭죽',1000,1181.71,92.53,0,48.17999999999999,75.93,789.79,271.44),('닭칼국수',900,643.1,70.24,0,19.59,39.86,2492.77,113.77),('닭튀김',300,909.8099999999998,45.92,0,52.339999999999996,54.55,1150.13,380.62),('대구찜',500,372.68,26.42,0,8.43,54.07999999999999,1888.04,196.35),('더덕구이',100,183.74,31.779999999999998,10.85,5.62,5.8,745.78,0),('더덕무침',150,220.89,48.43999999999999,31.54,2.74,4.89,1203.58,0),('도가니탕',800,563.65,5.58,0,34.77,54.6,599.27,192.64),('도라지나물',50,54.67,5.33,0,3.82,0.67,256.67,0),('도라지생채',150,165.21999999999997,38.59,3,1.71,4.15,789.08,0),('도미찜',100,126.31000000000002,0.76,0,3.68,21.009999999999998,882.04,191.25),('도토리묵',100,43.05,9.87,1.4,0.35,0.4,116.47000000000001,0),('돈가스',200,620.64,36.56,0,39.12,27.78,557.09,138.34),('돌솥밥',350,528.86,101.85,0,8.35,10.19,618.31,2.37),('동그랑땡',150,312.41,14.71,0,18.72,19.67,579.81,184.28),('동치미',400,57.69,14.26,0,0.64,2.7,2313.58,0),('동태전',150,265.25,11.48,0,16.14,19.87,672.98,134.56),('동태조림',250,270.61,16.77,5,4.09,39.03,1440.17,211.05),('동태찌개',800,369.69,18.94,1.38,7.8,59.57,2487.54,292.66),('돼지갈비',100,248.52000000000004,7.6,5.01,14.7,19.95,344.89,72.04),('돼지갈비찜',170.09999999999997,249.7,8.82,1.76,14.42,20.56,946.68,70.38),('돼지고기김치찌개',400,246.29,9.33,0,18.26,15.5,1961.48,25.3),('돼지고기메추리알장조림',50,62.97,3.14,0.8400000000000001,2.11,7.62,555.78,77.3),('돼지고기볶음',200,353.13,15.329999999999998,4.75,20.94,25.75,1060.33,84),('돼지고기수육',300,1218.19,8.69,0,99.52,61.47,389.53,191.4),('돼지국밥',1200,811.4399999999999,78.28,3.3,36.45,56.75,1257.67,734.5),('돼지껍데기볶음',150,346.14,22.73,15.84,19.23,22.389999999999997,759.29,95.4),('된장찌개',400,147.06,15.98,0,5.27,11.71,2021.7800000000002,0),('두부고추장조림',50,67.14,4.03,1.89,4,5.14,199.23,0),('두부구이',100,90.67,1.53,0,6.27,9.41,164.39,0),('두부김치',250,292.42,13.839999999999998,0,21.32,19.15,1033.85,30),('두부부침',100,134.88,4.29,0,8.76,9.92,199.83,0),('두부전',150,253.89,8.08,0,18.02,18.66,500.53000000000003,66.5),('두부전골',500,315.11,16.2,0.86,19.15,29.14,1651.53,0),('들깨칼국수',600,442.31999999999994,76.67,2.4,6.78,17.48,1695.77,16.72),('땅콩조림',20,80.42,6.54,3.27,5.11,2.91,154.25,0),('떡갈비',250,762.99,26.61,12.49,51.57999999999999,43.09,838.84,157.5),('떡국',800,714.99,144.02999999999997,0,5.39,21.86,2019.2800000000002,90.8),('떡라면',700,672.18,121.07999999999998,0,17.58,15.45,2214.36,2.34),('떡만둣국',700,625.35,113.96,0,9.4,22.72,1999.1199999999997,298.81),('떡볶이',200,300.76,58.849999999999994,5.7,2.96,8.72,862.2300000000001,6),('라면',550,509.33000000000004,83.17,0,17.75,14.079999999999998,1695.5,2.34),('라볶이',200,266.03,41.13,6.36,9.59,7.96,836.2400000000001,6.9),('마늘장아찌',30,16.06,3.07,0.3,0.02,0.79,481.75,0),('마늘쫑무침',30,38.12,9.35,3.28,0.28,0.9800000000000001,423.4599999999999,0),('마늘쫑장아찌',50,28.27,6.19,2.35,0.13,1.04,778.6,0),('마파두부',200,226.91999999999996,10.99,0.57,12.01,16.85,647.45,19.15),('막국수',550,566.89,111.3,11.019999999999998,5.09,26.95,1828.02,37.1),('만둣국',700,432.62,53.28,0,14.92,19.24,2356.67,94.22),('매운탕',600,402.78999999999996,18.83,1.55,21.559999999999995,37.16,2130.95,148.77),('매작과',30,121.48,19.06,0,3.57,2.55,31.05,0),('머위나물볶음',150,102.99000000000001,7.71,0,7.95,4.3,696.91,0),('메밀국수',600,588.68,120.09,10.16,4.53,25.26,1962.46,35.98),('메밀전병',100,166.13999999999996,24.82,0,5.5,5.79,340.66,0),('메추리알장조림',100,205.08,7.36,2.45,13.69,12.109999999999998,758.9,530.64),('멸치볶음',20,69.22,5.69,3.43,2.04,6.97,274.1,83.55),('명란젓',10,12,0.27,0,0.3,2.05,353.1,35),('모래집튀김',150,457.3399999999999,31.86,0,25.89,22.29,297.01,137.65),('무나물',50,34.58,3.04,0,2.56,0.58,293.52,0),('무말랭이',30,39.89,9.63,1.03,0.34,1.36,378.78,0.04),('무생채',150,73.68,16,4.5,1.28,2.63,832.1900000000002,1.68),('무장아찌',30,27.34,5.31,3.3,0.26,0.57,933.2799999999999,0),('무지개떡',100,218.18,48.7,6.99,0.86,4,277.71,0),('무피클',50,17,4.19,1.99,0.05,0.4,6.6,0),('문어숙회',80,67.49,0.18,0,0.73,14.14,222.82999999999998,116.74),('문어초밥',250,377.97,71.83,4.98,1.03,16.9,1420.92,96),('물냉면',800,579.71,96.4,1.2,9.78,28.78,2586.16,178.22),('물만두',120,158.04999999999998,20.48,0,5.84,5.86,269.52,7.59),('미꾸라지튀김',100,382.13,30.57,0,22.54,12.69,323.26,121.30000000000001),('미나리나물',50,28.34,2.56,0,2.14,0.99,165.51999999999998,0),('미나리전',150,215.86000000000004,30.1,0,8.63,6.09,235.65,28.5),('미소된장국',150,37.97,1.69,0,1.75,4.14,511.9800000000001,15.67),('미역국',500,50.16,4.69,0,4.35,2.7,1527.55,0),('미역오이냉국',450,77.35,19.74,8.99,1.35,5.61,1483.6,0),('미역초무침',50,24.94,5.7,4,0.54,1.07,285.8,0),('바지락조개국',550,159.25,8.51,0,1.84,25.83,1650.85,145.2),('배추겉절이',50,21.239999999999995,4.48,1,0.5,0.9399999999999998,325.41,1.34),('배추김치',50,18.43,4.15,0.5,0.3,1.15,309.53,3.41),('배추된장국',700,121.53,11.04,0,3.63,13.96,2321.48,25.97),('배추전',150,241.01,32.51,0,10.489999999999998,6.41,355.98,30.4),('백김치',50,19.8,4.38,0,0.26,0.8,211.72,0.04),('백설기',100,218.82000000000002,48.2,11.99,0.79,4.04,296.95,0),('버섯전',150,239.68000000000004,18.61,0.75,12.93,11.93,307.92,126.08),('버섯찌개',400,171.86,15.26,0,7.52,16.64,1267.81,0),('보리밥',200,316.1,70.57,0,0.14,5.55,4.5,0),('볶음밥',400,687.74,100.33000000000001,0,19.29,24.46,1441.42,309),('볶음우동',300,377.92,62.26,0.9099999999999999,10.809999999999999,9.58,1461.31,0),('부대찌개',600,525.98,46.81,0,28.479999999999997,27.709999999999997,2689.19,42.96),('부추김치',50,32.91,6.29,3.49,0.57,1.88,399.38,0),('부추전',150,241.18,32.01,0,9.5,7.14,255.16,7.12),('북어조림',100,184.58,15.66,2.91,3.04,23.88,761.39,103.95),('북어채무침',150,332.05,31.33,18.02,5.8,37.37,1048.53,108.57),('불고기',150,386.79,13.05,1.1,21.779999999999998,32.9,632.54,106.22),('불고기덮밥',500,699.96,92.08999999999999,5.99,21.399999999999995,29.31,1182.88,72),('비빔국수',550,577.17,114.47,11.01,9.55,16.71,1628.3,0),('비빔냉면',550,594.31,91.49,2,9.13,23.7,1530.57,31.73),('뼈다귀해장국 ',1000,715.98,29.71,0,45.37,53.63,3093.6,216.23999999999998),('뼈해장국',1000,692.93,25.42,0,37.16,67.92,3192.46,634.2),('산자',30,121.7,24.699999999999996,10.63,1.2,0.9099999999999999,8.01,0),('산채비빔밥 ',400,495.89,89.66,0.52,10.99,10.66,1060.78,0),('삼계탕',1000,881.32,44.07999999999999,0,40.57,76.65,1211.32,285),('삼선볶음밥',400,683.62,113.43,5.09,16.84,19.26,1155.81,119.13),('삼선우동',1000,692.26,89.19,2,10.53,56.17,2351.43,640.67),('삼선자장면',700,787.84,111.57,2,24.68,38.33,2791.11,162.24),('삼선짬뽕',900,629.1,89.31,3,13.45,39.17,2825.66,249.30000000000004),('삼치구이',200,355.71,8.48,0,18.01,37.83,797.71,156.87),('상추겉절이',200,130.62,17.99,2,6.25,5.65,952.32,5.36),('새우볶음밥',400,634.52,91.62,0,17.91,24.11,1124.63,127.2),('새우초밥',250,395.54,69.54,2.99,1.21,22.74,1396.75,138.33),('새우튀김',100,311.26,21.83,0,19.64,11.83,553.89,165.9),('새우튀김롤',300,572.02,81.5,4,18.9,21.109999999999996,1512.5,96.53999999999999),('샐러드김밥',250,422.43000000000006,75.84,0,7.51,12.76,906.6799999999998,100.53),('생선가스',200,646.21,57.38,0,37.09,24.5,817.2699999999999,176.3),('생선물회',800,575.01,81.44999999999999,29.37,14.13,36.77,2986.23,0.76),('생연어',100,110.28999999999999,1,0,1.94,20.91,213.05999999999997,60),('선지(해장)국',1000,314.42,22.29,0,5.03,48.1,3053.19,149.6),('설렁탕',600,422.76,10.939999999999998,0,18.2,52.71,725.16,219.35999999999999),('소갈비찜',250,500.45,11.31,0,29.16,42.55,768.42,141.82),('소고기국밥',700,331.71,54.93,0,4.74,16.04,1613.21,25.499999999999996),('소고기김밥',250,425.67,76.07,0,6.64,14.67,1477.98,99.87),('소고기메추리알장조림',50,61.22,3.45,1,2.21,6.67,608.29,70.17),('소고기무국',400,125.22,8.14,0,4.72,13.51,1095.18,28.56),('소고기미역국',650,154.93,6.91,0,6.83,20.23,2006.8699999999997,41.34),('소고기버섯죽',800,573.24,102.93,0,6.46,20.52,1263.62,29.31),('소고기전골',300,203.22,16.55,0,7.54,19.47,1090.15,31.8),('소곱창구이',150,639.11,6.51,0,51.71,35.62,332.72,652.5),('소머리국밥',1100,891.43,77.06,0,40.76,48.94,970.89,477.09999999999997),('소불고기',200,174.73,19.63,9.49,4.68,14.22,828.15,27.93),('소세지볶음',200,476.0400000000001,28.81,5.83,33.24,17.04,1409.05,56.25999999999999),('소양념갈비구이',300,986.92,27.74,14.31,66.48,61.97,1272.34,220.96),('송이덮밥',600,600.42,103.56999999999998,0,14.449999999999998,16.28,1578.85,9.54),('송편',100,234.9,46.82,1.52,2.7,4.17,236.53999999999996,0),('수수부꾸미',100,258.99,46.15,3,5.67,5.5,270.04,0),('수수팥떡',100,212.73,45.17,1,0.68,5.98,236.38,0),('수제비',800,622.15,99.22,0,6.54,38.53,1669.32,209),('숙주나물',50,19.51,1.56,0,1.35,1.31,186.73,0),('순대국',800,550.66,22.82,0,32.94,41.22,1532.59,774.77),('순대국밥',900,690.35,34.23,0,16.48,17.34,3418.2,1480.97),('순대볶음',400,579.56,70.96,14.289999999999997,25.61,17.58,1379.55,189.91999999999996),('순두부찌개',400,198.47,8.78,0,14.03,14.719999999999999,1331.31,6.6),('시금치나물',50,37.51,3.81,0,2.37,2.07,217.26000000000002,0),('시금치된장국',400,121.45000000000002,9.9,0,3.39,16.69,1381.25,117.04),('시래기된장국',450,99.12,10.68,0,2.54,10.02,1535.63,37.62),('시루떡',100,223.62,49.03,5.99,0.28,5.5,278.95,0),('쌀국수',600,321.34,46.2,2.2,5.81,21.85,2032.16,123.03),('쌀밥',210,334.8,73.71,0,0.45,5.76,59.39999999999999,0),('쑥갓나물무침',150,94.86,8.78,0,6.51,5.49,700.12,0),('쑥된장국',450,117.31,17.17,0,2.55,13.21,1799.6,68.97),('쑥떡',100,238.05999999999997,54.64,9.99,0.45,4.53,256.15,0),('아귀찜',400,310.7,17.59,0,6.68,48.849999999999994,1463.31,187.42),('아욱된장국',450,103.53000000000002,9.96,0,2.94,12,1462.13,37.62),('알감자조림',50,56.22999999999999,10.48,1.57,1.26,1.38,241.73,0),('알밥',400,606.54,92.1,0,3.45,15.16,1647.87,39),('알탕',700,424.12,49.519999999999996,14.849999999999998,6.98,49.21,2393.29,610.8),('야채전',100,194.94,24.97,0,8.78,4.95,322.92,23.75),('약과',30,113.84999999999998,22.18,2.15,1.24,2.57,16.46,0),('약식',100,232.21000000000004,48.879999999999995,7.99,2.27,3.83,290.64,0.16),('양념게장',200,275.55,46.33,26.52,2.06,20.41,1747.84,134.4),('양념왕갈비',150,485.51,15.04,8.35,33.71,29.33,533.19,103.49999999999999),('양념치킨',200,567.58,38.84,12.36,31.15,30.469999999999995,777.86,259),('양배추구이',100,60.93,7.62,0.8400000000000001,2.65,2.71,242.34,5.5),('양송이버섯볶음',150,132.42,10.55,0,9.79,5.46,520.11,0),('양파장아찌',50,19.71,3.54,1.5,0.05,0.58,423.61,0),('어묵국',600,252.09,37.16,0,4.21,22.85,2022.7400000000002,100.37),('어묵볶음',150,281.54,36.28,4.47,8.08,18.04,1283.83,18.9),('어죽',800,559.27,90.47,0,6.08,15.53,1621.29,75.77),('연근조림',50,87.19,14.71,1.39,2.55,1.34,330.58,0),('연어롤 ',300,518.58,76.11,0,14.719999999999999,20.72,1243.82,51.73),('연어초밥',250,451.03,70.87,3.96,5.76,24.94,995.0300000000001,54.6),('연포탕',1000,541.19,21.64,0,9.2,91.65,2307.07,844),('열무김치',50,16.29,3.16,1.2,0.35,1.34,308.35,0),('열무김치국수',800,488.31999999999994,81.61,0,8.22,21.939999999999998,2587.7,45.14),('열무비빔밥',400,445.65999999999997,90.03,1.72,3.16,12.989999999999998,718.39,12.8),('열무얼갈이김치',50,16.57,3.03,0,0.4,1.27,344.2,4.2),('오리불고기',250,559.93,24.47,4.07,34.25,38.16,854.07,124.82),('오리탕',600,480.82000000000005,24.16,1.03,21.64,43.209999999999994,1849.93,161.7),('오므라이스',450,684.99,101.62,0,19.75,23.15,1123.24,605.62),('오삼불고기',200,356.94,21.459999999999997,7.42,20.24,23.349999999999998,870.4000000000001,164.29999999999998),('오이생채',50,23.36,4.63,1.52,0.5,0.89,269.31,0),('오이소박이',50,16.67,2.96,1.2,0.53,0.9399999999999998,276.19,1.45),('오이지',50,11.44,2.39,0,0.31,1.14,926,0),('오이피클',50,54,14.639999999999999,1.99,0.15,0.3,333.6,0),('오일소스스파게티',400,626.58,99.24,0,16.59,14.68,968.7000000000002,0),('오징어국',500,169.02999999999997,10.6,0,2.35,27.74,1573.42,296.4),('오징어덮밥',500,693.98,83.42999999999999,2.69,20.92,40.59,1497.37,387.6),('오징어무침',200,249.52999999999997,13.549999999999999,0,4.19,38.67,682.39,430.9200000000001),('오징어볶음',200,243.7,27.419999999999998,9.28,6.84,20.43,1025.86,198),('오징어젓갈',10,6.83,0.29,0,0.1,1.24,179.11,13.679999999999998),('오징어채볶음',20,55.709999999999994,7,1.35,0.69,5.39,240.96,50.05),('오징어튀김',100,308.43,26.02,0,16.5,13.46,361.57,133),('우거지나물무침',150,126.10999999999999,10.28,1.5,8.66,5.08,774.55,0),('우거지된장국',450,85.97,13.72,0,1.81,6.44,1593.99,0),('우거지해장국',600,158.5,14.86,0,5.73,14.19,1972.09,13.26),('우렁된장국',500,245.27999999999997,21.19,0,7.05,24.72,2150.43,22.95),('우엉조림',30,68.5,15.51,7.61,0.33,1.1,242.28,0),('유과',30,129.06,24.14,1.12,3.5,0.36,7.06,0),('유부초밥',250,463.2099999999999,78.47,6.76,11.23,12.37,929.07,0),('육개장',440,137.86,11.62,0,5.87,13.439999999999998,1112.78,24.219999999999995),('육사시미',150,203.55000000000004,6.96,4.09,6.07,29.279999999999998,888.03,63.45),('육전',100,197.1,6.72,0.3,9.51,19.58,248.68,91.5),('육회',150,236.56,15.95,7.04,8.05,25.03,433.42,57.75),('육회비빔밥',450,661.41,91.74,2.58,17.54,32,1126.6,241.65),('인절미',100,214.46,42.55,0,1.76,6.4,337.74,0),('일반김밥',200,348.87,63.64,0,5.42,10.28,951.3200000000002,69.12),('일반비빔밥',500,703,95.68,3.44,25.28,22.6,1234.09,40.2),('일식우동',700,420.79,81.23,0.5,1.74,16.93,1873.54,16.2),('자장면',650,760.88,134.29,7.99,23.159999999999997,15.74,2447,3.08),('자장밥',500,729.62,98.08,4,24.95,25.76,1521.85,36),('잔치국수',700,564.23,104.66,0.44000000000000006,6.23,20.26,1792.23,167.41),('잡채',150,198.82,37.47,2.99,4.7,2.59,664.75,14.25),('잡채밥',650,851.54,125.70000000000002,4,28.609999999999996,21.139999999999997,2251.34,36),('잡탕밥',750,737.23,100.55000000000001,0,22.48,29.02,1922.1400000000003,188.04999999999998),('잣죽',700,872.61,153.78999999999996,0,20.29,15.79,850.63,0),('장어덮밥',400,671.72,103.03999999999999,0,19.24,26.139999999999997,893.22,156.96),('장어초밥',400,486.35,74.84,2.06,12.73,16.33,1291.81,130.43),('전복죽',800,587.29,105.04,0,11.45,14.57,1423.9300000000003,45.15),('전주비빔밥',450,662.19,92.99,3.44,13.03,15.84,1281.3,286.94),('전주콩나물국밥',900,432.38000000000005,88.73,0,3.52,12.5,1753.26,2.77),('절편',100,197.80999999999997,44.07,5,0.35,3.06,266.77,0),('제육덮밥',500,796.94,95.8,5.4,27.519999999999996,37.8,1375.69,108),('조기조림',300,378.26,14.239999999999998,1.45,16.26,41.43,1682.9,176.61),('조기찜',100,185.25,1.81,0.34,9.2,22.27,631.89,105.74),('족발',150,381.57,32.3,0,16.62,26.02,839.1399999999999,98),('주꾸미볶음',200,211.81,21.69,6.7,6.11,20.16,969.88,385.6),('주먹밥',150,209.56,36.18,0,3.46,6.7,329.69,50.129999999999995),('쥐치채',20,53.39,10.18,6.6,0.2,2.77,289.45,5.93),('쥐포튀김',100,353.33,37.99,0,16.54,11.209999999999999,423.80000000000007,75.64),('증편',100,198.69,44.22,15.98,0.34,2.54,259.04,0),('지리탕',600,260.59,10.52,0,8.36,38.34,1685.1599999999999,154.15),('짜장라면',250,409.38,63.77,0,14.849999999999998,12.01,1276.38,1.5),('짬뽕',1000,650.31,118.54,0,13.519999999999998,25.52,3451.37,105.22),('짬뽕라면',750,633.34,88.79,0,24.63,31.41,2380.93,85.28),('짬뽕밥',900,696.69,93.42,0,22.419999999999998,41.8,2869.54,304.3),('쫄면',450,622.42,110.85000000000001,22.13,6.93,12.36,1271.55,0),('찜닭',1500,1358.38,140.64,57.52,36.54,114.9,5290.09,341.64),('찰떡',100,216.19000000000003,44.88,5.5,1.24,5.81,236.82,0),('참꼬막',80,89.77,4.92,1.6,2.17,12.98,400.23,46.989999999999995),('참치김밥',250,401.21999999999997,47.55,0,14.59,19.82,925.73,143.67),('참치김치찌개',400,193.58,13.33,0,10.889999999999999,16.86,2604.45,35.44),('참치마요삼각김밥',100,189.58,31.93,0,2.89,8.11,189.1,16.63),('참치죽',800,658.46,105.93999999999998,0,13.85,26.079999999999995,1264.15,40.75),('찹쌀떡',100,264.74,62.08,13.99,0.23000000000000004,3.41,226.37999999999997,0),('채소죽',800,514.83,100.8,0,5.13,11.89,1211.63,24.29),('채소튀김',100,311.99,36.35,0,18.53,3.01,277.28,0),('청국장찌개',400,275.46,14.97,0,14.43,25.84,1839.75,36),('청포묵무침',250,157.61,19.68,13.74,4.22,2.96,756.74,2.35),('총각김치',50,17.56,3.44,0,0.37,1.03,347.17,4.43),('추어탕',700,338.67,24.42,1.81,11.51,37.37,2077.15,298.48),('취나물',50,72.94,3.46,0,6.71,1.6,288.65,0),('치즈김밥 ',250,462.23,77.12,0,8.84,17.12,919.97,83.02),('치즈돈가스',250,758.5,45.48,0,46.15,36.02,855.05,146.4),('치즈라면',600,598.67,83.53,0,23.28,23.349999999999998,2425.97,302.2),('치킨가스',200,582.01,51.28,0,28.639999999999997,31.03,748.73,113.3),('치킨데리야끼',340,692.52,50.73,3.64,32.19,47.339999999999996,865.98,171.25),('치킨윙',100,219.42,9.96,2.45,14.23,11.4,351.39,66),('카레라이스',500,653.24,92.57999999999998,0,10.67,13.4,1108.55,13.75),('캘리포니아롤',300,468.16,81.22,0,9.73,12.8,1351.96,28.34),('코다리조림',100,146.67,4.57,0.5,5.62,18.46,433.18,77.6),('콘스프',400,280.48,35.37,0,14.02,5.82,1319.46,40.709999999999994),('콩국수',800,623.5,67.12,1,20.43,47.79999999999999,875.84,0),('콩나물',50,24.13,1.14,0,1.98,1.64,203.5,0),('콩나물국',400,22.53,1.26,0,1.42,1.82,752.42,7.41),('콩밥',200,322.9,65.85,0,1.67,8.43,4.1,0),('콩비지찌개',400,248.66000000000003,24.52,0,12.81,15.96,1206.33,27.06),('콩조림',20,59.22,7.75,2.92,1.94,3.57,234.7,0),('크림소스스파게티',400,825.0599999999998,85.88,0,45.4,19.44,1025.21,140.15),('탕국',250,94.24,2.58,0,4.32,12.08,663.05,35.48),('탕수육',200,454.43999999999994,56.49,1.9,16.59,17.06,403.25999999999993,76.47),('탕평채',100,101.19,10.2,6.99,3.11,3.53,247.41999999999996,4.95),('토란국',250,462.9700000000001,85.16,0,7.07,23.89,700.67,37.72),('토마토소스스파게티',500,642.18,102.07,0,17.37,20.22,1404.81,12.65),('토마토스프',400,382.40999999999997,12.42,0,25.4,18.2,1544.31,70.8),('파김치',50,28.01,5.47,1,0.7,1.55,395.86,4.69),('파래무침',30,31.589999999999996,5.43,0.9,0.69,2.34,252.05,0),('파무침',150,124.29999999999998,19.47,8.37,5.41,3.82,693.83,10.05),('파전',150,280.55,37.45,0,12.04,7.73,338,57),('팥죽',600,482.6499999999999,100.73999999999998,4.79,0.56,20.59,1026.11,0),('표고버섯볶음',150,143.59,14.28,1.49,7.36,4.01,563.59,0),('하이라이스',360,477.59999999999997,84.58999999999999,0,9.67,7.92,991.6800000000001,8.57),('한치초밥',250,389.96,77.31,1.74,1.2,13.54,1153.49,0.75),('해물덮밥',700,837.9799999999999,100.11000000000001,0,29,51.77,2117.83,293.87),('해물볶음',400,420.5299999999999,36.53,7.66,15.32,37.48,1647.02,376.2),('해물볶음밥',400,659.23,85.19,0,23.71,22.679999999999996,951.0299999999999,362.4),('해물찜',500,397.37,36.02,0,8.94,50.28,2213.44,323.98),('해물칼국수',900,621.2,124.21,0,4.01,24.87,2195.05,156.77),('해물탕',600,272.26,19.58,1.55,3.38,41.74,2071.99,350.22),('해물파전',150,267.23,27.679999999999996,0,12.57,12.94,356.43,96.84),('해파리냉채',150,87.28,13.83,7.49,1.55,6.63,490.13,17.62),('햄김치찌개',300,190.47,15.44,0,10.68,11.63,1527.82,23.37),('햄버거스테이크',200,436.74999999999994,21.35,0,28.05,24.919999999999998,920.26,75.78),('햄부침',100,232.6,9.73,0,15.48,13.069999999999999,774.68,52.15),('현미밥',230,351.35,77.88,0,1.1,6.66,42.08,0),('호박볶음',50,29.19,3.09,0,2.01,0.77,223.28,0.07),('호박부침개',100,130.72,8.67,0,9.23,3.37,172.03,61.75),('호박전',150,215.28,16.56,0,14.42,6.59,274.63,106.88),('호박죽',600,430.33,111.40999999999998,25.78,0.72,8.11,911.72,0),('호박찌개',300,98.3,12.74,2.06,2.34,7.78,1028.14,59.28),('홍어무침',200,193.14,24.9,9.43,2.27,21.64,817.4199999999998,79.2),('홍합미역국',650,168.87999999999997,14.13,0,6.43,19.99,2066.27,79.62),('황태해장국',600,184.22,6.39,0,7.22,25.209999999999997,1526.82,91.61),('회냉면',550,638.9,131.9,22.73,8.78,20.22,1524.28,92.89),('회덮밥',500,698,101.75,18.41,11.4,42.99,777.63,125.59),('회무침',300,311.59,42.88,26.41,4.26,27.18,1253.25,61.379999999999995),('훈제연어',100,169,9.34,5.46,6.16,19.28,1260.8,141.6),('훈제오리',250,789.96,11.83,6.25,64.65,38.16,1216.98,200.25),('흑미밥',200,318,70.29,0,0.39,5.44,4.5,0);
/*!40000 ALTER TABLE `nutrient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermeal`
--

DROP TABLE IF EXISTS `usermeal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermeal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` char(32) NOT NULL,
  `meal_type` longtext,
  `meal_date` date DEFAULT NULL,
  `imagelink` varchar(100) NOT NULL,
  `food_name_id` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usermeal_food_name_id_fc3239e6_fk_nutrient_Food_Name` (`food_name_id`),
  CONSTRAINT `usermeal_food_name_id_fc3239e6_fk_nutrient_Food_Name` FOREIGN KEY (`food_name_id`) REFERENCES `nutrient` (`Food_Name`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermeal`
--

LOCK TABLES `usermeal` WRITE;
/*!40000 ALTER TABLE `usermeal` DISABLE KEYS */;
INSERT INTO `usermeal` VALUES (1,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-03','a','가래떡'),(2,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-02','ㅇㅇㅇ','가래떡'),(3,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-01','ㄴㄴㄴ','가래떡'),(4,'950cfbad7a9e43c0a11af905fe67dafb','아침','2023-12-31','ㅇㅇ','가래떡'),(5,'950cfbad7a9e43c0a11af905fe67dafb','저녁','2023-12-30','ㅇㅇㄴㄴ','가래떡'),(6,'950cfbad7a9e43c0a11af905fe67dafb','저녁','2023-12-28','ㅇㅇㅇㄴ','가래떡'),(7,'950cfbad7a9e43c0a11af905fe67dafb','저녁','2023-12-26','ㅇㅇㅇ','가자미전'),(8,'950cfbad7a9e43c0a11af905fe67dafb','아침','2023-12-25','ㅇㄴㅁ','간장게장'),(61,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','연근조림'),(62,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','단감'),(63,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','홍어무침'),(64,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','약식'),(65,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','파김치'),(66,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','코다리조림'),(67,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','김치찌개'),(68,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','참치김밥'),(69,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','a','참치김밥'),(70,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','images/asd.png','(검은)콩조림'),(71,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','images/asd_5e8o8r6.png','(검은)콩조림'),(72,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','images/asd_00IeDUV.png','(검은)콩조림'),(73,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','연근조림'),(74,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','단감'),(75,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','홍어무침'),(76,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','약식'),(77,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','파김치'),(78,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','코다리조림'),(79,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','[<InMemoryUploadedFile: asd.png (image/png)>]','김치찌개'),(80,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-01','images/asd_XUSTvHs.png','연근조림'),(81,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-01','images/asd_aVIYnJU.png','연근조림'),(82,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','연근조림'),(83,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','단감'),(84,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','홍어무침'),(85,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','약식'),(86,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','파김치'),(87,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','코다리조림'),(88,'950cfbad7a9e43c0a11af905fe67dafb','아침','2024-01-04','<실제 이미지를 넣어주세요>','김치찌개'),(89,'1223cb0d0d844aa6ae51cc4f679e3a0a','아침','2024-01-04','','쌀밥'),(90,'1223cb0d0d844aa6ae51cc4f679e3a0a','아침','2024-01-04','','곰탕'),(91,'1223cb0d0d844aa6ae51cc4f679e3a0a','아침','2024-01-04','','김치전'),(92,'1223cb0d0d844aa6ae51cc4f679e3a0a','점심','2024-01-04','<실제 이미지를 넣어주세요>','쌀밥'),(93,'1223cb0d0d844aa6ae51cc4f679e3a0a','점심','2024-01-04','<실제 이미지를 넣어주세요>','곰탕'),(94,'1223cb0d0d844aa6ae51cc4f679e3a0a','점심','2024-01-04','<실제 이미지를 넣어주세요>','김치전'),(95,'1223cb0d0d844aa6ae51cc4f679e3a0a','저녁','2024-01-04','<실제 이미지를 넣어주세요>','쌀밥'),(96,'1223cb0d0d844aa6ae51cc4f679e3a0a','저녁','2024-01-04','<실제 이미지를 넣어주세요>','곰탕'),(97,'1223cb0d0d844aa6ae51cc4f679e3a0a','저녁','2024-01-04','<실제 이미지를 넣어주세요>','김치전');
/*!40000 ALTER TABLE `usermeal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermealevaluation`
--

DROP TABLE IF EXISTS `usermealevaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermealevaluation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` char(32) NOT NULL,
  `meal_date` date DEFAULT NULL,
  `sum_carb` double DEFAULT NULL,
  `sum_sugar` double DEFAULT NULL,
  `sum_protein` double DEFAULT NULL,
  `sum_fat` double DEFAULT NULL,
  `meal_evaluation` longtext,
  `sum_kcal` double DEFAULT NULL,
  `sum_col` double DEFAULT NULL,
  `sum_nat` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermealevaluation`
--

LOCK TABLES `usermealevaluation` WRITE;
/*!40000 ALTER TABLE `usermealevaluation` DISABLE KEYS */;
INSERT INTO `usermealevaluation` VALUES (10,'950cfbad7a9e43c0a11af905fe67dafb','2023-12-29',0,0,0,0,'bad',0,NULL,NULL),(13,'950cfbad7a9e43c0a11af905fe67dafb','2024-01-03',45.05,0,3.52,0.33,'bad',205.03999999999996,0,254.68),(14,'1223cb0d0d844aa6ae51cc4f679e3a0a','2024-01-04',363.84,0,106.56000000000002,55.11,'bad',2405.85,508.98,4675.92),(15,'1223cb0d0d844aa6ae51cc4f679e3a0a','2024-01-03',500,0,300,50,'perfect',1000,10,300),(16,'1223cb0d0d844aa6ae51cc4f679e3a0a','2024-01-02',500,0,300,50,'not bad',1000,10,300),(17,'1223cb0d0d844aa6ae51cc4f679e3a0a','2024-01-01',500,0,300,50,'very good',1000,10,300),(18,'1223cb0d0d844aa6ae51cc4f679e3a0a','2023-12-31',500,0,300,50,'good',1000,10,300),(19,'1223cb0d0d844aa6ae51cc4f679e3a0a','2023-12-30',500,0,300,50,'bad',1000,10,300),(20,'1223cb0d0d844aa6ae51cc4f679e3a0a','2023-12-29',500,0,300,50,'perfect',1000,10,300),(21,'1223cb0d0d844aa6ae51cc4f679e3a0a','2023-12-28',500,0,300,50,'good',1000,10,300);
/*!40000 ALTER TABLE `usermealevaluation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-05  0:08:56

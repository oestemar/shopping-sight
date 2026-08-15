-- MySQL dump 10.13  Distrib 9.6.0, for Win64 (x86_64)
--
-- Host: localhost    Database: shoppingdb1
-- ------------------------------------------------------
-- Server version	9.6.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '6e146740-25bb-11f1-9dbb-ec21e5baa540:1-1036';

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'demo@demoadmin.job','scrypt:32768:8:1$6iT2HXvoza5ipbsR$2beb1af3ef89cf0bc3114c462781d14ee5a53e13e15bd29e02344e641e6bf4c605347fd5cf0e38e110bec6bac0f511dceaec37a8c02145680064a67a71e23441',1,NULL),(2,'north@admin.job','scrypt:32768:8:1$YU8CUgGsnGk5EXJn$52534a2c863efc8959eac867a2fecf23fe828a921b3871cb3ab85d80294b6a66ac5e7e1ff2dc575c6d9d89df3b236e64ba1345c1b1e13cb2c9bb4547a9695e4e',2,NULL),(3,'south@super.job','scrypt:32768:8:1$5mZt7BzwRX6HVZtr$3cdce2b1fd4f2cacd303a56a19d5aec5e686b77741aa9e17215c8bf36f64ed585df703a1fb132f0a24e01bd84ca271984c8aa22e51e42c7880c6426d40eb6b23',3,NULL);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('f98adad7fa66');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price_at_added` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'野菜',1),(2,'肉',2),(3,'飲料',3),(4,'お菓子',4);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_images`
--

DROP TABLE IF EXISTS `category_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `category_images_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_images`
--

LOCK TABLES `category_images` WRITE;
/*!40000 ALTER TABLE `category_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `category_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price_at_order` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,41,1,2,150),(2,41,3,1,980),(3,42,8,2,120),(4,45,6,5,110),(5,46,1,3,150),(6,46,2,5,120),(7,47,2,3,120),(8,47,4,2,380),(9,48,6,5,110);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `total_amount` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,0,'processing','2026-07-14 09:01:58','stripe',NULL),(2,1,650,'canceled','2026-07-14 09:02:23','stripe',NULL),(3,1,510,'processing','2026-07-14 09:07:57','stripe',NULL),(4,1,490,'paid','2026-07-14 09:11:03','stripe',NULL),(5,1,370,'processing','2026-07-15 08:30:56','paspo',NULL),(6,1,4080,'processing','2026-07-15 08:46:16','paspo',NULL),(7,1,810,'processing','2026-07-15 08:49:01','paspo',NULL),(8,1,4080,'processing','2026-07-15 09:03:32','paspo',NULL),(9,1,810,'paid','2026-07-15 09:44:41','stripe',NULL),(10,1,810,'processing','2026-07-15 09:58:53','paspo',NULL),(11,1,540,'processing','2026-07-15 10:16:25','paspo',NULL),(12,1,480,'processing','2026-07-15 11:17:50','stripe',NULL),(13,1,460,'processing','2026-07-15 11:18:51','stripe',NULL),(14,1,600,'paid','2026-07-15 11:26:30','stripe',NULL),(15,1,580,'processing','2026-07-15 11:33:22','paspo',NULL),(16,1,1410,'processing','2026-07-16 07:14:32','qr',NULL),(17,1,1410,'processing','2026-07-16 07:23:49','paspo',NULL),(18,1,360,'processing','2026-07-16 07:25:01','paspo',NULL),(19,1,360,'processing','2026-07-16 07:36:40','paspo',NULL),(20,1,580,'processing','2026-07-16 07:43:25','paspo',NULL),(21,1,580,'processing','2026-07-16 07:46:05','qr',NULL),(22,1,580,'processing','2026-07-16 07:47:57','paspo',NULL),(23,1,2280,'processing','2026-07-16 07:48:49','paspo',NULL),(24,1,2280,'processing','2026-07-16 07:49:03','qr',NULL),(25,1,2280,'processing','2026-07-16 07:51:54','paspo',NULL),(26,1,630,'processing','2026-07-16 08:16:33','paspo',NULL),(27,1,760,'processing','2026-07-16 09:23:07','qr',NULL),(28,1,360,'processing','2026-07-16 09:26:26','paspo',NULL),(29,1,600,'processing','2026-07-16 09:38:36','paspo',NULL),(30,1,360,'processing','2026-07-16 09:43:37','paspo',NULL),(31,1,750,'processing','2026-07-16 09:44:04','qr',NULL),(32,1,790,'paid','2026-07-16 09:44:45','stripe',NULL),(33,1,1630,'processing','2026-07-16 12:10:47','paspo',NULL),(34,1,480,'processing','2026-07-16 12:24:56','paspo',NULL),(35,1,380,'processing','2026-07-16 12:32:33','paspo',NULL),(36,1,1360,'processing','2026-07-16 12:35:35','paspo',NULL),(37,1,760,'processing','2026-07-16 13:00:15','paspo',NULL),(38,1,340,'paid','2026-07-16 13:21:54','paspo',NULL),(39,1,1290,'paid','2026-07-17 06:50:59','qr',NULL),(41,1,1280,'paid','2026-07-17 07:42:09','paspo',NULL),(42,1,240,'paid','2026-07-17 07:42:31','qr',NULL),(43,1,360,'paid','2026-07-17 07:42:56','stripe',NULL),(44,1,1250,'paid','2026-07-17 09:55:28','stripe',NULL),(45,1,550,'paid','2026-07-17 10:00:14','stripe',NULL),(46,1,1050,'paid','2026-07-18 14:58:42','qr',NULL),(47,1,1120,'paid','2026-07-22 11:30:12','qr',NULL),(48,1,550,'paid','2026-07-23 15:01:18','paspo',NULL);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (1,1,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/d9690915-c8e3-41d0-b8fc-a90ffda2b725.png',0),(2,2,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/67f00ff8-0298-4f2d-a0ee-881b83ba1798.png',0),(3,3,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/be1d8083-1ce5-4489-a860-bdd93cc1407b.png',0),(4,4,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/47128117-0616-4756-9bc5-4f56e303f7c3.png',0),(5,5,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/7a3a5be0-c19a-49ad-a439-b8932a4faacd.png',0),(6,6,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/459bdb86-ea6c-4041-a581-df60ab5080ce.png',0),(7,7,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/c98a9d78-7c76-4589-ada4-652b76b7f61b.png',0),(8,8,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/d43eb531-d2b9-4a91-b0e7-557690aa9fa1.png',0),(9,1,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/3ca4c91e-3b90-4b79-8681-094811651980.png',1),(10,2,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/e51e5b32-0efe-4696-a809-0d640e200cc0.png',0),(11,3,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/66da4928-6938-4b56-bb38-306b90c21cf7.png',0),(12,4,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/f409df2a-04e5-4b1b-9803-85e804289341.png',0),(13,5,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/14d58d48-ed47-465a-bb0a-66f4e62225a3.png',0),(14,6,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/0f2d67bf-26a2-4a4e-be05-e76774101600.png',0),(15,7,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/9777553b-c831-4a31-bc78-f4f16ad9bb7c.png',0),(16,8,'https://kujwcaoueamqmkbmfrix.supabase.co/storage/v1/object/public/products_test/2c5ec5ae-ab6e-4f13-accf-94ddacc5750f.png',0);
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` int NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `category_id` int NOT NULL,
  `stock` int NOT NULL,
  `sku` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `brand` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int NOT NULL,
  `spec_json` json DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'トマト',150,'新鮮なトマトです',1,100,'SKU001','農家直送',1,NULL,NULL,'2026-08-01 11:40:50'),(2,'じゃがいも',120,'北海道産のじゃがいも',1,100,'SKU002','農家直送',1,NULL,NULL,'2026-08-01 11:01:56'),(3,'牛肉ロース',980,'焼肉に最適な国産牛ロース',2,50,'SKU003','国産牛',1,NULL,NULL,'2026-08-01 11:02:16'),(4,'鶏もも肉',380,'唐揚げに最適な鶏もも肉',2,80,'SKU004','国産鶏',1,NULL,NULL,'2026-08-01 11:02:45'),(5,'コーラ',120,'炭酸飲料の定番',3,200,'SKU005','Coca-Cola',1,NULL,NULL,'2026-08-01 11:03:07'),(6,'緑茶',110,'国産茶葉使用',3,150,'SKU006','伊藤園',1,NULL,NULL,'2026-08-01 11:03:29'),(7,'ポテトチップス',150,'うすしお味',4,300,'SKU007','カルビー',1,NULL,NULL,'2026-08-01 11:03:46'),(8,'チョコレート',120,'ミルクチョコレート',4,200,'SKU008','明治',1,NULL,NULL,'2026-08-01 11:04:05');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'東西 南北','we@sample.com','we','北海道札幌市','111-1111-1111','2026-07-10 11:44:49');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-04 10:17:21

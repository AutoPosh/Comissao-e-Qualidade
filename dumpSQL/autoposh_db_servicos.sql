CREATE DATABASE  IF NOT EXISTS `autoposh_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `autoposh_db`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 192.168.0.34    Database: autoposh_db
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `servicos`
--

DROP TABLE IF EXISTS `servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicos` (
  `id_servico` int NOT NULL AUTO_INCREMENT,
  `numero_os` int NOT NULL,
  `id_colaborador_1` varchar(200) NOT NULL,
  `id_colaborador_2` varchar(200) DEFAULT NULL,
  `id_colaborador_3` varchar(200) DEFAULT NULL,
  `descricao` varchar(100) DEFAULT NULL,
  `etapa_servico` int NOT NULL,
  `servico` varchar(255) NOT NULL,
  `status_servico` varchar(50) NOT NULL,
  `tempo_inicio` datetime DEFAULT NULL,
  `tempo_fim` datetime DEFAULT NULL,
  `tempo_pausa` datetime DEFAULT NULL,
  `tempo_reinicio` datetime DEFAULT NULL,
  `valor_pausa` time DEFAULT NULL,
  `roxo_qtd` varchar(5) DEFAULT NULL,
  `roseo_qtd` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id_servico`),
  KEY `servicos_ibfk_1_idx` (`id_colaborador_1`),
  KEY `servicos_ibfk_2_idx` (`id_colaborador_2`),
  KEY `servicos_ibfk_3_idx` (`id_colaborador_3`),
  KEY `idx_numero_os` (`numero_os`),
  KEY `idx_id_colaborador_1` (`id_colaborador_1`),
  KEY `idx_id_colaborador_2` (`id_colaborador_2`),
  KEY `idx_id_colaborador_3` (`id_colaborador_3`),
  KEY `idx_etapa_servico` (`etapa_servico`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos`
--

LOCK TABLES `servicos` WRITE;
/*!40000 ALTER TABLE `servicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-12 14:03:08

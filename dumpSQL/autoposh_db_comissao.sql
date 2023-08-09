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
-- Table structure for table `comissao`
--

DROP TABLE IF EXISTS `comissao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comissao` (
  `id_comissao` int NOT NULL AUTO_INCREMENT,
  `numero_os` int NOT NULL,
  `etapa_servico` int NOT NULL,
  `status_avaliacao` varchar(45) DEFAULT NULL,
  `id_colaborador_1` varchar(200) DEFAULT NULL,
  `id_colaborador_2` varchar(200) DEFAULT NULL,
  `id_colaborador_3` varchar(200) DEFAULT NULL,
  `porc_colab1` int NOT NULL,
  `porc_colab2` int NOT NULL,
  `porc_colab3` int NOT NULL,
  `controle_ponto` int DEFAULT NULL,
  `agenda_rotina` int DEFAULT NULL,
  `nota_avaliacao` int DEFAULT NULL,
  `comissao_colab_1` decimal(10,2) DEFAULT NULL,
  `comissao_colab_2` decimal(10,2) DEFAULT NULL,
  `comissao_colab_3` decimal(10,2) DEFAULT NULL,
  `premio_1_colab_1` decimal(10,2) DEFAULT NULL,
  `premio_2_colab_1` decimal(10,2) DEFAULT NULL,
  `premio_1_colab_2` decimal(10,2) DEFAULT NULL,
  `premio_2_colab_2` decimal(10,2) DEFAULT NULL,
  `premio_1_colab_3` decimal(10,2) DEFAULT NULL,
  `premio_2_colab_3` decimal(10,2) DEFAULT NULL,
  `tempo_inicio` datetime DEFAULT NULL,
  `tempo_fim` datetime DEFAULT NULL,
  PRIMARY KEY (`id_comissao`),
  KEY `id_colaborador_1` (`id_colaborador_1`),
  KEY `id_colaborador_2` (`id_colaborador_2`),
  KEY `id_colaborador_3` (`id_colaborador_3`),
  KEY `comissao_ibfk_1` (`numero_os`),
  KEY `comissao_ibfk_5` (`etapa_servico`),
  CONSTRAINT `comissao_ibfk_1` FOREIGN KEY (`numero_os`) REFERENCES `servicos` (`numero_os`),
  CONSTRAINT `comissao_ibfk_2` FOREIGN KEY (`id_colaborador_1`) REFERENCES `servicos` (`id_colaborador_1`),
  CONSTRAINT `comissao_ibfk_3` FOREIGN KEY (`id_colaborador_2`) REFERENCES `servicos` (`id_colaborador_2`),
  CONSTRAINT `comissao_ibfk_4` FOREIGN KEY (`id_colaborador_3`) REFERENCES `servicos` (`id_colaborador_3`),
  CONSTRAINT `comissao_ibfk_5` FOREIGN KEY (`etapa_servico`) REFERENCES `servicos` (`etapa_servico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissao`
--

LOCK TABLES `comissao` WRITE;
/*!40000 ALTER TABLE `comissao` DISABLE KEYS */;
/*!40000 ALTER TABLE `comissao` ENABLE KEYS */;
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

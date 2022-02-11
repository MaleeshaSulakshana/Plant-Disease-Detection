-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 20, 2021 at 08:24 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `plantdisease`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` varchar(30) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `psw` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `psw`) VALUES
('12345', 'Maleesha Sulakshana', 'mpmsulakshana@gmail.com', '1d2f80ed088e87150fa670b6f3214822'),
('Ravidu881416', 'Ravidu', 'ravidunayanajith98@gmail.com', 'ea7fa0fa15a8483e42778336899840c5');

-- --------------------------------------------------------

--
-- Table structure for table `diseases`
--

CREATE TABLE `diseases` (
  `id` varchar(30) NOT NULL,
  `plant_name` varchar(50) NOT NULL,
  `disease_name` varchar(50) NOT NULL,
  `disease_details` varchar(400) NOT NULL,
  `treatment_details` varchar(400) NOT NULL,
  `thumbnail` varchar(100) NOT NULL,
  `image1` varchar(100) NOT NULL,
  `image2` varchar(100) NOT NULL,
  `image3` varchar(100) NOT NULL,
  `image4` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `diseases`
--

INSERT INTO `diseases` (`id`, `plant_name`, `disease_name`, `disease_details`, `treatment_details`, `thumbnail`, `image1`, `image2`, `image3`, `image4`) VALUES
('AppleAppleScab965155', 'Apple', 'Apple Scab', 'Apple Scab', 'Apple scab', '0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417_90deg.JPG', '0a769a71-052a-4f19-a4d8-b0f0cb75541c___FREC_Scab 3165.JPG', 'None', 'None', 'None'),
('AppleBlackRot446029', 'Apple', 'Black Rot', 'Black Rot', 'Black Rot', '0b8dabb7-5f1b-4fdc-b3fa-30b289707b90___JR_FrgE.S 3047_90deg.JPG', 'None', 'None', 'None', 'None'),
('GrapeBlackRot203557', 'Grape', 'Black Rot', 'Black Rot', 'Black Rot', '0aff8add-93ad-4099-97ae-23515744e620___FAM_B.Rot 0748_flipLR.JPG', 'None', 'None', 'None', 'None'),
('PeachBacterialSpot646584', 'Peach', 'Bacterial Spot', 'Bacterial Spot', 'Bacterial Spot', '0ddfb4d4-0310-4ea0-b74b-415ee6921105___Rutg._Bact.S 1641.JPG', '0eb8a77a-fe2b-43f8-804c-d958c01ba0c0___Rutg._Bact.S 1188.JPG', '1a456b62-2c4b-4f09-80f4-78b474348ca7___Rutg._Bact.S 2277.JPG', 'None', 'None'),
('PepperBellBacterialSpot799632', 'Pepper Bell', 'Bacterial Spot', 'Bacterial Spot', 'Bacterial Spot', '0abffc81-6be8-4b17-a83c-4d2830e30382___JR_B.Spot 9076.JPG', '0c2392f6-3e69-4baf-b9f3-197623f6631a___JR_B.Spot 3176.JPG', 'None', 'None', 'None'),
('PotatoEarlyBlight333579', 'Potato', 'Early Blight', 'Early Blight', 'Early Blight for potato', '0d9dbf50-53a9-42b2-8b29-0360fb7dbd98___RS_Early.B 6692.JPG', '0d2325ff-4e3e-44bf-9614-e5ad6c23fc16___RS_Early.B 6797.JPG', 'None', 'None', 'None'),
('TomatoBacterialSpot757455', 'Tomato', 'Bacterial Spot', 'Bacterial Spot', 'Bacterial Spot', '00a7c269-3476-4d25-b744-44d6353cd921___GCREC_Bact.Sp 5807.JPG', '0a22f50a-5f25-4cf6-816b-76cae94b7f30___GCREC_Bact.Sp 6103.JPG', '0a1655ed-797c-4d1d-ba35-dc255d68a2ee___GCREC_Bact.Sp 3560.JPG', '0ce4dee0-2d0c-4c25-a9b2-4abc5f9083db___GCREC_Bact.Sp 3708.JPG', 'None');

-- --------------------------------------------------------

--
-- Table structure for table `prediction_count`
--

CREATE TABLE `prediction_count` (
  `date` date NOT NULL,
  `count` int(11) NOT NULL,
  `accuracy` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `prediction_count`
--

INSERT INTO `prediction_count` (`date`, `count`, `accuracy`) VALUES
('2021-06-06', 42, 0),
('2021-06-05', 2, 0),
('2021-06-04', 13, 0),
('2021-06-03', 5, 0),
('2021-06-02', 75, 0),
('2021-06-01', 20, 0),
('2021-05-31', 10, 0),
('2021-05-30', 20, 0),
('2021-06-07', 10, 970),
('2021-06-08', 3, 190),
('2021-06-11', 3, 300),
('2021-06-12', 2, 200),
('2021-06-20', 1, 100);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

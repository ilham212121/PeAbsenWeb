-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 08, 2022 at 06:09 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pe_absen`
--

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

CREATE TABLE `data` (
  `nip` int(10) DEFAULT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `no_rumah` varchar(10) NOT NULL,
  `kontak` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data`
--

INSERT INTO `data` (`nip`, `nama`, `email`, `password`, `no_rumah`, `kontak`) VALUES
(NULL, 'RIzky Dwi Saputra', 'rizkyds@gmail.com', 'blabla12', '12', '08921423532'),
(NULL, 'm ilham fs', 'ilhamdariatas@gmail.com', 'bla123', '123', '089214322351'),
(NULL, 'm ilham fs', 'ilhamdariat@gmail.com', 'bla123', '123', '089214322351'),
(19090107, 'Rizky Dwi Saputra', 'rizkydwisaputrar1@gmail.com', 'blabla12', '12', '08953605107');

-- --------------------------------------------------------

--
-- Table structure for table `dataabsen`
--

CREATE TABLE `dataabsen` (
  `nip` varchar(10) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `waktu` date DEFAULT NULL,
  `lokasi` geometry DEFAULT NULL,
  `foto` varchar(100) NOT NULL,
  `sidik jari` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

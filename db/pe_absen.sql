-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 18, 2022 at 08:07 AM
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
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `nip` int(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `alamat` varchar(1000) NOT NULL,
  `no_hp` varchar(13) NOT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`nip`, `nama`, `email`, `password`, `alamat`, `no_hp`, `role`) VALUES
(19090101, 'M Ilham Fajar S', 'ilham@gmail.com', 'pbkdf2:sha256:260000$wZS9dWu7iGiaoHg4$8ba676fd6c10fa74eff20866639e183ff293b879b31cd4111ce62c87c45a54', 'jl sriti gang 3 no 4', '0895365912452', 'admin'),
(19090107, 'Rizky Dwi Saputra', 'rizkydwisaputrar1@gmail.com', 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'jl balamoa selatan rt 03/01', '08953605107', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `dataabsen`
--

CREATE TABLE `dataabsen` (
  `id` int(11) NOT NULL,
  `nip` varchar(10) DEFAULT NULL,
  `latitude` varchar(1000) DEFAULT NULL,
  `longitude` varchar(1000) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `tanggal` date DEFAULT NULL,
  `waktu` time DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dataabsen`
--

INSERT INTO `dataabsen` (`id`, `nip`, `latitude`, `longitude`, `foto`, `tanggal`, `waktu`, `status`) VALUES
(1, '220712001', '', '', '2207120012022-7-14934AM.jpg', '2022-07-14', '09:34:00', 'tepat waktu'),
(2, '220712001', '', '', '2207120012022-7-151126AM.jpg', '2022-07-15', '11:26:00', 'telat'),
(3, '220712001', '', '', '2207120012022-7-1676AM.jpg', '2022-07-16', '07:06:00', 'tepat waktu'),
(4, '220712001', '', '', '2207120012022-7-1798AM.jpg', '2022-07-17', '09:08:00', 'telat'),
(5, '220712002', '', '', '2207120022022-7-1824PM.jpg', '2022-07-18', '14:04:00', 'tepat waktu'),
(6, '220712001', '', '', '2207120012022-7-1826PM.jpg', '2022-07-18', '14:06:00', 'tepat waktu'),
(7, '220712001', '', '', '2207120012022-7-20225PM.jpg', '2022-07-20', '14:25:00', 'telat'),
(8, '220712001', '', '', '2207120012022-7-21228PM.jpg', '2022-07-21', '14:28:00', 'telat'),
(9, '220712001', '-9.123124', '109.23132', '2207120012022-7-22959AM.jpg', '2022-07-22', '09:59:00', 'telat');

-- --------------------------------------------------------

--
-- Table structure for table `datapulang`
--

CREATE TABLE `datapulang` (
  `id` int(11) NOT NULL,
  `nip` varchar(100) NOT NULL,
  `latitude` varchar(1000) NOT NULL,
  `longitude` varchar(1000) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `tanggal` date NOT NULL,
  `waktu` time NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `datapulang`
--

INSERT INTO `datapulang` (`id`, `nip`, `latitude`, `longitude`, `foto`, `tanggal`, `waktu`, `status`) VALUES
(1, '220712001', '', '', '2207120022022-7-1824PM.jpg', '2022-07-16', '00:00:00', 'terlalu cepat'),
(2, '220712002', '', '', 'IMG20220712110028.jpg', '2022-07-16', '00:00:00', 'terlalu cepat');

-- --------------------------------------------------------

--
-- Table structure for table `hrd`
--

CREATE TABLE `hrd` (
  `nip` varchar(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `pswd` varchar(1000) NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_hp` varchar(15) NOT NULL,
  `alamat` varchar(1000) NOT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'HRD'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hrd`
--

INSERT INTO `hrd` (`nip`, `nama`, `pswd`, `email`, `no_hp`, `alamat`, `role`) VALUES
('2208001', 'boss', 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'hrd@rsi.com', '08564006310', 'jln milyader no 1', 'HRD');

-- --------------------------------------------------------

--
-- Table structure for table `karu`
--

CREATE TABLE `karu` (
  `nip` varchar(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `pswd` varchar(1000) NOT NULL,
  `penempatan` varchar(1000) NOT NULL,
  `email` varchar(1000) NOT NULL,
  `no_hp` varchar(15) NOT NULL,
  `alamat` varchar(1000) NOT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'k_ruang'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `karu`
--

INSERT INTO `karu` (`nip`, `nama`, `pswd`, `penempatan`, `email`, `no_hp`, `alamat`, `role`) VALUES
('2209001', 'kepala ruang #1', 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'dahlia', 'karu@gmail.com', '08921321485', 'jl jalak barat gang 3', 'karu');

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `nip` varchar(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `posisi` varchar(100) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `ttl` date NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_hp` varchar(15) NOT NULL,
  `alamat` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`nip`, `nama`, `posisi`, `gender`, `ttl`, `email`, `no_hp`, `alamat`) VALUES
('220712001', 'Bambang', 'Perawat', 'L', '1992-08-03', 'banbangkeuh@gmail.com', '0895360510704', 'jl jalak barat gang 3'),
('220712002', 'farid', 'dokter', 'L', '1993-07-11', 'halodok@gmail.com', '089213212135', 'jl kedungbanteng kidul');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `nip` int(100) NOT NULL,
  `pswd` varchar(1000) NOT NULL,
  `role` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`nip`, `pswd`, `role`) VALUES
(2208001, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'HRD'),
(2209001, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'karu'),
(19090101, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'admin'),
(19090107, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'admin'),
(220712001, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'karyawan'),
(220712002, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'karyawan');

-- --------------------------------------------------------

--
-- Table structure for table `shift`
--

CREATE TABLE `shift` (
  `shift` varchar(10) NOT NULL,
  `nip` varchar(100) NOT NULL,
  `ruangan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shift`
--

INSERT INTO `shift` (`shift`, `nip`, `ruangan`) VALUES
('pagi', '220712001', 'dahlia');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`nip`);

--
-- Indexes for table `dataabsen`
--
ALTER TABLE `dataabsen`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `datapulang`
--
ALTER TABLE `datapulang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hrd`
--
ALTER TABLE `hrd`
  ADD PRIMARY KEY (`nip`);

--
-- Indexes for table `karu`
--
ALTER TABLE `karu`
  ADD PRIMARY KEY (`nip`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`nip`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`nip`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dataabsen`
--
ALTER TABLE `dataabsen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `datapulang`
--
ALTER TABLE `datapulang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

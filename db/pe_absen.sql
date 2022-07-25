-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 23, 2022 at 06:40 AM
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
  `gender` varchar(1) NOT NULL,
  `ttl` date NOT NULL,
  `alamat` varchar(1000) NOT NULL,
  `no_hp` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`nip`, `nama`, `email`, `gender`, `ttl`, `alamat`, `no_hp`) VALUES
(19090101, 'M Ilham Fajar S', 'ilham@gmail.com', 'L', '2001-08-03', 'jl sriti gang 3 no 4', '0895365912452'),
(19090107, 'Rizky Dwi Saputra', 'rizkydwisaputrar1@gmail.com', 'L', '2000-08-03', 'jl balamoa selatan rt 03/01', '08953605107');

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
(1, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2022-07-17', '07:04:00', 'tepat waktu'),
(2, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2022-07-18', '07:19:00', 'telat'),
(3, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(4, '220712001', '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-21', '08:51:00', 'telat'),
(5, '220712001', '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-07-26', '07:07:00', 'tepat waktu'),
(6, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-24', '11:59:00', 'telat'),
(7, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2022-07-23', '07:04:00', 'tepat waktu'),
(8, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2022-07-25', '07:19:00', 'telat'),
(9, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-27', '11:59:00', 'telat'),
(10, '220712001', '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-28', '08:51:00', 'telat'),
(11, '220712001', '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-06-29', '07:07:00', 'tepat waktu'),
(12, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2021-07-30', '11:59:00', 'telat'),
(13, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2021-08-17', '07:04:00', 'tepat waktu'),
(14, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2021-12-18', '07:19:00', 'telat'),
(15, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2021-11-20', '11:59:00', 'telat'),
(16, '220712001', '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-21', '08:51:00', 'telat'),
(17, '220712001', '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-07-26', '07:07:00', 'tepat waktu'),
(18, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(19, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2022-07-17', '07:04:00', 'tepat waktu'),
(20, '220712001', '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2022-07-18', '07:19:00', 'telat'),
(21, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(22, '220712001', '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-21', '08:51:00', 'telat'),
(23, '220712001', '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-07-26', '07:07:00', 'tepat waktu'),
(24, '220712001', '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(25, '220712001', '-6.8762537', '109.1290818', '2207120012022-7-2914PM.jpg', '2022-07-29', '13:04:00', 'telat'),
(26, '220712001', '-6.8762543', '109.1290671', '2207120012022-7-2216PM.jpg', '2022-07-22', '13:06:00', 'telat'),
(27, '220712001', '-6.8762276', '109.1290969', '2207120012022-7-167257.jpg', '2022-07-16', '07:25:07', 'telat'),
(28, '220712001', '-6.8762594', '109.1290755', '2207120012022-7-30135820.jpg', '2022-07-30', '13:58:20', 'tepat waktu');

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
(2, '220712002', '', '', 'IMG20220712110028.jpg', '2022-07-16', '00:00:00', 'terlalu cepat'),
(3, '220712001', '-6.8763278', '109.1290271', 'storage_emulated_0_Android_data_com.rizky.ilham.pe_absen_files_Pictures_JPEG_20220722_105301_8278989', '2022-07-22', '00:00:00', 'terlalu cepat'),
(4, '220712001', '-6.8762543', '109.1290671', 'storage_emulated_0_Android_data_com.rizky.ilham.pe_absen_files_Pictures_JPEG_20220722_132009_3099783', '2022-07-29', '00:00:00', 'terlalu cepat');

-- --------------------------------------------------------

--
-- Table structure for table `hrd`
--

CREATE TABLE `hrd` (
  `nip` varchar(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `ttl` date DEFAULT NULL,
  `no_hp` varchar(15) NOT NULL,
  `alamat` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hrd`
--

INSERT INTO `hrd` (`nip`, `nama`, `email`, `gender`, `ttl`, `no_hp`, `alamat`) VALUES
('2208001', 'boss', 'hrd@rsi.com', 'L', '1993-07-11', '08564006310', 'jln milyader no 1');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id` int(11) NOT NULL,
  `nip` varchar(100) NOT NULL,
  `shift` varchar(10) NOT NULL,
  `ruangan` varchar(100) NOT NULL,
  `bulan` varchar(2) NOT NULL,
  `from_tgl` varchar(2) NOT NULL,
  `to_tgl` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id`, `nip`, `shift`, `ruangan`, `bulan`, `from_tgl`, `to_tgl`) VALUES
(1, '220712001', 'pagi', 'dahlia', '7', '', ''),
(2, '220712002', 'malam', 'melati', '7', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal_khusus`
--

CREATE TABLE `jadwal_khusus` (
  `id` int(11) NOT NULL,
  `nip` int(10) NOT NULL,
  `shift` varchar(100) NOT NULL,
  `ruangan` varchar(100) NOT NULL,
  `tanggal` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `jadwal_khusus`
--

INSERT INTO `jadwal_khusus` (`id`, `nip`, `shift`, `ruangan`, `tanggal`) VALUES
(1, 220712001, 'siang', 'dahlia', '2022-07-30');

-- --------------------------------------------------------

--
-- Table structure for table `karu`
--

CREATE TABLE `karu` (
  `nip` varchar(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `penempatan` varchar(1000) NOT NULL,
  `email` varchar(1000) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `ttl` date DEFAULT NULL,
  `no_hp` varchar(15) NOT NULL,
  `alamat` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `karu`
--

INSERT INTO `karu` (`nip`, `nama`, `penempatan`, `email`, `gender`, `ttl`, `no_hp`, `alamat`) VALUES
('2209001', 'dea', 'dahlia', 'karu@gmail.com', 'P', '1992-08-03', '08921321485', 'jl jalak barat gang 3');

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
('220712001', 'Bambang', 'Perawat', 'L', '1992-08-03', 'bambanggg@gmail.com', '0895360510704', 'jl jalak barat gang 3'),
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
(220712001, 'pbkdf2:sha256:260000$kFhghJliwhsmJ5UU$394a8dac83163d79dd889a4b70a47d346d2f9cdb87558b0a20d4345d3eb465f0', 'karyawan'),
(220712002, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'karyawan');

-- --------------------------------------------------------

--
-- Table structure for table `shift`
--

CREATE TABLE `shift` (
  `shift` varchar(10) NOT NULL,
  `berangkat` time NOT NULL,
  `pulang` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shift`
--

INSERT INTO `shift` (`shift`, `berangkat`, `pulang`) VALUES
('malam', '21:00:00', '05:00:00'),
('middle', '10:00:00', '17:00:00'),
('pagi', '07:00:00', '14:00:00'),
('siang', '14:00:00', '17:00:00');

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
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jadwal_khusus`
--
ALTER TABLE `jadwal_khusus`
  ADD PRIMARY KEY (`id`);

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
-- Indexes for table `shift`
--
ALTER TABLE `shift`
  ADD PRIMARY KEY (`shift`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dataabsen`
--
ALTER TABLE `dataabsen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `datapulang`
--
ALTER TABLE `datapulang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `jadwal_khusus`
--
ALTER TABLE `jadwal_khusus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2023 at 07:08 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `e_attandance`
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
  `no_hp` varchar(13) NOT NULL,
  `deleted_at` date DEFAULT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`nip`, `nama`, `email`, `gender`, `ttl`, `alamat`, `no_hp`, `deleted_at`, `created_at`, `updated_at`) VALUES
(19090101, 'M Ilham Fajar Sidiq', 'ilham@gmail.com', 'L', '2001-08-03', 'blabla', '082123', NULL, '2021-08-25', '2022-10-01'),
(19090107, 'Ilham Fajar', 'rizkydwisaputra@gmail.com', 'L', '2000-08-09', 'jl oemuda dewjndkjewkjbjk', '0832432876788', NULL, '2022-08-27', '2022-10-01'),
(2147483647, 'coba', 'coba1@gmail.com', 'L', '2023-07-12', 'dfdf', '454', '0000-00-00', '2023-07-29', '2023-07-29');

-- --------------------------------------------------------

--
-- Table structure for table `dataabsen`
--

CREATE TABLE `dataabsen` (
  `id` int(11) NOT NULL,
  `nip` int(11) DEFAULT NULL,
  `latitude` varchar(1000) DEFAULT NULL,
  `longitude` varchar(1000) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `tanggal` date DEFAULT NULL,
  `waktu` time DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dataabsen`
--

INSERT INTO `dataabsen` (`id`, `nip`, `latitude`, `longitude`, `foto`, `tanggal`, `waktu`, `status`) VALUES
(1, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2022-07-17', '07:04:00', 'tepat waktu'),
(2, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2022-07-18', '07:19:00', 'telat'),
(3, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(4, 220712001, '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-21', '08:51:00', 'telat'),
(5, 220712001, '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-07-26', '07:07:00', 'tepat waktu'),
(6, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-24', '11:59:00', 'telat'),
(7, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2022-07-23', '07:04:00', 'tepat waktu'),
(8, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2022-07-25', '07:19:00', 'telat'),
(9, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-27', '11:59:00', 'telat'),
(10, 220712001, '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-28', '08:51:00', 'telat'),
(11, 220712001, '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-06-29', '07:07:00', 'tepat waktu'),
(12, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2021-07-30', '11:59:00', 'telat'),
(13, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2021-08-17', '07:04:00', 'tepat waktu'),
(14, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2021-12-18', '07:19:00', 'telat'),
(15, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2021-11-20', '11:59:00', 'telat'),
(16, 220712001, '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-21', '08:51:00', 'telat'),
(17, 220712001, '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-07-26', '07:07:00', 'tepat waktu'),
(18, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(19, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-1774AM.jpg', '2022-07-17', '07:04:00', 'tepat waktu'),
(20, 220712001, '-6.8761117', '109.1290823', '2207120012022-7-18719AM.jpg', '2022-07-18', '07:19:00', 'telat'),
(21, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(22, 220712001, '-6.8761844', '109.1291096', '2207120012022-7-21851AM.jpg', '2022-07-21', '08:51:00', 'telat'),
(23, 220712001, '-6.8761763', '109.1290976', '2207120012022-7-2677AM.jpg', '2022-07-26', '07:07:00', 'tepat waktu'),
(24, 220712001, '-6.8751565', '109.1288559', '2207120012022-7-201159AM.jpg', '2022-07-20', '11:59:00', 'telat'),
(25, 220712001, '-6.8762537', '109.1290818', '2207120012022-7-2914PM.jpg', '2022-07-29', '13:04:00', 'telat'),
(26, 220712001, '-6.8762543', '109.1290671', '2207120012022-7-2216PM.jpg', '2022-07-22', '13:06:00', 'telat'),
(27, 220712001, '-6.8762276', '109.1290969', '2207120012022-7-167257.jpg', '2022-07-16', '07:25:07', 'telat'),
(28, 220712001, '-6.8762594', '109.1290755', '2207120012022-7-30135820.jpg', '2022-07-30', '13:58:20', 'tepat waktu'),
(29, 220712001, '0.0', '0.0', '2022-12-28-220712001.jpg', '2022-12-28', '14:14:15', 'telat'),
(30, 220712001, '0.0', '0.0', '2022-12-29-220712001.jpg', '2022-12-29', '14:01:40', 'telat'),
(31, 220712001, '0.0', '0.0', '2022-12-30-220712001.jpg', '2022-12-30', '14:59:10', 'telat'),
(32, 220712001, '0.0', '0.0', '2023-1-4-220712001.jpg', '2023-01-04', '11:57:15', 'telat'),
(33, 220712001, '0.0', '0.0', '2023-1-10-220712001.jpg', '2023-01-10', '14:26:49', 'telat'),
(35, 220712001, '0.0', '0.0', '2023-1-20-220712001.jpg', '2023-01-20', '11:46:29', 'telat'),
(120, 220712001, '0', '0', '2207120012022-7-2677AM.jpg', '2023-03-25', '14:03:05', 'telat'),
(121, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-14', '15:54:14', 'telat'),
(122, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-15', '11:54:14', 'tepat waktu'),
(123, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-16', '10:00:00', 'telat'),
(124, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-17', '07:00:00', 'tepat waktu'),
(125, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-18', '07:30:00', 'telat'),
(126, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-19', '14:15:00', 'telat'),
(127, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-20', '22:10:00', 'telat'),
(128, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-21', '07:40:00', 'telat'),
(129, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-22', '22:16:00', 'telat'),
(130, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-23', '13:55:00', 'tepat waktu'),
(131, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-24', '13:50:00', 'tepat waktu'),
(132, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-25', '07:00:00', 'tepat waktu'),
(134, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-27', '00:00:06', 'tepat waktu'),
(135, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-28', '13:50:00', 'tepat waktu'),
(136, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-29', '14:15:00', 'telat'),
(137, 220712001, '0', '0', '2207120012022-7-2020PM.jpg\r\n', '2023-03-30', '22:10:00', 'telat'),
(138, 220712001, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-31', '07:00:00', 'tepat waktu'),
(139, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-14', '14:03:05', 'telat'),
(140, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-15', '07:00:00', 'tepat waktu'),
(141, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-16', '06:55:00', 'tepat waktu'),
(142, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-17', '14:15:00', 'telat'),
(143, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-18', '21:55:00', 'tepat waktu'),
(144, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-19', '14:56:00', 'tepat waktu'),
(145, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-20', '21:45:00', 'tepat waktu'),
(146, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-21', '06:57:00', 'tepat waktu'),
(147, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-22', '21:58:00', 'tepat waktu'),
(148, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-23', '06:59:00', 'tepat waktu'),
(149, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-24', '07:00:00', 'tepat waktu'),
(150, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-25', '07:05:00', 'telat'),
(152, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-27', '22:15:00', 'telat'),
(153, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-28', '07:54:00', 'telat'),
(154, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-29', '07:14:00', 'telat'),
(155, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-30', '07:14:00', 'telat'),
(156, 220712002, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-31', '07:19:00', 'telat'),
(157, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-14', '07:01:00', 'telat'),
(158, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-15', '07:00:00', 'tepat waktu'),
(159, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-16', '21:55:00', 'tepat waktu'),
(160, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-17', '07:05:00', 'telat'),
(161, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-18', '14:10:00', 'telat'),
(162, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-19', '22:14:00', 'telat'),
(163, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-20', '22:00:00', 'tepat waktu'),
(164, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-21', '22:00:00', 'tepat waktu'),
(165, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-22', '22:05:00', 'telat'),
(166, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-23', '06:57:00', 'tepat waktu'),
(167, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-24', '07:06:00', 'telat'),
(168, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-25', '06:58:00', 'tepat waktu'),
(170, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-27', '14:05:00', 'telat'),
(171, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-28', '07:14:00', 'telat'),
(172, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-29', '14:00:00', 'tepat waktu'),
(173, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-30', '07:54:00', 'telat'),
(174, 220712003, '0', '0', '2207120012022-7-2020PM.jpg', '2023-03-31', '07:00:00', 'tepat waktu'),
(175, 220712001, '0.0', '0.0', '2023-4-19-220712001.jpg', '2023-04-19', '10:49:16', 'telat'),
(176, 220712001, '0.0', '0.0', '2023-6-18-220712001.jpg', '2023-06-18', '16:04:35', 'telat'),
(177, 220712001, '0.0', '0.0', '2023-6-23-220712001.jpg', '2023-06-23', '18:34:57', 'telat'),
(182, 563146, '-6.8533856', '109.1406238', '2023-7-30-563146.jpg', '2023-07-30', '18:21:52', 'telat'),
(197, 563146, '-6.8530852', '109.1399203', '2023-7-31-563146.jpg', '2023-07-31', '18:23:43', 'tepat waktu'),
(199, 220712001, '-6.8839439', '109.1346783', '2023-7-29-220712001.jpg', '2023-07-29', '21:45:38', 'tepat waktu'),
(203, 563146, '-6.946388', '109.1841025', '2023-8-1-563146.jpg', '2023-08-01', '08:17:12', 'telat'),
(208, 220712001, '-6.878775', '109.13229333333332', '2023-8-9-220712001.jpg', '2023-08-09', '17:35:03', 'telat'),
(212, 563146, '0.0', '0.0', '2023-8-14-563146.jpg', '2023-08-14', '11:44:13', 'telat');

-- --------------------------------------------------------

--
-- Table structure for table `datapulang`
--

CREATE TABLE `datapulang` (
  `id` int(11) NOT NULL,
  `nip` int(11) NOT NULL,
  `latitude` varchar(1000) NOT NULL,
  `longitude` varchar(1000) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `tanggal` date NOT NULL,
  `waktu` time NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `datapulang`
--

INSERT INTO `datapulang` (`id`, `nip`, `latitude`, `longitude`, `foto`, `tanggal`, `waktu`, `status`) VALUES
(10, 220712001, '0.0', '0.0', '2023-1-4-220712001-12-13-34.jpg', '2023-01-04', '12:13:34', 'terlalu cepat'),
(11, 220712001, '0.0', '0.0', '2023-1-3-220712001-12-16-10.jpg', '2023-01-03', '12:16:10', 'terlalu cepat'),
(12, 220712001, '0.0', '0.0', '2023-1-10-220712001-14-27-52.jpg', '2023-01-10', '14:27:52', 'lembur?'),
(14, 220712001, '0.0', '0.0', '2023-1-20-220712001-11-46-53.jpg', '2023-01-20', '11:46:53', 'terlalu cepat'),
(16, 220712001, '-6.951625', '109.183072', '2023-8-14-220712001-11-32-24.jpg', '2023-08-14', '11:32:24', 'lembur?'),
(17, 563146, '0.0', '0.0', '2023-8-14-563146-11-44-32.jpg', '2023-08-14', '11:44:32', 'terlalu cepat');

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
  `no_hp` varchar(13) NOT NULL,
  `alamat` varchar(1000) NOT NULL,
  `deleted_at` date DEFAULT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hrd`
--

INSERT INTO `hrd` (`nip`, `nama`, `email`, `gender`, `ttl`, `no_hp`, `alamat`, `deleted_at`, `created_at`, `updated_at`) VALUES
('1995518202', 'arif rachman', 'rachman12@gmail.com', 'L', '1995-05-18', '089504290562', 'jalan panusukan', '0000-00-00', '2023-06-17', '2023-06-17'),
('2023542023', 'hrd bar', 'newhrd@hrd.hrd', 'L', '2023-05-04', '0895453548868', 'jl hrd kec hrd kab hrd ', '0000-00-00', '2023-05-31', '2023-05-31'),
('2208001', 'hrd lama', 'hrd_lama@mail.com', 'L', '1999-01-12', '0892736787147', 'jln slawi ayu', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id` int(11) NOT NULL,
  `nip` int(11) NOT NULL,
  `shift` varchar(10) NOT NULL,
  `ruangan` varchar(100) NOT NULL,
  `tanggal` date NOT NULL,
  `bulan` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id`, `nip`, `shift`, `ruangan`, `tanggal`, `bulan`) VALUES
(8, 220712001, 'middle 1', 'DAHLIA', '2023-01-11', 1),
(9, 220712003, 'siang', 'DAHLIA', '2023-01-09', 1),
(10, 220712001, 'malam', 'melati', '2023-01-20', 1),
(11, 220712001, 'malam', 'melati', '2023-01-20', 1),
(13, 123, 'pagi', 'DAHLIA', '2023-03-21', 3),
(14, 220712001, 'siang', 'DAHLIA', '2023-03-25', 3),
(15, 123, 'pagi', 'DAHLIA', '2023-03-14', 3),
(16, 123, 'pagi', 'DAHLIA', '2023-03-15', 3),
(17, 123, 'middle', 'DAHLIA', '2023-03-16', 3),
(18, 123, 'malam', 'DAHLIA', '2023-03-17', 3),
(19, 123, 'pagi', 'DAHLIA', '2023-03-18', 3),
(20, 220712001, 'pagi', 'DAHLIA', '2023-03-14', 3),
(21, 220712001, 'middle 1', 'DAHLIA', '2023-03-15', 3),
(22, 220712001, 'siang', 'DAHLIA', '2023-03-16', 3),
(23, 220712001, 'pagi', 'DAHLIA', '2023-03-17', 3),
(24, 220712001, 'malam', 'DAHLIA', '2023-03-18', 3),
(25, 220712001, 'pagi', 'DAHLIA', '2023-03-20', 3),
(26, 220712001, 'middle 1', 'DAHLIA', '2023-03-21', 3),
(27, 220712001, 'malam', 'DAHLIA', '2023-03-22', 3),
(28, 220712001, 'siang', 'DAHLIA', '2023-03-23', 3),
(29, 220712001, 'pagi', 'DAHLIA', '2023-03-24', 3),
(30, 220712001, 'pagi', 'DAHLIA', '2023-03-27', 3),
(31, 220712002, 'pagi', 'DAHLIA', '2023-03-14', 3),
(32, 220712003, 'middle 3', 'DAHLIA', '2023-03-14', 3),
(33, 220712003, 'pagi', 'DAHLIA', '2023-03-16', 3),
(34, 220712003, 'pagi', 'DAHLIA', '2023-03-17', 3),
(35, 220712003, 'middle 4', 'DAHLIA', '2023-03-18', 3),
(36, 220712003, 'middle 2', 'DAHLIA', '2023-03-20', 3),
(37, 220712003, 'siang', 'DAHLIA', '2023-03-21', 3),
(38, 220712003, 'siang', 'DAHLIA', '2023-03-22', 3),
(39, 220712003, 'middle 1', 'DAHLIA', '2023-03-23', 3),
(40, 220712003, 'pagi', 'DAHLIA', '2023-03-24', 3),
(41, 220712003, 'pagi', 'DAHLIA', '2023-03-25', 3),
(42, 220712003, 'middle 1', 'DAHLIA', '2023-03-27', 3),
(43, 220712002, 'pagi', 'DAHLIA', '2023-03-15', 3),
(44, 220712002, 'pagi', 'DAHLIA', '2023-03-16', 3),
(45, 220712002, 'malam', 'DAHLIA', '2023-03-17', 3),
(46, 220712002, 'siang', 'DAHLIA', '2023-03-18', 3),
(47, 220712003, 'middle 1', 'DAHLIA', '2023-03-13', 3),
(48, 220712001, 'siang', 'DAHLIA', '2023-03-19', 3),
(49, 220712001, 'siang', 'DAHLIA', '2023-03-28', 3),
(50, 220712001, 'malam', 'DAHLIA', '2023-03-29', 3),
(51, 220712001, 'pagi', 'DAHLIA', '2023-03-30', 3),
(52, 220712001, 'pagi', 'DAHLIA', '2023-03-31', 3),
(53, 220712002, 'pagi', 'DAHLIA', '2023-03-13', 3),
(54, 220712002, 'malam', 'DAHLIA', '2023-03-20', 3),
(55, 220712002, 'siang', 'DAHLIA', '2023-03-21', 3),
(56, 220712002, 'pagi', 'DAHLIA', '2023-03-22', 3),
(57, 220712002, 'malam', 'DAHLIA', '2023-03-23', 3),
(58, 220712002, 'pagi', 'DAHLIA', '2023-03-24', 3),
(59, 220712002, 'siang', 'DAHLIA', '2023-03-25', 3),
(60, 220712002, 'siang', 'DAHLIA', '2023-03-27', 3),
(61, 220712002, 'pagi', 'DAHLIA', '2023-03-28', 3),
(62, 220712002, 'pagi', 'DAHLIA', '2023-03-29', 3),
(63, 220712002, 'malam', 'DAHLIA', '2023-03-30', 3),
(64, 220712002, 'malam', 'DAHLIA', '2023-03-31', 3),
(65, 220712003, 'pagi', 'DAHLIA', '2023-03-15', 3),
(66, 220712003, 'malam', 'DAHLIA', '2023-03-28', 3),
(67, 220712003, 'middle 1', 'DAHLIA', '2023-03-29', 3),
(68, 220712003, 'pagi', 'DAHLIA', '2023-03-30', 3),
(69, 220712003, 'malam', 'DAHLIA', '2023-03-31', 3),
(70, 220712001, 'pagi', 'MELATI', '2023-04-04', 4),
(71, 220712002, 'siang', 'MELATI', '2023-04-04', 4),
(72, 220712003, 'middle 1', 'MELATI', '2023-04-04', 4),
(73, 220712001, 'malam', 'DAHLIA', '2023-01-12', 1),
(74, 220712002, 'pagi', 'DAHLIA', '2023-01-09', 1),
(75, 220712001, 'pagi', 'DAHLIA', '2023-01-02', 1),
(76, 220712001, 'pagi', 'DAHLIA', '2023-01-04', 1),
(77, 220712001, 'siang', 'DAHLIA', '2023-01-05', 1),
(78, 220712001, 'siang', 'DAHLIA', '2023-01-06', 1),
(79, 220712001, 'middle 1', 'DAHLIA', '2023-01-07', 1),
(80, 220712001, 'middle 2', 'DAHLIA', '2023-01-08', 1),
(81, 220712001, 'middle 2', 'DAHLIA', '2023-01-13', 1),
(82, 220712001, 'middle 2', 'DAHLIA', '2023-01-14', 1),
(83, 220712001, 'middle 2', 'DAHLIA', '2023-01-16', 1),
(84, 220712001, 'malam', 'DAHLIA', '2023-01-17', 1),
(85, 220712001, 'middle 2', 'DAHLIA', '2023-01-19', 1),
(86, 220712001, 'middle 2', 'DAHLIA', '2023-01-23', 1),
(87, 220712001, 'middle 2', 'DAHLIA', '2023-01-24', 1),
(88, 220712001, 'middle 2', 'DAHLIA', '2023-01-26', 1),
(89, 220712001, 'middle 2', 'DAHLIA', '2023-01-27', 1),
(90, 220712001, 'pagi', 'DAHLIA', '2023-01-29', 1),
(91, 220712001, 'malam', 'DAHLIA', '2023-01-30', 1),
(92, 220712001, 'middle 2', 'DAHLIA', '2023-01-31', 1),
(93, 220712001, 'pagi', 'DAHLIA', '2023-01-03', 1),
(94, 220712001, 'middle 1', 'DAHLIA', '2023-01-01', 1),
(95, 220712002, 'siang', 'DAHLIA', '2023-01-10', 1),
(96, 220712001, 'middle 3', 'ANGGREK', '2023-03-10', 3),
(97, 220712001, 'siang', 'DAHLIA', '2023-06-18', 6),
(98, 220712001, 'middle 1', 'DAHLIA', '2023-01-09', 1),
(99, 220712001, 'pagi', 'DAHLIA', '2023-04-09', 4),
(104, 563146, 'middle 4', 'IT', '2023-07-31', 7),
(105, 220712002, 'pagi', 'MELATI', '2023-01-13', 1),
(106, 220712002, 'pagi', 'MELATI', '2023-02-13', 2),
(107, 220712001, 'malam', 'DAHLIA', '2023-07-29', 7),
(109, 220712003, 'pagi', 'DAHLIA', '2023-08-01', 8),
(110, 563146, 'pagi', 'IT', '2023-08-01', 8),
(111, 220712001, 'middle 1', 'DAHLIA', '2023-07-01', 7),
(112, 220712001, 'middle 1', 'DAHLIA', '2023-07-02', 7),
(113, 1540951, 'middle 4', 'IT', '2023-08-01', 8),
(114, 990593, 'pagi', 'DAHLIA', '2023-06-01', 6),
(115, 2209001, 'middle 1', 'DAHLIA', '2023-06-01', 6),
(117, 19090107, 'pagi', '', '2023-06-01', 6),
(118, 990593, 'pagi', 'DAHLIA', '2023-06-02', 6),
(119, 990593, 'pagi', 'DAHLIA', '2023-06-03', 6),
(120, 220712001, 'middle 1', 'DAHLIA', '2023-06-01', 6),
(121, 8709377, 'pagi', 'Security', '2023-06-01', 6),
(122, 220712001, 'malam', 'DAHLIA', '2023-08-09', 8),
(124, 220712001, 'siang', 'DAHLIA', '2023-08-13', 8),
(125, 563146, 'siang', 'DAHLIA', '2023-08-13', 8),
(126, 563146, 'middle 1', 'DAHLIA', '2023-08-14', 8),
(127, 2147483647, 'Budi', 'DAHLIA', '2023-08-01', 8),
(128, 2147483647, 'Budi', 'DAHLIA', '2023-08-02', 8),
(129, 2147483647, 'coba', 'DAHLIA', '2023-08-03', 8),
(130, 2147483647, 'cobaa', 'DAHLIA', '2023-08-04', 8),
(131, 2147483647, 'cobaa', 'DAHLIA', '2023-08-05', 8),
(132, 2147483647, 'coba', 'DAHLIA', '2023-08-07', 8);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal_khusus`
--

INSERT INTO `jadwal_khusus` (`id`, `nip`, `shift`, `ruangan`, `tanggal`) VALUES
(1, 220712001, 'siang', 'dahlia', '2022-07-30'),
(2, 220712001, 'malam', 'dahlia', '2021-09-07');

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
  `alamat` varchar(1000) NOT NULL,
  `deleted_at` date DEFAULT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `karu`
--

INSERT INTO `karu` (`nip`, `nama`, `penempatan`, `email`, `gender`, `ttl`, `no_hp`, `alamat`, `deleted_at`, `created_at`, `updated_at`) VALUES
('2209001', 'dhea', 'DAHLIA', 'karu@gmail.com', 'P', '1992-08-03', '08921321485', 'jl jalak barat gang 3', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `nip` bigint(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `ruangan` varchar(100) DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `ttl` date NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_hp` varchar(15) NOT NULL,
  `alamat` varchar(1000) NOT NULL,
  `posisi` varchar(100) NOT NULL,
  `deleted_at` date DEFAULT NULL,
  `created_at` date DEFAULT current_timestamp(),
  `updated_at` date DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`nip`, `nama`, `ruangan`, `gender`, `ttl`, `email`, `no_hp`, `alamat`, `posisi`, `deleted_at`, `created_at`, `updated_at`) VALUES
(450995, 'cobardftf', 'NUSA-INDAH', 'L', '2002-01-08', 'ilham21silva@gmail.com', '0897532587965', 'jl blabla12', 'security', '0000-00-00', '2023-08-05', '2023-08-05'),
(563146, 'Joko', 'DAHLIA', 'L', '1996-11-20', 'Joko@gmail.com', '089976888902', 'Jalan Merpati', 'Programer', '0000-00-00', '2023-07-30', '2023-07-30'),
(923578, 'M Ilham Fajar Sidiq', 'DAHLIA', 'L', '2003-02-08', 'ilham21silva@gmail.com', '08798878888', 'jl blabla', 'Programer', '0000-00-00', '2023-08-05', '2023-08-05'),
(990593, 'agus210', 'DAHLIA', 'L', '2006-06-01', 'agus21@gmail.com', '08978', 'jl balamoa selatan', 'Perawat', '0000-00-00', '2023-08-01', '2023-08-01'),
(1540951, 'agus', 'IT', 'L', '2006-06-01', 'agus21@gmail.com', '08978', 'jjascbas', 'Programer', '0000-00-00', '2023-08-01', '2023-08-01'),
(5691370, '123', 'DAHLIA', 'L', '2000-06-21', 'ilham21silva@gmail.com', '089765898298', 'jalan blanak', 'IT', '0000-00-00', '2023-08-18', '2023-08-18'),
(7426713, 'coba', 'Security', 'L', '1998-01-06', 'maulanailham425@yahoo.com', '0897632134', 'jl blabla', 'security', '0000-00-00', '2023-08-05', '2023-08-05'),
(8405641, 'Budi Santoso', 'Security', 'L', '0000-00-00', 'Budi@gmail.com', '0897677865467', 'Jalan Blanak', 'Security', '0000-00-00', '2023-08-19', '2023-08-19'),
(8709377, 'Dony', 'Security', 'L', '2023-08-05', 'iljl@mail.com', '08965635242', 'hvvhgvghcrrt', 'Security', '0000-00-00', '2023-08-05', '2023-08-05'),
(220712001, 'Bamba', 'DAHLIA', 'L', '1992-08-03', 'bambang@gmail.com', '08972708282728', 'Jalan Korea no.25', 'Perawat', NULL, NULL, NULL),
(220712003, 'gilang', 'DAHLIA', 'L', '1993-01-20', 'jbjknkj@gmail.com', '085535443', 'jvhvjbkjbkjbiu', 'Perawat', NULL, NULL, NULL),
(2308120100017, 'ani', 'DAHLIA', 'P', '2002-01-01', 'ani@gmail.com', '089645646587', 'jkhjkhkj', 'akuntan', '0000-00-00', '2023-08-20', '2023-08-20'),
(2308120100018, 'nurdin', 'Akutansi', 'L', '1949-09-20', 'nurdin@gmail.com', '0967867564539', 'jl nlnunuknkjnk', 'akuntan', '0000-00-00', '2023-08-20', '2023-08-20'),
(2308243222020, 'doni', 'Kepegawaian', 'L', '1999-11-28', 'doni@ail.net', '0897567563452', 'jl ygutgf5fy', 'staff', '0000-00-00', '2023-08-20', '2023-08-20'),
(2308254272015, 'Joni', 'IT', 'L', '1999-02-06', 'Joni@gmail.com', '089728278292', 'Jalan Murnu', 'Programer', '0000-00-00', '2023-08-19', '2023-08-19'),
(2308254272016, 'BambangJonjon', 'IT', 'L', '1999-02-10', 'Jonjon@gmail.com', '089722992922', 'Jalan Mamam', 'Programer', '0000-00-00', '2023-08-19', '2023-08-19'),
(2308272272014, 'Eis Putri sholeka', 'IT', 'P', '1997-01-20', 'EisPutri@gmail.com', '089278289202', 'Jalan maryam', 'IT', '0000-00-00', '2023-08-19', '2023-08-19'),
(2308633138013, 'ilhammam', 'Security', 'L', '1999-02-10', 'mamam@gmail.com', '089229920202', 'Jalan Kemuning', 'Security', '0000-00-00', '2023-08-19', '2023-08-19'),
(2308633272012, 'Sayahuro', 'Security', 'L', '1999-02-21', 'Says@gmail.com', '089627262872', 'Jalan Kenang', 'Security', '0000-00-00', '2023-08-19', '2023-08-19'),
(2308670295019, 'nina', 'Farmasi', 'P', '2000-12-30', 'nina@mal.net', '089767564534', 'jl blbserstr', 'apoteker', '0000-00-00', '2023-08-20', '2023-08-20');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `nip` bigint(20) NOT NULL,
  `pswd` varchar(1000) NOT NULL,
  `role` varchar(10) NOT NULL,
  `token` varchar(15) NOT NULL,
  `device_id` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`nip`, `pswd`, `role`, `token`, `device_id`) VALUES
(450995, 'pbkdf2:sha256:260000$jiKYLv2UBdTU31iG$e5a3944427e860b63dba03e35bf007422907e913a029471d44533b17605f93cf', 'karyawan', '', NULL),
(563146, 'pbkdf2:sha256:260000$1De3sgqoYWZP0Fax$6a35054041aaadc505de7a42ea4c5014b1207626a1c7c22c05dcb905c38045f9', 'karyawan', 'J4GGP8LQAXYSQFC', 'dc9da44edb512b27'),
(923578, 'pbkdf2:sha256:260000$6MGnogKLuwphIPTf$290bb199863d97eca2446658e36be2b49da94c07f717ac9921ecc430087093e4', 'karyawan', 'SGXZ4DOJ8MIJIZ2', 'cb9422271fd6df3c'),
(990593, 'pbkdf2:sha256:260000$GDU9XUuxoxlT8Riq$47fb21cddbdd8cb5ab423133928cb17c67d40539502a9c6a0b8c4c76d9614464', 'karyawan', '', 'None'),
(1540951, 'pbkdf2:sha256:260000$BDsOAjZ7anBidkXa$82297f4c813dc2c9ce036180b52d33f0b02a479f54c98b9845e51b55fb2b6d1e', 'karyawan', 'Y0YMSOSGOEOP1GP', NULL),
(2208001, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'HRD', 'JT5M84NWZHF8AQV', '867308042510437'),
(2209001, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'karu', '', NULL),
(5691370, 'pbkdf2:sha256:260000$eigRSPMfHjHILVxt$894e4547e4b40f537693962e6e7f393cd95befb88ed6a067d841f75362c3372f', 'karyawan', '', NULL),
(7426713, 'pbkdf2:sha256:260000$ZPP8o13rijYXg0PG$308b94c741d5833a5a5fb3d5672d654c5830fce78fdd37227522d47cad7f4d5e', 'karyawan', '', NULL),
(8405641, 'pbkdf2:sha256:260000$zrWoCRjmdgwfdctD$95934d18a23d0d11c2686d2a36d22a7e13c3fdbc5ee242212061596dff913b8d', 'karyawan', '', NULL),
(8709377, 'pbkdf2:sha256:260000$dMnW1kh9S2ZcADYf$4d66e42afa7e77390ee4cfdf27859212837dacf7252012fc7bbbb673538b7d91', 'karyawan', '', NULL),
(19090101, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'admin', '', NULL),
(19090107, 'sha256$nLb0vObcNS7FiHeC$645acf9b245e3d523e5629b59e3ba5750cb60ce6ee0b1cdab44cb5a07c22b49d', 'admin', '', NULL),
(220712001, 'pbkdf2:sha256:260000$CErCYrSF4zi5DXO3$5350ec065d4a6a609c9c6e0b23169ac65c186392a53ee86d4582bfba7230d058', 'karyawan', 'N2O8G6IEOW55YZO', '867308042510437'),
(220712002, 'pbkdf2:sha256:260000$vmSAtn1BmZpukPDj$b061d2812b3e02e20eefb2f2dabeccc2e65033b5461765c064c7b9b3da6fc6b3', 'karyawan', 'WX7R197BX3NFCB8', NULL),
(220712003, 'pbkdf2:sha256:260000$vmSAtn1BmZpukPDj$b061d2812b3e02e20eefb2f2dabeccc2e65033b5461765c064c7b9b3da6fc6b3', 'karyawan', 'QV4BMXOR7DCZ3SO', NULL),
(220712004, 'pbkdf2:sha256:260000$vmSAtn1BmZpukPDj$b061d2812b3e02e20eefb2f2dabeccc2e65033b5461765c064c7b9b3da6fc6b3', 'karyawan', 'VN1KU71J6AKOATV', NULL),
(2308120100017, 'pbkdf2:sha256:260000$U2RbF9vQlZfwgFV6$4e5d6a3de94154f366871ae31ca79d9b837a1d2043d611c71aac0940b310c689', 'karyawan', '', 'None'),
(2308120100018, 'pbkdf2:sha256:260000$jhYLBWUba116p7eS$0faafab28a56f018733ed75a26a257474a1b0d859678afa60c99231014ad542f', 'karyawan', '', NULL),
(2308243222020, 'pbkdf2:sha256:260000$yCyErkdO7y01BjPG$e5dff1b54d2c31bbf15a9e5694200173975e6d3dbc7ea22b66c9c095f95dc886', 'karyawan', '', NULL),
(2308254272015, 'pbkdf2:sha256:260000$MWozogful4EapUVN$c320a98339ac6dc40f698ec3284344d9ce446800a069ae4cd9e6f599af4e09fb', 'karyawan', '', NULL),
(2308254272016, 'pbkdf2:sha256:260000$ajHglFXd6NfDpR6P$36e0265bb8dedc5476889ddcdbaa330742444df027099d28ea79c4f2a5a1e953', 'karyawan', '', NULL),
(2308272272014, 'pbkdf2:sha256:260000$ekaauFM83gQcaQju$9223df836cbb450212587f7bce7a071aa8908b1494c1fb492921cc8f31c87333', 'karyawan', '', NULL),
(2308633138013, 'pbkdf2:sha256:260000$OXob5hFI344L7Hjv$a3d031eda12451bc4ea0e76579c8761c9a82e3478bd9f5cb9d1dedeaf1c3e479', 'karyawan', '', 'None'),
(2308633272012, 'pbkdf2:sha256:260000$TcxS0Swc84Xt9REK$233d68fa3d7378a183d3d3616d8310ba20fda575010572a306274032e6a32fd0', 'karyawan', '', 'None'),
(2308670295019, 'pbkdf2:sha256:260000$gtk7WSoXyRitZttc$a7440d25b13f080e195a5e27eead4ed0745ae0cdab7ba1dd11ed5f3bad763a98', 'karyawan', '', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `posisi`
--

CREATE TABLE `posisi` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posisi`
--

INSERT INTO `posisi` (`id`, `nama`) VALUES
(1, 'perawat'),
(2, 'dokter umum'),
(3, 'suster');

-- --------------------------------------------------------

--
-- Table structure for table `ruangan`
--

CREATE TABLE `ruangan` (
  `id` int(11) NOT NULL,
  `Nama` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ruangan`
--

INSERT INTO `ruangan` (`id`, `Nama`) VALUES
(1, 'DAHLIA'),
(2, 'MELATI'),
(3, 'BOUGENVILLE'),
(4, 'AMARILIS'),
(5, 'ANGGREK'),
(6, 'ANYELIR'),
(7, 'ALAMANDA'),
(8, 'CASABLANCA'),
(9, 'MELATI'),
(10, 'LILY'),
(11, 'SAKURA'),
(12, 'NUSA-INDAH'),
(13, 'IT'),
(14, 'Security'),
(15, 'Akutansi'),
(16, 'Kepegawaian'),
(17, 'Farmasi');

-- --------------------------------------------------------

--
-- Table structure for table `shift`
--

CREATE TABLE `shift` (
  `id` int(11) NOT NULL,
  `Nama` varchar(10) NOT NULL,
  `berangkat` time NOT NULL,
  `pulang` time NOT NULL,
  `jam_kerja` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shift`
--

INSERT INTO `shift` (`id`, `Nama`, `berangkat`, `pulang`, `jam_kerja`) VALUES
(1, 'pagi', '07:00:00', '14:00:00', '07:00:00'),
(2, 'middle 1', '10:00:00', '17:00:00', '07:00:00'),
(3, 'siang', '14:00:00', '22:00:00', '08:00:00'),
(4, 'malam', '22:00:00', '07:00:00', '09:00:00'),
(5, 'middle 2', '10:00:00', '17:00:00', '07:00:00'),
(6, 'middle 3', '11:00:00', '18:00:00', '07:00:00'),
(7, 'middle 4', '18:30:00', '01:30:00', '08:00:00'),
(12, 'Budi', '07:00:00', '14:00:00', '07:00:00'),
(13, 'cobaa', '22:01:00', '01:00:59', '22:01:00'),
(16, 'coba', '01:00:00', '23:00:00', '22:00:00');

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
  ADD PRIMARY KEY (`nip`),
  ADD UNIQUE KEY `nama` (`nama`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`nip`);

--
-- Indexes for table `posisi`
--
ALTER TABLE `posisi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ruangan`
--
ALTER TABLE `ruangan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shift`
--
ALTER TABLE `shift`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Nama` (`Nama`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dataabsen`
--
ALTER TABLE `dataabsen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=213;

--
-- AUTO_INCREMENT for table `datapulang`
--
ALTER TABLE `datapulang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;

--
-- AUTO_INCREMENT for table `jadwal_khusus`
--
ALTER TABLE `jadwal_khusus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `posisi`
--
ALTER TABLE `posisi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ruangan`
--
ALTER TABLE `ruangan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `shift`
--
ALTER TABLE `shift`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 08, 2026 at 11:08 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `exw_fca`
--

-- --------------------------------------------------------

--
-- Table structure for table `exchange_rates`
--

CREATE TABLE `exchange_rates` (
  `id` int(11) NOT NULL,
  `currency_code` char(3) DEFAULT NULL,
  `rate_to_brl` decimal(10,4) DEFAULT NULL,
  `source` varchar(50) DEFAULT 'BCB_PTAX',
  `effective_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `freight_matrix`
--

CREATE TABLE `freight_matrix` (
  `origin_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL,
  `cost_per_ton` decimal(10,2) DEFAULT NULL,
  `distance_km` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `origins`
--

CREATE TABLE `origins` (
  `origin_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` char(2) DEFAULT NULL,
  `country` char(2) DEFAULT 'BR'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ports`
--

CREATE TABLE `ports` (
  `port_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `port_code` char(5) DEFAULT NULL,
  `country` char(2) DEFAULT 'BR'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ports`
--

INSERT INTO `ports` (`port_id`, `name`, `port_code`, `country`) VALUES
(1, 'Santos', 'BRSSZ', 'BR'),
(2, 'Rio de Janeiro', 'BRRIO', 'BR'),
(3, 'Paranaguá', 'BRPNG', 'BR'),
(4, 'Rotterdam', 'NLRTM', 'NL'),
(5, 'Shanghai', 'CNSHA', 'CN'),
(6, 'Los Angeles', 'USLAX', 'US');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `hs_code` varchar(20) DEFAULT NULL,
  `unit_weight_kg` decimal(10,2) DEFAULT NULL,
  `price_exw_brl` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `view_export_prices`
-- (See below for the actual view)
--
CREATE TABLE `view_export_prices` (
`product` varchar(100)
,`price_brl` decimal(15,2)
,`price_usd` decimal(20,2)
,`price_eur` decimal(20,2)
,`price_cny` decimal(20,2)
);

-- --------------------------------------------------------

--
-- Structure for view `view_export_prices`
--
DROP TABLE IF EXISTS `view_export_prices`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_export_prices`  AS SELECT `p`.`name` AS `product`, `p`.`price_exw_brl` AS `price_brl`, round(`p`.`price_exw_brl` / (select `exchange_rates`.`rate_to_brl` from `exchange_rates` where `exchange_rates`.`currency_code` = 'USD' order by `exchange_rates`.`effective_date` desc limit 1),2) AS `price_usd`, round(`p`.`price_exw_brl` / (select `exchange_rates`.`rate_to_brl` from `exchange_rates` where `exchange_rates`.`currency_code` = 'EUR' order by `exchange_rates`.`effective_date` desc limit 1),2) AS `price_eur`, round(`p`.`price_exw_brl` / (select `exchange_rates`.`rate_to_brl` from `exchange_rates` where `exchange_rates`.`currency_code` = 'CNY' order by `exchange_rates`.`effective_date` desc limit 1),2) AS `price_cny` FROM `products` AS `p` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `exchange_rates`
--
ALTER TABLE `exchange_rates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_rate` (`currency_code`,`effective_date`);

--
-- Indexes for table `freight_matrix`
--
ALTER TABLE `freight_matrix`
  ADD PRIMARY KEY (`origin_id`,`port_id`),
  ADD KEY `fk_port` (`port_id`);

--
-- Indexes for table `origins`
--
ALTER TABLE `origins`
  ADD PRIMARY KEY (`origin_id`);

--
-- Indexes for table `ports`
--
ALTER TABLE `ports`
  ADD PRIMARY KEY (`port_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `exchange_rates`
--
ALTER TABLE `exchange_rates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `origins`
--
ALTER TABLE `origins`
  MODIFY `origin_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ports`
--
ALTER TABLE `ports`
  MODIFY `port_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `freight_matrix`
--
ALTER TABLE `freight_matrix`
  ADD CONSTRAINT `fk_origin` FOREIGN KEY (`origin_id`) REFERENCES `origins` (`origin_id`),
  ADD CONSTRAINT `fk_port` FOREIGN KEY (`port_id`) REFERENCES `ports` (`port_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

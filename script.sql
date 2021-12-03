-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-12-2021 a las 19:55:25
-- Versión del servidor: 10.4.21-MariaDB
-- Versión de PHP: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `municipios`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_municipios`
--

CREATE TABLE `tbl_municipios` (
  `nombre_municipio` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tbl_municipios`
--

INSERT INTO `tbl_municipios` (`nombre_municipio`) VALUES
('huehuetoca'),
('zumpango'),
('coyotepec'),
('teoloyucan'),
('melchor'),
('tepotzotlan'),
('cuautitlan'),
('izcalli'),
('tultitlán'),
('coacalco'),
('atizapan'),
('tlanepantla');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_rutas`
--

CREATE TABLE `tbl_rutas` (
  `ruta_origen` varchar(50) NOT NULL,
  `ruta_destino` varchar(50) NOT NULL,
  `km` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tbl_rutas`
--

INSERT INTO `tbl_rutas` (`ruta_origen`, `ruta_destino`, `km`) VALUES
('huehuetoca', 'zumpango','9'),
('huehuetoca', 'coyotepec','3'),
('zumpango', 'teoloyucan','5'),
('coyotepec', 'teoloyucan','3'),
('teoloyucan', 'tepozotlan','5'),
('teoloyucan', 'melchor','3'),
('teoloyucan', 'cuautitlan','7'),
('teoloyucan', 'tultitlan','10'),
('teoloyucan', 'izcalli','9'),
('teoloyucan', 'tlanepantla','17'),
('tepozotlan', 'izcalli','3'),
('izcalli', 'atizapan','6'),
('tultitlan', 'coacalco','5'),
('tultitlan', 'tlanepantla','5'),
('coacalco', 'tlanepantla','11'),
('tlanepantla', 'atizapan','3');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_tarifas`
--

CREATE TABLE `tbl_tarifas` (
  `tarifa` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tbl_tarifas`
--

INSERT INTO `tbl_tarifas` (`tarifa`) VALUES
('11'),
('12'),
('13'),
('14'),
('15'),
('16'),
('17'),
('18'),
('19'),
('20'),
('21'),
('22'),
('23'),
('24'),
('25'),
('26');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

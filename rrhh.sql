-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-10-2024 a las 20:51:44
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `rrhh`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulaciones`
--

CREATE TABLE `postulaciones` (
  `id` varchar(36) NOT NULL,
  `vacante_id` varchar(36) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `cv` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` binary(16) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `contrasena` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `nombre`, `email`, `telefono`, `contrasena`) VALUES
(0x37343961323330382d613333362d3430, 'Nelvin', 'admin@admin.com', '04247537350', '12345678'),
(0x64613938663935642d313934392d3437, 'Nelvin', 'njmarquezm@gmail.com', '04247537350', '12345678');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vacantes`
--

CREATE TABLE `vacantes` (
  `id` binary(16) NOT NULL,
  `iduser` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `salario` decimal(10,2) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `tipo_contrato` enum('Tiempo Completo','Medio Tiempo','Contrato','Temporal','Prácticas') DEFAULT NULL,
  `experiencia_requerida` varchar(255) DEFAULT NULL,
  `educacion_requerida` varchar(255) DEFAULT NULL,
  `habilidades_requeridas` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `postulaciones`
--
ALTER TABLE `postulaciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `vacantes`
--
ALTER TABLE `vacantes`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

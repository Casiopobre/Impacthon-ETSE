DROP DATABASE IF EXISTS `pastillero`;
CREATE DATABASE IF NOT EXISTS `pastillero`;
USE `pastillero`;
-- DROP TABLE IF EXISTS `ProfesionalPaciente`;  

-- ============================================================
-- 1. Tabla de Usuarios (Pacientes y Profesionales Sanitarios)
-- ============================================================
CREATE TABLE IF NOT EXISTS `Usuario` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `dni` VARCHAR(9) NOT NULL,
    `tipo` ENUM('paciente', 'medico') NOT NULL DEFAULT 'paciente',
    `email` VARCHAR(255),
    `fecha_nac` DATE NOT NULL,
    `nombre_completo` TEXT NOT NULL,
    `passwd` LONGTEXT NOT NULL,
    `num_tlf` INT,
    `profesional_responsable` BIGINT UNSIGNED,  -- Profesional responsable (FK para pacientes)
    UNIQUE KEY (`dni`)
);

-- ============================================================
-- 3. Tabla de Opciones (1:1 con Paciente)
-- ============================================================
CREATE TABLE IF NOT EXISTS `Opciones` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` BIGINT UNSIGNED NOT NULL,
    `voz` BOOLEAN NOT NULL DEFAULT 0,
    `interfaz_guiada` BOOLEAN NOT NULL DEFAULT 0,
    `nivel_recordatorios` INT NOT NULL DEFAULT 2,
    UNIQUE KEY (`id_paciente`),
    CONSTRAINT `opciones_paciente_foreign` FOREIGN KEY (`id_paciente`) REFERENCES `Usuario`(`id`)
);

-- ============================================================
-- 4. Tabla de Código QR (asociado a un Paciente)
-- ============================================================
CREATE TABLE IF NOT EXISTS  `codigoQR` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `token` VARCHAR(10) NOT NULL,
    `paciente` BIGINT UNSIGNED NOT NULL,
    `usp` ENUM('login', 'editar') NOT NULL,
    CONSTRAINT `codigoqr_paciente_foreign` FOREIGN KEY (`paciente`) REFERENCES `Usuario`(`id`)
);

-- ============================================================
-- 5. Tabla de Medicamentos
-- (Estructura basada en el script previo para el JSON de la API CIMA)
-- ============================================================
CREATE TABLE IF NOT EXISTS  `Medicamento` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `nregistro` VARCHAR(255) NOT NULL UNIQUE,
    `nombre` VARCHAR(255) NOT NULL,
    `labtitular` VARCHAR(255),
    `labcomercializador` VARCHAR(255),
    `cpresc` VARCHAR(255),
    `estado_aut` BIGINT,
    `estado_rev` BIGINT NULL,
    `comerc` BOOLEAN,
    `receta` BOOLEAN,
    `generico` BOOLEAN,
    `conduc` BOOLEAN,
    `triangulo` BOOLEAN,
    `huerfano` BOOLEAN,
    `biosimilar` BOOLEAN,
    `nosustituible_id` INT,
    `nosustituible_nombre` VARCHAR(255),
    `psum` BOOLEAN,
    `notas` BOOLEAN,
    `materialesInf` BOOLEAN,
    `ema` BOOLEAN,
    `vtm_id` BIGINT,
    `vtm_nombre` VARCHAR(255),
    `dosis` TEXT,
    `formaFarmaceutica_id` INT,
    `formaFarmaceutica_nombre` VARCHAR(255),
    `formaFarmaceuticaSimplificada_id` INT,
    `formaFarmaceuticaSimplificada_nombre` VARCHAR(255),
    `viaAdministracion_id` INT,
    `viaAdministracion_nombre` VARCHAR(255)
);


-- ============================================================
-- 6. Tabla de Recetas (Relación: Paciente - Medicamento)
-- ============================================================
CREATE TABLE IF NOT EXISTS `Receta` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` BIGINT UNSIGNED NOT NULL,
    `id_medicamento` BIGINT UNSIGNED NOT NULL,
    `fecha_emision` DATE NOT NULL,
    `fecha_fin` DATE NOT NULL,
    `dosificacion` INT NOT NULL,
    `intervalos_dosificacion` INT NOT NULL,
    CONSTRAINT `receta_id_paciente_foreign` FOREIGN KEY (`id_paciente`) REFERENCES `Usuario`(`id`),
    CONSTRAINT `receta_id_medicamento_foreign` FOREIGN KEY (`id_medicamento`) REFERENCES `Medicamento`(`id`)
);

-- ============================================================
-- 7. Tabla de Sintomatología (una entrada por día y paciente)
-- ============================================================
CREATE TABLE IF NOT EXISTS `Sintomatologia` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` BIGINT UNSIGNED NOT NULL,
    `fecha` DATE NOT NULL,
    `sintomas` TEXT NOT NULL,
    CONSTRAINT `sintomatologia_id_paciente_foreign` FOREIGN KEY (`id_paciente`) REFERENCES `Usuario`(`id`),
    UNIQUE KEY `unique_sintomatologia` (`id_paciente`, `fecha`)
);

-- ============================================================
-- 8. Tabla de Relación Profesional - Paciente
-- (Un profesional puede atender a varios pacientes)
-- ============================================================
-- CREATE TABLE IF NOT EXISTS `ProfesionalPaciente` (
--     `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     `id_profesional` BIGINT UNSIGNED NOT NULL,
--     `id_paciente` BIGINT UNSIGNED NOT NULL,
--     UNIQUE KEY (`id_profesional`, `id_paciente`),
--     CONSTRAINT `profesionalpaciente_profesional_foreign` FOREIGN KEY (`id_profesional`) REFERENCES `ProfesionalSanitario`(`id`),
--     CONSTRAINT `profesionalpaciente_paciente_foreign` FOREIGN KEY (`id_paciente`) REFERENCES `Paciente`(`id`)
-- );

-- ============================================================
-- 9. Relaciones adicionales
-- ============================================================

-- En Paciente, el campo profesional_responsable es obligatorio para la existencia del registro
ALTER TABLE `Usuario`
    ADD CONSTRAINT `paciente_profesional_responsable_foreign`
    FOREIGN KEY (`profesional_responsable`) REFERENCES `Usuario`(`id`);

-- (Opcional) Si se desea agregar índices para optimizar consultas:
ALTER TABLE `Usuario` ADD INDEX `paciente_profesional_responsable_index` (`profesional_responsable`);
ALTER TABLE `Receta` ADD INDEX `receta_id_paciente_index` (`id_paciente`);
ALTER TABLE `Receta` ADD INDEX `receta_id_medicamento_index` (`id_medicamento`);
ALTER TABLE `Sintomatologia` ADD INDEX `sintomatologia_id_paciente_index` (`id_paciente`);
ALTER TABLE `codigoQR` ADD INDEX `codigoqr_paciente_index` (`paciente`);

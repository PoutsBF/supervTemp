-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'Capteurs'
-- 
-- ---

DROP TABLE IF EXISTS `Capteurs`;
		
CREATE TABLE `Capteurs` (
  `idCapteur` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `mac_addr` MEDIUMTEXT(17) NULL DEFAULT NULL,
  `location` MEDIUMTEXT(20) NULL DEFAULT NULL,
  `name` MEDIUMTEXT(15) NULL DEFAULT NULL,
  PRIMARY KEY (`idCapteur`)
);

-- ---
-- Table 'Datas'
-- 
-- ---

DROP TABLE IF EXISTS `Datas`;
		
CREATE TABLE `Datas` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `idCapteur` INTEGER NULL DEFAULT NULL,
  `timeStamp` DATETIME NULL DEFAULT NULL,
  `temperature` FLOAT NULL DEFAULT NULL,
  `hygrometrie` FLOAT NULL DEFAULT NULL,
  `batterie` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `Datas` ADD FOREIGN KEY (idCapteur) REFERENCES `Capteurs` (`idCapteur`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `Capteurs` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Datas` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `Capteurs` (`idCapteur`,`mac_addr`,`location`,`name`) VALUES
-- ('','','','');
-- INSERT INTO `Datas` (`id`,`idCapteur`,`timeStamp`,`temperature`,`hygrometrie`,`batterie`) VALUES
-- ('','','','','','');
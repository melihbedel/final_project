-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema final_project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema final_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `final_project` DEFAULT CHARACTER SET utf8mb4 ;
USE `final_project` ;

-- -----------------------------------------------------
-- Table `final_project`.`company_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`company_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `contacts` VARCHAR(45) NULL,
  `logo` BLOB NULL,
  `job_ads` INT NULL,
  `matches` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `final_project`.`companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`companies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `company_info_id` INT NOT NULL,
  PRIMARY KEY (`id`, `company_info_id`),
  INDEX `fk_companies_company_info_idx` (`company_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_companies_company_info`
    FOREIGN KEY (`company_info_id`)
    REFERENCES `final_project`.`company_info` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `final_project`.`professional_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`professional_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `summary` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `status` TINYINT(1) NULL,
  `logo` BLOB NULL,
  `company_ads` INT NULL,
  `matches` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `final_project`.`professionals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`professionals` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `professional_info_id` INT NOT NULL,
  PRIMARY KEY (`id`, `professional_info_id`),
  INDEX `fk_professionals_professional_info1_idx` (`professional_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_professionals_professional_info1`
    FOREIGN KEY (`professional_info_id`)
    REFERENCES `final_project`.`professional_info` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `final_project`.`company_ad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`company_ad` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `professionals_id` INT NOT NULL,
  `professionals_professional_info_id` INT NOT NULL,
  `salary_min` INT NULL,
  `salary_max` INT NULL,
  `description` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `skills` VARCHAR(45) NULL,
  `matches` VARCHAR(45) NULL,
  PRIMARY KEY (`id`, `professionals_id`, `professionals_professional_info_id`),
  INDEX `fk_company_ad_professionals1_idx` (`professionals_id` ASC, `professionals_professional_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_company_ad_professionals1`
    FOREIGN KEY (`professionals_id` , `professionals_professional_info_id`)
    REFERENCES `final_project`.`professionals` (`id` , `professional_info_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `final_project`.`job_ad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`job_ad` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `companies_id` INT NOT NULL,
  `companies_company_info_id` INT NOT NULL,
  `salary_min` INT NULL,
  `salary_max` INT NULL,
  `description` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `status` TINYINT(1) NULL,
  `requirements` VARCHAR(45) NULL,
  `matches` VARCHAR(45) NULL,
  PRIMARY KEY (`id`, `companies_id`, `companies_company_info_id`),
  INDEX `fk_job_ad_companies1_idx` (`companies_id` ASC, `companies_company_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ad_companies1`
    FOREIGN KEY (`companies_id` , `companies_company_info_id`)
    REFERENCES `final_project`.`companies` (`id` , `company_info_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

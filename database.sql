- MySQL Workbench Forward Engineering-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
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
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `contacts` VARCHAR(45) NULL DEFAULT NULL,
  `logo` BLOB NULL DEFAULT NULL,
  `job_ads` INT(11) NULL DEFAULT NULL,
  `matches` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 38
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`login_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`login_users` (
  `login_user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `type` INT(11) NOT NULL,
  PRIMARY KEY (`login_user_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 48
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`companies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `login_id1` INT(11) NOT NULL,
  `company_info_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `company_info_id`),
  INDEX `fk_companies_login_users1_idx` (`login_id1` ASC) VISIBLE,
  INDEX `fk_companies_company_info1_idx` (`company_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_companies_company_info1`
    FOREIGN KEY (`company_info_id`)
    REFERENCES `final_project`.`company_info` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_companies_login_users1`
    FOREIGN KEY (`login_id1`)
    REFERENCES `final_project`.`login_users` (`login_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`professionals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`professionals` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `last_name` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `login_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_professionals_login_users1_idx` (`login_id` ASC) VISIBLE,
  CONSTRAINT `fk_professionals_login_users1`
    FOREIGN KEY (`login_id`)
    REFERENCES `final_project`.`login_users` (`login_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`company_ad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`company_ad` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `professionals_id` INT(11) NOT NULL,
  `professionals_professional_info_id` INT(11) NOT NULL,
  `salary_min` INT(11) NULL DEFAULT NULL,
  `salary_max` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `status` VARCHAR(45) NULL DEFAULT NULL,
  `skills` VARCHAR(45) NULL DEFAULT NULL,
  `matches` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `professionals_id`, `professionals_professional_info_id`),
  INDEX `fk_company_ad_professionals1_idx` (`professionals_id` ASC, `professionals_professional_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_company_ad_professionals1`
    FOREIGN KEY (`professionals_id`)
    REFERENCES `final_project`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`job_ad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`job_ad` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `companies_id` INT(11) NOT NULL,
  `companies_company_info_id` INT(11) NOT NULL,
  `salary_min` INT(11) NULL DEFAULT NULL,
  `salary_max` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `status` TINYINT(1) NULL DEFAULT NULL,
  `requirements` VARCHAR(45) NULL DEFAULT NULL,
  `matches` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `companies_id`, `companies_company_info_id`),
  INDEX `fk_job_ad_companies1_idx` (`companies_id` ASC, `companies_company_info_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ad_companies1`
    FOREIGN KEY (`companies_id`)
    REFERENCES `final_project`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`professional_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`professional_info` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `summary` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `status` TINYINT(1) NULL DEFAULT NULL,
  `logo` BLOB NULL DEFAULT NULL,
  `company_ads` INT(11) NULL DEFAULT NULL,
  `matches` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
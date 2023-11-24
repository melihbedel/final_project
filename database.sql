-- MySQL Workbench Forward Engineering

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
AUTO_INCREMENT = 53
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`companies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `login_id1` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_companies_login_users1_idx` (`login_id1` ASC) VISIBLE,
  CONSTRAINT `fk_companies_login_users1`
    FOREIGN KEY (`login_id1`)
    REFERENCES `final_project`.`login_users` (`login_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`professionals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`professionals` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `login_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_professionals_login_users1_idx` (`login_id` ASC) VISIBLE,
  CONSTRAINT `fk_professionals_login_users1`
    FOREIGN KEY (`login_id`)
    REFERENCES `final_project`.`login_users` (`login_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`company_ads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`company_ads` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `professional_id` INT(11) NOT NULL,
  `salary_min` INT(11) NULL DEFAULT NULL,
  `salary_max` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `status` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_company_ads_professionals1_idx` (`professional_id` ASC) VISIBLE,
  CONSTRAINT `fk_company_ads_professionals1`
    FOREIGN KEY (`professional_id`)
    REFERENCES `final_project`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`skills` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `skill` VARCHAR(45) NOT NULL,
  `level` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`company_ads_has_skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`company_ads_has_skills` (
  `company_ad_id` INT(11) NOT NULL,
  `skill_id` INT(11) NOT NULL,
  PRIMARY KEY (`company_ad_id`, `skill_id`),
  INDEX `fk_company_ads_has_skills_skills1_idx` (`skill_id` ASC) VISIBLE,
  INDEX `fk_company_ads_has_skills_company_ads1_idx` (`company_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_company_ads_has_skills_company_ads1`
    FOREIGN KEY (`company_ad_id`)
    REFERENCES `final_project`.`company_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_company_ads_has_skills_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `final_project`.`skills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`company_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`company_info` (
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `contacts` VARCHAR(45) NULL DEFAULT NULL,
  `logo` BLOB NULL DEFAULT NULL,
  `job_ads` INT(11) NULL DEFAULT NULL,
  `matches` INT(11) NULL DEFAULT NULL,
  `companies_id` INT(11) NOT NULL,
  PRIMARY KEY (`companies_id`),
  CONSTRAINT `fk_company_info_companies1`
    FOREIGN KEY (`companies_id`)
    REFERENCES `final_project`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`job_ads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`job_ads` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `company_id` INT(11) NOT NULL,
  `salary_min` INT(11) NULL DEFAULT NULL,
  `salary_max` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `status` TINYINT(1) NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  INDEX `fk_job_ads_companies1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_companies1`
    FOREIGN KEY (`company_id`)
    REFERENCES `final_project`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`job_ads_has_skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`job_ads_has_skills` (
  `job_ad_id` INT(11) NOT NULL,
  `skill_id` INT(11) NOT NULL,
  PRIMARY KEY (`job_ad_id`, `skill_id`),
  INDEX `fk_job_ads_has_skills_skills1_idx` (`skill_id` ASC) VISIBLE,
  INDEX `fk_job_ads_has_skills_job_ads1_idx` (`job_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_has_skills_job_ads1`
    FOREIGN KEY (`job_ad_id`)
    REFERENCES `final_project`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_has_skills_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `final_project`.`skills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`match_requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`match_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `job_ad_id` INT(11) NOT NULL,
  `company_ad_id` INT(11) NOT NULL,
  `company_match` TINYINT(1) NOT NULL,
  `professional_match` TINYINT(1) NOT NULL,
  `requester` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_match_requests_job_ads1_idx` (`job_ad_id` ASC) VISIBLE,
  INDEX `fk_match_requests_company_ads1_idx` (`company_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_match_requests_company_ads1`
    FOREIGN KEY (`company_ad_id`)
    REFERENCES `final_project`.`company_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_requests_job_ads1`
    FOREIGN KEY (`job_ad_id`)
    REFERENCES `final_project`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `final_project`.`professional_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `final_project`.`professional_info` (
  `summary` VARCHAR(45) NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `status` TINYINT(1) NULL DEFAULT NULL,
  `logo` BLOB NULL DEFAULT NULL,
  `professionals_id` INT(11) NOT NULL,
  PRIMARY KEY (`professionals_id`),
  INDEX `fk_professional_info_professionals1_idx` (`professionals_id` ASC) VISIBLE,
  CONSTRAINT `fk_professional_info_professionals1`
    FOREIGN KEY (`professionals_id`)
    REFERENCES `final_project`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

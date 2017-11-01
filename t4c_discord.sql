--
-- Structure de la table `discord_logchat`
--

DROP TABLE IF EXISTS `discord_logchat`;
CREATE TABLE IF NOT EXISTS `discord_logchat` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `TIMESTAMP` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `PLAYER` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `MESSAGE` varchar(500) CHARACTER SET latin1 DEFAULT NULL,
  `CHANNEL` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `discord_logdeath`
--

DROP TABLE IF EXISTS `discord_logdeath`;
CREATE TABLE IF NOT EXISTS `discord_logdeath` (
  `ID` bigint(20) NOT NULL,
  `TIMESTAMP` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `VICTIME` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `ASSASSIN` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Déclencheurs `logdeath2`
--
DROP TRIGGER IF EXISTS `DISCORD_ONDEATH`;
DELIMITER $$
CREATE TRIGGER `DISCORD_ONDEATH` AFTER INSERT ON `logdeath2` FOR EACH ROW BEGIN
	INSERT INTO discord_logdeath (`TIMESTAMP`, `VICTIME`, `ASSASSIN`) VALUES (NEW.TimeStamp, NEW.Victime, NEW.Assassin);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Déclencheurs `logshouts`
--
DROP TRIGGER IF EXISTS `DISCORD_ONSHOUT`;
DELIMITER $$
CREATE TRIGGER `DISCORD_ONSHOUT` AFTER INSERT ON `logshouts` FOR EACH ROW BEGIN
	INSERT INTO discord_logchat (TIMESTAMP, PLAYER, MESSAGE, CHANNEL)
    VALUES (NEW.TimeStamp, 
			SUBSTRING_INDEX(SUBSTRING_INDEX(NEW.LogInfo, ' ', 2), ' ', -1), 
			SUBSTRING_INDEX(NEW.LogInfo, SUBSTRING_INDEX(NEW.LogInfo, ':', 1), -1), 
			SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(NEW.LogInfo, ' ', 7),' ',-1), ':',1));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Déclencheurs `onlineusers`
--
DROP TRIGGER IF EXISTS `PLAYTIME_OVER`;
DELIMITER $$
CREATE TRIGGER `PLAYTIME_OVER` BEFORE DELETE ON `onlineusers` FOR EACH ROW BEGIN
	UPDATE `playtime` SET `ONLINE` = 0, `LOGOFF` = CURRENT_TIME WHERE `PLAYER`=OLD.PlayerName AND `ONLINE` = 1;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `PLAYTIME_START`;
DELIMITER $$
CREATE TRIGGER `PLAYTIME_START` AFTER UPDATE ON `onlineusers` FOR EACH ROW BEGIN
	IF NEW.PlayerName != '<logging on>' THEN
    	INSERT INTO `playtime` (`PLAYER`, `ONLINE`, `LOGON`, `LOGOFF`, `PLAYTIME`, `LASTUPDATE`)
VALUES(NEW.PlayerName, 1, CURRENT_TIME, 0, 0, CURRENT_TIME);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `playtime`
--

DROP TABLE IF EXISTS `playtime`;
CREATE TABLE IF NOT EXISTS `playtime` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `PLAYER` varchar(50) NOT NULL,
  `ONLINE` tinyint(1) NOT NULL,
  `LOGON` datetime NOT NULL,
  `LOGOFF` datetime NOT NULL,
  `PLAYTIME` bigint(20) NOT NULL,
  `LASTUPDATE` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

DELIMITER $$
--
-- Procédures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `CALCULATE_PLAYTIME` ()  BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE l_playtime BIGINT(20);
  DECLARE l_player VARCHAR(50);
  DECLARE cur1 CURSOR FOR SELECT `PLAYER`, `PLAYTIME` FROM `playtime` WHERE `ONLINE` = 1;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN cur1;

  read_loop: LOOP
    FETCH cur1 INTO l_player,l_playtime;
    IF done THEN
      LEAVE read_loop;
    END IF;
    UPDATE `playtime` SET `LASTUPDATE`=CURRENT_TIME, `PLAYTIME`=l_playtime+60 WHERE `PLAYER`=l_player AND `ONLINE` = 1;
  END LOOP;
  COMMIT;
  CLOSE cur1;
END$$

DELIMITER ;
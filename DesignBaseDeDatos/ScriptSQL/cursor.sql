DELIMITER //
CREATE OR REPLACE PROCEDURE reporte(in fchIn DATE, in fchFin DATE) 
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE ci INT;
    DECLARE cur1 CURSOR FOR SELECT carnet FROM USUARIO;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur1;
        bucle: LOOP
            FETCH cur1 INTO ci;
            IF done = 1 THEN
                LEAVE bucle;
            END IF;
            SELECT * FROM REGISTRO WHERE carnet = ci and fecha BETWEEN fchIn AND fchFin order by fecha asc;
        END LOOP bucle;
    CLOSE cur1;
END // 
DELIMITER ;
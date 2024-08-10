-- creates a safe div that divides the first and second number
DELIMITER //
CREATE FUNCTION SafeDiv (a INT, b INT) RETURNS FLOAT DETERMINISTIC
BEGIN
    IF (b = 0) THEN
        RETURN 0;
    ELSE
        RETURN a/b;
    END IF;
END //
DELIMITER ;


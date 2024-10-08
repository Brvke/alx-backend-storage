-- creates an average
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE average float;
    SELECT AVG(score) INTO average FROM corrections WHERE corrections.user_id = user_id;
    UPDATE users
    SET users.average_score = average
    WHERE users.id = user_id;
END //
DELIMITER ;


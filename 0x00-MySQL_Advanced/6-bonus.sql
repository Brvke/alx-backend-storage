-- creates a stored procedure AddBonus that adds a new correction for a studen
DELIMITER //
CREATE PROCEDURE AddBonus (IN user_id INT, project_name VARCHAR(255), score INT)
BEGIN
    DECLARE project_id INT;
    IF ((SELECT COUNT(*) AS num_rows FROM projects WHERE projects.name = project_name) = 0) THEN 
        INSERT INTO `projects`(`name`)
        VALUE (project_name);
    END IF;
    
    SELECT projects.id INTO project_id FROM projects WHERE projects.name = project_name;
    INSERT INTO `corrections`(`user_id`, `project_id`, `score`)
    VALUES (user_id, project_id, score);
END //
DELIMITER ;


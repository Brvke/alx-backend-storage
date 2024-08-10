-- index first name and score
ALTER TABLE names ADD INDEX idx_name_first_score (name(1), score);


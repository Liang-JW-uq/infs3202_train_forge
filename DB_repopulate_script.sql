-- =========================
-- RESET
-- =========================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE workout_exercises;
TRUNCATE TABLE workouts;
TRUNCATE TABLE tags_exercises;
TRUNCATE TABLE exercises;
TRUNCATE TABLE clients;
TRUNCATE TABLE tags;
TRUNCATE TABLE user_trainers;s

SET FOREIGN_KEY_CHECKS = 1;


-- =========================
-- TRAINERS
-- =========================
INSERT INTO user_trainers 
(username, PASSWORD, email, first_name, last_name, 
 is_trainer, is_active, is_staff, is_superuser, date_joined)
VALUES
('trainer1@email.com','pbkdf2_sha256$600000$abc123xyz$uQwK8Jp0zJ7h6F2mVw0QkK5sP6Q9ZxYx8zQfF3Yk1k8=','trainer1@email.com','John','Tan',1,1,0,0,NOW()),
('trainer2@email.com','pbkdf2_sha256$600000$abc123xyz$uQwK8Jp0zJ7h6F2mVw0QkK5sP6Q9ZxYx8zQfF3Yk1k8=','trainer2@email.com','Sarah','Lim',1,1,0,0,NOW()),
('trainer3@email.com','pbkdf2_sha256$600000$abc123xyz$uQwK8Jp0zJ7h6F2mVw0QkK5sP6Q9ZxYx8zQfF3Yk1k8=','trainer3@email.com','David','Wong',1,1,0,0,NOW());


-- =========================
-- TAGS
-- =========================
INSERT INTO tags (name, trainer_id) VALUES
('Slimming',1),('Body Build',1),('Muscle Toning',1),('Upper Body',1),('Lower Body',1),('Biceps',1),('Calves',1),
('Slimming',2),('Body Build',2),('Muscle Toning',2),('Upper Body',2),('Lower Body',2),('Biceps',2),('Calves',2),
('Slimming',3),('Body Build',3),('Muscle Toning',3),('Upper Body',3),('Lower Body',3),('Biceps',3),('Calves',3);


-- =========================
-- EXERCISES
-- =========================
INSERT INTO exercises 
(name, instructions, def_sets, def_reps, def_weight, def_duration, trainer_id)
VALUES
-- Trainer 1
('Bench Press','Proper form',3,10,40,0,1),
('Push Up','Standard',3,15,0,0,1),
('Pull Up','Full range',3,8,0,0,1),
('Bicep Curl','Dumbbells',3,12,10,0,1),
('Tricep Dip','Bodyweight',3,12,0,0,1),
('Squat','Barbell',4,10,60,0,1),
('Lunges','Alternating',3,12,10,0,1),
('Deadlift','Keep back straight',4,8,80,0,1),
('Calf Raise','Controlled',3,15,20,0,1),
('Leg Press','Machine',3,12,80,0,1),
('Running','Treadmill',0,0,0,20,1),
('Cycling','Bike',0,0,0,25,1),
('Jump Rope','Skipping',0,0,0,10,1),
('Plank','Hold',0,0,0,5,1),
('Mountain Climbers','Fast pace',0,0,0,10,1),
('Burpees','Full body',3,10,0,0,1),

-- Trainer 2
('Bench Press','Proper form',3,10,40,0,2),
('Push Up','Standard',3,15,0,0,2),
('Pull Up','Full range',3,8,0,0,2),
('Bicep Curl','Dumbbells',3,12,10,0,2),
('Tricep Dip','Bodyweight',3,12,0,0,2),
('Squat','Barbell',4,10,60,0,2),
('Lunges','Alternating',3,12,10,0,2),
('Deadlift','Keep back straight',4,8,80,0,2),
('Calf Raise','Controlled',3,15,20,0,2),
('Leg Press','Machine',3,12,80,0,2),
('Running','Treadmill',0,0,0,20,2),
('Cycling','Bike',0,0,0,25,2),
('Jump Rope','Skipping',0,0,0,10,2),
('Plank','Hold',0,0,0,5,2),
('Mountain Climbers','Fast pace',0,0,0,10,2),
('Burpees','Full body',3,10,0,0,2),

-- Trainer 3
('Bench Press','Proper form',3,10,40,0,3),
('Push Up','Standard',3,15,0,0,3),
('Pull Up','Full range',3,8,0,0,3),
('Bicep Curl','Dumbbells',3,12,10,0,3),
('Tricep Dip','Bodyweight',3,12,0,0,3),
('Squat','Barbell',4,10,60,0,3),
('Lunges','Alternating',3,12,10,0,3),
('Deadlift','Keep back straight',4,8,80,0,3),
('Calf Raise','Controlled',3,15,20,0,3),
('Leg Press','Machine',3,12,80,0,3),
('Running','Treadmill',0,0,0,20,3),
('Cycling','Bike',0,0,0,25,3),
('Jump Rope','Skipping',0,0,0,10,3),
('Plank','Hold',0,0,0,5,3),
('Mountain Climbers','Fast pace',0,0,0,10,3),
('Burpees','Full body',3,10,0,0,3);


-- =========================
-- CLIENTS
-- =========================
INSERT INTO clients 
(name, email, age, height, weight, goals, preferred_times, trainer_id)
VALUES
('John Carter','john1@email.com',28,1.75,75,'Build muscle','Morning',1),
('Alice Tan','alice1@email.com',24,1.60,55,'Slim down','Evening',1),
('Michael Lee','mike1@email.com',35,1.80,85,'Strength','Afternoon',1),
('Sarah Lim','sarah2@email.com',29,1.65,60,'Tone','Morning',2),
('David Wong','david2@email.com',40,1.78,90,'Lose weight','Evening',2),
('Kevin Goh','kevin3@email.com',31,1.70,70,'Maintain','Night',3),
('Emma Ong','emma3@email.com',26,1.58,52,'Slimming','Morning',3);


-- =========================
-- WORKOUTS (FIXED)
-- =========================
INSERT INTO workouts (trainer_id, client_id, scheduled_date, is_completed)
VALUES
(1,1,NOW(),0),
(2,4,NOW(),0);


-- =========================
-- WORKOUT EXERCISES (FIXED)
-- =========================
INSERT INTO workout_exercises
(workout_id, exercise_id, pre_sets, pre_reps, pre_weight, actual_sets, actual_reps, actual_weight)
VALUES
(1,1,3,10,40,3,10,40),
(1,2,3,15,0,3,12,0),
(2,17,3,10,40,3,8,40),
(2,18,3,15,0,2,10,0);


-- =========================
-- TAGS ↔ EXERCISES (SAFE)
-- =========================
INSERT IGNORE INTO tags_exercises (exercise_id, tag_id)

SELECT e.id, t.id
FROM exercises e
JOIN tags t ON t.trainer_id = e.trainer_id
WHERE
(e.name='Bench Press' AND t.name IN ('Upper Body','Body Build','Biceps')) OR
(e.name='Push Up' AND t.name IN ('Upper Body','Muscle Toning')) OR
(e.name='Pull Up' AND t.name IN ('Upper Body','Biceps')) OR
(e.name='Bicep Curl' AND t.name IN ('Biceps','Muscle Toning')) OR
(e.name='Tricep Dip' AND t.name='Upper Body') OR
(e.name='Squat' AND t.name IN ('Lower Body','Body Build')) OR
(e.name='Lunges' AND t.name IN ('Lower Body','Muscle Toning')) OR
(e.name='Deadlift' AND t.name IN ('Lower Body','Body Build')) OR
(e.name='Calf Raise' AND t.name IN ('Calves','Lower Body')) OR
(e.name='Leg Press' AND t.name IN ('Lower Body','Body Build')) OR
(e.name='Running' AND t.name IN ('Slimming','Lower Body')) OR
(e.name='Cycling' AND t.name IN ('Slimming','Lower Body')) OR
(e.name='Jump Rope' AND t.name='Slimming') OR
(e.name='Plank' AND t.name='Muscle Toning') OR
(e.name='Mountain Climbers' AND t.name IN ('Slimming','Muscle Toning')) OR
(e.name='Burpees' AND t.name IN ('Slimming','Body Build'));
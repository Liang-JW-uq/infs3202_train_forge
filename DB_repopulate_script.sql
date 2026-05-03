-- 1. CLIENTS 
-- ----------
INSERT INTO clients (NAME, goals, weight, height, age, preferred_times, email, trainer_id) VALUES
('Client 1 T1', 'I want to slim down', 123, 1.5, 35, 'Morning', 'client1@email.com', 2),


-- 2. TAGS
-- -------
INSERT INTO tags (NAME, trainer_id) VALUES
('Slimming T1', 2), 
('Muscle Build T1', 2), 
('Endurance T1', 2), 
('Upper Body T1', 2), 
('Lower Body T1', 2), 
('Core Stability T1', 2), 
('Explosive T1', 2), 
('Bodyweight T1', 2), 
('Cardio T1', 2), 
('Strength T1', 2), 
('Push T1', 2), 
('Pull T1', 2), 
('Legs T1', 2);


-- 3. EXERCISES
-- ------------
INSERT INTO exercises (NAME, instructions, def_sets, def_reps, def_weight, def_duration, trainer_id) VALUES
('Barbell Squat T1', 'Bar on traps. Squat deep, keep back straight.', 4, 10, 60.00, 0, 2),
('Deadlift T1', 'Hinge at hips. Lift using legs and back.', 5, 5, 100.00, 0, 2),
('Bench Press T1', 'Lower bar to mid-chest. Push explosively.', 4, 8, 50.00, 0, 2),
('Overhead Press T1', 'Press bar from shoulders to lock-out overhead.', 3, 10, 30.00, 0, 2),
('Barbell Rows T1', 'Hinge forward, pull bar to mid-waist.', 4, 10, 40.00, 0, 2),
('Romanian Deadlift T1', 'Hinge at hips, feel hamstring stretch.', 3, 12, 50.00, 0, 2),
('Barbell Hip Thrusts T1', 'Drive hips upward, squeeze glutes.', 4, 12, 60.00, 0, 2),
('Incline DB Press T1', 'Press dumbbells up from an inclined bench.', 3, 10, 20.00, 0, 2),
('DB Shoulder Press T1', 'Seated press, start at ear level.', 3, 12, 18.00, 0, 2),
('DB Lateral Raises T1', 'Lift dumbbells out to sides to shoulder height.', 4, 15, 7.50, 0, 2),
('DB Bicep Curls T1', 'Alternating arms, rotate palm up.', 3, 12, 12.00, 0, 2),
('Hammer Curls T1', 'Neutral grip (palms in).', 3, 12, 12.00, 0, 2),
('DB Bulgarian Split Squats T1', 'One foot elevated on bench.', 3, 10, 10.00, 0, 2),
('DB Goblet Squats T1', 'Hold one dumbbell at chest level.', 3, 15, 20.00, 0, 2),
('DB Lunges T1', 'Step forward, keeping torso upright.', 3, 20, 15.00, 0, 2),
('DB Tricep Extensions T1', 'Hold DB behind head, extend upward.', 3, 12, 15.00, 0, 2),
('Lat Pulldown T1', 'Pull bar to upper chest.', 4, 10, 45.00, 0, 2),
('Leg Press T1', 'Push platform with mid-foot.', 4, 12, 120.00, 0, 2),
('Leg Extensions T1', 'Extend legs fully on machine.', 3, 15, 30.00, 0, 2),
('Seated Leg Curls T1', 'Curl legs toward glutes.', 3, 15, 25.00, 0, 2),
('Cable Pushdowns T1', 'Use rope attachment. Squeeze triceps.', 3, 15, 20.00, 0, 2),
('Seated Cable Row T1', 'Pull handle to stomach.', 3, 12, 40.00, 0, 2),
('Pec Deck Flys T1', 'Bring handles together in front of chest.', 3, 12, 35.00, 0, 2),
('Cable Face Pulls T1', 'Pull rope toward forehead.', 4, 20, 15.00, 0, 2),
('Assault Bike T1', 'Max effort push/pull for 30s.', 8, 0, 0.00, 10, 2),
('StairMaster T1', 'Continuous climbing.', 0, 0, 0.00, 20, 2),
('Rowing Machine T1', 'Drive with legs, pull to ribs.', 0, 0, 0.00, 15, 2),
('Kettlebell Swings T1', 'Snap hips forward to swing bell.', 4, 25, 16.00, 0, 2),
('Burpees T1', 'Chest to floor, jump up.', 4, 15, 0.00, 0, 2),
('Box Jumps T1', 'Jump onto box, land softly.', 3, 10, 0.00, 0, 2),
('Battle Ropes T1', 'Alternating waves.', 5, 0, 0.00, 1, 2),
('Mountain Climbers T1', 'Drive knees to chest rapidly.', 4, 0, 0.00, 1, 2),
('Jump Rope T1', 'Continuous jumping.', 5, 0, 0.00, 3, 2),
('Pull Ups T1', 'Hang from bar, pull chest to bar.', 3, 10, 0.00, 0, 2),
('Chin Ups T1', 'Underhand grip. Targets biceps.', 3, 10, 0.00, 0, 2),
('Dips T1', 'Lower body between parallel bars.', 3, 12, 0.00, 0, 2),
('Push Ups T1', 'Standard chest-to-floor.', 4, 20, 0.00, 0, 2),
('Plank T1', 'Hold straight line on elbows.', 3, 0, 0.00, 2, 2),
('Hanging Leg Raises T1', 'Lift legs to 90 degrees.', 3, 15, 0.00, 0, 2),
('Russian Twists T1', 'Rotate torso side to side.', 3, 30, 5.00, 0, 2),
('Ab Wheel Rollouts T1', 'Roll forward keeping back flat.', 3, 12, 0.00, 0, 2),
('Walking Lunges T1', 'Step forward alternating legs.', 3, 24, 0.00, 0, 2),
('Bicycle Crunches T1', 'Rotate elbow to opposite knee.', 3, 40, 0.00, 0, 2),
('Wall Sits T1', 'Back against wall, thighs parallel.', 3, 0, 0.00, 1, 2),
('Bird Dog T1', 'Extend opposite arm/leg.', 3, 12, 0.00, 0, 2);



-- 4. JUNCTION TABLE
-- -----------------
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 2 FROM exercises WHERE id BETWEEN 1 AND 24;
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 10 FROM exercises WHERE id IN (1, 2, 3, 4, 5, 7, 18);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 1 FROM exercises WHERE id IN (25, 26, 27, 28, 29, 31, 32, 33, 42);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 9 FROM exercises WHERE id IN (25, 26, 27, 29, 32, 33);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 3 FROM exercises WHERE id IN (25, 26, 27, 28, 31, 38, 42, 44);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 4 FROM exercises WHERE id IN (3, 4, 5, 8, 9, 10, 11, 12, 16, 17, 21, 22, 23, 24, 34, 35, 36, 37);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 5 FROM exercises WHERE id IN (1, 2, 6, 7, 13, 14, 15, 18, 19, 20, 42, 44);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 11 FROM exercises WHERE id IN (1, 3, 4, 8, 9, 16, 18, 19, 21, 23, 36, 37, 44);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 12 FROM exercises WHERE id IN (2, 5, 6, 7, 11, 12, 17, 20, 22, 24, 34, 35);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 13 FROM exercises WHERE NAME IN ('Barbell Squat', 'Romanian Deadlift', 'Barbell Hip Thrusts', 'Leg Press', 'Leg Extensions', 'Seated Leg Curls', 'DB Bulgarian Split Squats', 'DB Goblet Squats');
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 6 FROM exercises WHERE id IN (38, 39, 40, 41, 43, 45, 27, 32);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 7 FROM exercises WHERE id IN (1, 3, 25, 28, 29, 30, 31);
INSERT INTO tags_exercises (exercise_id, tag_id) SELECT id, 8 FROM exercises WHERE id IN (29, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45);
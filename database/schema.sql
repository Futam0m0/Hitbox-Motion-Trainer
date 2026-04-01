CREATE TABLE Player(
    player_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL

);

CREATE TABLE TrainingSession(
    session_id INT PRIMARY KEY,
    player_id INT,
    start_time DATETIME,
    end_time DATETIME,

    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

CREATE TABLE MotionDefinition(
    motion_id INT PRIMARY KEY,
    motion_name VARCHAR(50) NOT NULL,
    motion_description VARCHAR(100) NOT NULL    
);

CREATE TABLE MotionAttempt(
    attempt_id INT PRIMARY KEY,
    session_id INT,
    motion_id INT,
    success BIT,
    execution_time FLOAT

    FOREIGN KEY (session_id) REFERENCES TrainingSession(session_id),
    FOREIGN KEY (motion_id) REFERENCES MotionDefinition(motion_id)
);

CREATE TABLE MotionStep(
    motion_id INT,
    step_order INT,
    direction VARCHAR(50) NOT NULL,

    PRIMARY KEY (motion_id, step_order),

    FOREIGN KEY (motion_id) REFERENCES MotionDefinition(motion_id)
);

CREATE TABLE InputEvent(
    event_id INT PRIMARY KEY,
    session_id INT,
    direction VARCHAR(50) NOT NULL,
    time_stamp DATETIME NOT NULL,

    FOREIGN KEY (session_id) REFERENCES TrainingSession(session_id)
);

CREATE TABLE Controller(
    controller_id INT PRIMARY KEY,
    controller_name VARCHAR(50) NOT NULL,
    controller_type VARCHAR(50) NOT NULL
);

CREATE TABLE ButtonMapping(
    mapping_id INT PRIMARY KEY,
    controller_id INT,
    button_name VARCHAR(50) NOT NULL,
    direction VARCHAR(50) NOT NULL,

    FOREIGN KEY (controller_id) REFERENCES Controller(controller_id)
);

CREATE TABLE SessionSummary(
    session_id INT PRIMARY KEY,
    total_attempts INT,
    success_rate FLOAT,

    FOREIGN KEY (session_id) REFERENCES TrainingSession(session_id)
);

CREATE TABLE UserSettings(
    settings_id INT PRIMARY KEY,
    player_id INT,
    difficulty_level VARCHAR(20) NOT NULL,
    preferred_controller VARCHAR(50) NOT NULL,

    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);
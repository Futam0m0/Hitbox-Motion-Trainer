create table Player(
    player_id int not null,
    username varchar(50) not null,
    created_at datetime not null,

    primary key(player_id)
)


create table TrainingSession(
    session_id int identity(1,1),
    player_id int,
    start_time datetime,
    end_time datetime,

    primary key(session_id),
    foreign key (player_id) references Player(player_id)
    on delete set null on update cascade
)

create table MotionDefinition(
    motion_id int identity(1,1)not null,
    motion_name varchar(50) not null,
    motion_description varchar(100) not null ,

    primary key(motion_id)   
)

--list of special moves
insert into Motiondefinition(motion_name,motion_description)
values ('QCF','Quarter Circle Forward')

insert into Motiondefinition(motion_name,motion_description)
values ('DP','Dragon Punch')

create table MotionAttempt(
    attempt_id int identity(1,1) not null,
    session_id int,
    motion_id int,
    success bit not null,
    execution_time float check (execution_time >= 0),

    primary key(attempt_id),

    foreign key (session_id) references TrainingSession(session_id)
    on delete cascade on update cascade,
    foreign key (motion_id) references MotionDefinition(motion_id)
    on delete cascade on update cascade
)

create table MotionStep(
    motion_id int not null,
    step_order int check (step_order > 0),
    direction varchar(50) not null,
    min_frames int default 0 check (min_frames >= 0),

    primary key (motion_id, step_order),

    foreign key (motion_id) references MotionDefinition(motion_id)
    on delete cascade on update cascade
)
-- data for steps 
insert into MotionDefinition (motion_name, motion_description) values
('DP', 'Dragon Punch (Forward, Down, Down-Forward)'),
('QCB', 'Quarter Circle Back'),
('HCF', 'Half Circle Forward'),
('Sonic Boom', 'Charge Back -> Forward'),
('Flash Kick', 'Charge Down -> Up');
go

-- QCB (Let's assume ID 3)
insert into MotionStep (motion_id, step_order, direction, min_frames) values
(3, 1, 'Down', 0),
(3, 2, 'Down-Back', 0),
(3, 3, 'Back', 0);

-- HCF (ID 4)
insert into MotionStep (motion_id, step_order, direction, min_frames) values
(4, 1, 'Back', 0),
(4, 2, 'Down-Back', 0),
(4, 3, 'Down', 0),
(4, 4, 'Down-Forward', 0),
(4, 5, 'Forward', 0);

-- Sonic Boom (ID 5) - Charge Back (40 frames) -> Forward
insert into MotionStep (motion_id, step_order, direction, min_frames) values
(5, 1, 'Back', 40),
(5, 2, 'Forward', 0);

-- Flash Kick (ID 6) - Charge Down (50 frames) -> Up
insert into MotionStep (motion_id, step_order, direction, min_frames) values
(6, 1, 'Down', 50),
(6, 2, 'Up', 0);




create table InputEvent(
    event_id int not null,
    session_id int,
    direction varchar(50) not null,
    time_stamp datetime not null,

    primary key(event_id),
    foreign key (session_id) references TrainingSession(session_id)
    on delete cascade on update cascade
)

create table Controller(
    controller_id int not null,
    controller_name varchar(50) not null,
    controller_type varchar(50) not null,

    primary key(controller_id)
)

create table ButtonMapping(
    mapping_id int not null,
    controller_id int,
    button_name varchar(50) not null,
    direction varchar(50) not null,

    primary key(mapping_id),
    foreign key (controller_id) references Controller(controller_id)
    on delete cascade on update cascade
)

create table SessionSummary(
    session_id int not null,
    total_attempts int check (total_attempts >= 0),
    success_rate decimal(5,2) check (success_rate >= 0 and success_rate <= 100),
    
    primary key(session_id),
    foreign key (session_id) references TrainingSession(session_id)
    on delete cascade on update cascade
)

create table UserSettings(
    settings_id int not null,
    player_id int,
    difficulty_level varchar(20) not null,
    preferred_controller varchar(50) not null,

    primary key(settings_id),
    foreign key (player_id) references Player(player_id)
    on delete cascade on update cascade
)

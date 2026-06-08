create index IX_MotionAttempt_MotionID_Success on MotionAttempt (motion_id, success);
create index IX_MotionAttempt_SessionID on MotionAttempt (session_id);

---------------------------------

create index IX_MotionAttempt_ExecutionTime on MotionAttempt (execution_time) where success = 1;
go

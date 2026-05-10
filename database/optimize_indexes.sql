-- Optimization Indexes for Analytics Queries (Refined)
-- Indexes on foreign keys and success status for fast joining and filtering
create index IX_MotionAttempt_MotionID_Success on MotionAttempt (motion_id, success);
create index IX_MotionAttempt_SessionID on MotionAttempt (session_id);
-- Filtered index for performance on successful executions
create index IX_MotionAttempt_ExecutionTime on MotionAttempt (execution_time) where success = 1;
go

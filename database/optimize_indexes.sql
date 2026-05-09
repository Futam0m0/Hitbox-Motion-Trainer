-- Optimization Indexes for Analytics Queries (Refined)
-- Indexes on foreign keys and success status for fast joining and filtering
CREATE INDEX IX_MotionAttempt_MotionID_Success ON MotionAttempt (motion_id, success);
CREATE INDEX IX_MotionAttempt_SessionID ON MotionAttempt (session_id);
-- Filtered index for performance on successful executions
CREATE INDEX IX_MotionAttempt_ExecutionTime ON MotionAttempt (execution_time) WHERE success = 1;
GO

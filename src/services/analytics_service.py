from db import connection

def get_motion_statistics():
    """
    Returns statistics for each motion using JOINS and CASE statements.
    Demonstrates: JOIN, GROUP BY, CASE logic.
    """
    conn = connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        md.motion_name,
        COUNT(ma.attempt_id) AS total_attempts,
        SUM(CASE WHEN ma.success = 1 THEN 1 ELSE 0 END) AS successful_attempts,
        CAST(SUM(CASE WHEN ma.success = 1 THEN 1.0 ELSE 0.0 END) / NULLIF(COUNT(ma.attempt_id), 0) * 100 AS DECIMAL(5,2)) AS success_rate,
        AVG(CASE WHEN ma.success = 1 THEN ma.execution_time ELSE NULL END) AS avg_execution_time
    FROM MotionDefinition md
    LEFT JOIN MotionAttempt ma ON md.motion_id = ma.motion_id
    GROUP BY md.motion_id, md.motion_name
    ORDER BY success_rate DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_session_statistics():
    """
    Returns per-session statistics using SUBQUERIES and GROUP BY/HAVING.
    Demonstrates: GROUP BY, HAVING, SUBQUERY.
    """
    conn = connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        ts.session_id,
        ts.start_time,
        stats.attempts,
        stats.success_rate,
        stats.avg_time
    FROM TrainingSession ts
    JOIN (
        SELECT 
            session_id,
            COUNT(*) AS attempts,
            CAST(SUM(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100 AS DECIMAL(5,2)) AS success_rate,
            AVG(CASE WHEN success = 1 THEN execution_time ELSE NULL END) AS avg_time
        FROM MotionAttempt
        GROUP BY session_id
        HAVING COUNT(*) > 0
    ) AS stats ON ts.session_id = stats.session_id
    ORDER BY ts.start_time DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_motion_rankings():
    """
    Ranks successful attempts using WINDOW FUNCTIONS.
    Demonstrates: RANK(), ROW_NUMBER(), AVG() OVER().
    """
    conn = connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        md.motion_name,
        ma.execution_time,
        RANK() OVER (PARTITION BY md.motion_id ORDER BY ma.execution_time ASC) as local_rank,
        AVG(ma.execution_time) OVER (PARTITION BY md.motion_id) as motion_avg_time,
        ma.execution_time - AVG(ma.execution_time) OVER (PARTITION BY md.motion_id) as diff_from_avg
    FROM MotionAttempt ma
    JOIN MotionDefinition md ON ma.motion_id = md.motion_id
    WHERE ma.success = 1;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_consistency_report():
    """
    Generates a consistency report using CTEs to track improvement.
    Demonstrates: CTE (Common Table Expressions).
    """
    conn = connection()
    cursor = conn.cursor()
    
    query = """
    WITH SessionProgress AS (
        SELECT 
            ma.session_id,
            md.motion_name,
            AVG(CASE WHEN ma.success = 1 THEN ma.execution_time ELSE NULL END) as session_avg,
            ROW_NUMBER() OVER (PARTITION BY md.motion_id ORDER BY ma.session_id ASC) as session_order
        FROM MotionAttempt ma
        JOIN MotionDefinition md ON ma.motion_id = md.motion_id
        GROUP BY ma.session_id, md.motion_id, md.motion_name
    )
    SELECT 
        motion_name,
        session_order,
        session_avg,
        session_avg - LAG(session_avg) OVER (PARTITION BY motion_name ORDER BY session_order) as improvement
    FROM SessionProgress;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_running_averages():
    """
    Calculates running average of execution times using WINDOW FUNCTIONS.
    Demonstrates: AVG() OVER (ORDER BY ... ROWS BETWEEN ...).
    """
    conn = connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        md.motion_name,
        ma.attempt_id,
        ma.execution_time,
        AVG(ma.execution_time) OVER (
            PARTITION BY md.motion_id 
            ORDER BY ma.attempt_id 
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) as moving_avg_5_attempts
    FROM MotionAttempt ma
    JOIN MotionDefinition md ON ma.motion_id = md.motion_id
    WHERE ma.success = 1;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

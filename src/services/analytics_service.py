from db import connection

def get_motion_statistics():
    """
    Returns statistics for each motion using JOINS and CASE statements.
    Demonstrates: JOIN, GROUP BY, CASE logic.
    """
    conn = connection()
    cursor = conn.cursor()
    
    query = """
    select 
        md.motion_name,
        count(ma.attempt_id) as total_attempts,
        sum(CASE WHEN ma.success = 1 THEN 1 ELSE 0 END) as successful_attempts,
        cast(sum(CASE WHEN ma.success = 1 THEN 1.0 ELSE 0.0 END) / NULLIF(count(ma.attempt_id), 0) * 100 AS DECIMAL(5,2)) as success_rate,
        avg(CASE WHEN ma.success = 1 THEN ma.execution_time ELSE NULL END) as avg_execution_time
    from MotionDefinition md
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
    select 
        ts.session_id,
        ts.start_time,
        stats.attempts,
        stats.success_rate,
        stats.avg_time
    from TrainingSession ts
    join (
        select 
            session_id,
            count(*) as attempts,
            cast(sum(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) / count(*) * 100 AS DECIMAL(5,2)) as success_rate,
            avg(CASE WHEN success = 1 THEN execution_time ELSE NULL END) as avg_time
        from MotionAttempt
        group by session_id
        having count(*) > 0
    ) as stats on ts.session_id = stats.session_id
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
    select 
        md.motion_name,
        ma.execution_time,
        rank() over (partition by md.motion_id order by ma.execution_time asc) as local_rank,
        avg(ma.execution_time) over (partition by md.motion_id) as motion_avg_time,
        ma.execution_time - avg(ma.execution_time) over (partition by md.motion_id) as diff_from_avg
    from MotionAttempt ma
    join MotionDefinition md on ma.motion_id = md.motion_id
    where ma.success = 1;
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
    with SessionProgress as (
        select 
            ma.session_id,
            md.motion_name,
            avg(CASE WHEN ma.success = 1 THEN ma.execution_time ELSE NULL END) as session_avg,
            row_number() over (partition by md.motion_id order by ma.session_id asc) as session_order
        from MotionAttempt ma
        join MotionDefinition md on ma.motion_id = md.motion_id
        group by ma.session_id, md.motion_id, md.motion_name
    )
    select 
        motion_name,
        session_order,
        session_avg,
        session_avg - lag(session_avg) over (partition by motion_name order by session_order) as improvement
    from SessionProgress
    where session_order > 1
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
    select 
        md.motion_name,
        ma.attempt_id,
        ma.execution_time,
        avg(ma.execution_time) over (
            partition by md.motion_id 
            order by ma.attempt_id 
            rows between 4 preceding and current row
        ) as moving_avg_5_attempts
    from MotionAttempt ma
    join MotionDefinition md on ma.motion_id = md.motion_id
    where ma.success = 1;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

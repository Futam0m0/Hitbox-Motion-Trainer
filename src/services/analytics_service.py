from db import connection

def get_motion_statistics():

    conn = connection()
    cursor = conn.cursor()
    
    query = """
    select 
        md.motion_name,
        count(ma.attempt_id) as total_attempts,
        sum(case when ma.success = 1 then 1 else 0 end) as successful_attempts,
        cast(sum(case when ma.success = 1 then 1.0 else 0.0 end) / nullif(count(ma.attempt_id), 0) * 100 as decimal(5,2)) as success_rate,
        avg(case when ma.success = 1 then ma.execution_time else null end) as avg_execution_time
    from MotionDefinition md
    left join MotionAttempt ma on md.motion_id = ma.motion_id
    group by md.motion_id, md.motion_name
    order by success_rate DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_session_statistics():

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
            cast(sum(case when success = 1 then 1.0 else 0.0 end) / count(*) * 100 as decimal(5,2)) as success_rate,
            avg(case when success = 1 then execution_time else null end) as avg_time
        from MotionAttempt
        group by session_id
        having count(*) > 0
    ) as stats on ts.session_id = stats.session_id
    order by ts.start_time DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_motion_rankings():

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

    conn = connection()
    cursor = conn.cursor()
    
    query = """
    with SessionProgress as (
        select 
            ma.session_id,
            md.motion_name,
            avg(case when ma.success = 1 then ma.execution_time else null end ) as session_avg,
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

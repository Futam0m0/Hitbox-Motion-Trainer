import pyodbc

def connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-40CIS8U;"
        "DATABASE=HitBoxTrainerDB;"
        "Trusted_Connection=yes;"
        "Connection Timeout=30;"
        
        )
    return conn
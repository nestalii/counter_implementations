import psycopg2

def get_connection():
    return psycopg2.connect("dbname=counter_db user=postgres password=****** host=localhost")
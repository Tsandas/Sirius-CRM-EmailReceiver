from db.postgres import get_conn, release_conn

def find_last_email_in_db():
    conn = get_conn()
    #########
    release_conn(conn)
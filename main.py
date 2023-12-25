import psycopg2
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR (200),
            last_name VARCHAR (200),
            email VARCHAR (200) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(id),
            phone_number VARCHAR(200) NOT NULL UNIQUE
        );
        """)
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email))
        client_id = cur.fetchone()
        if phones != None:
            for phone in phones:
                cur.execute("""
                INSERT INTO phones (client_id, phone_number) VALUES (%s, %s);
                """, (client_id, phone))
        return conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones (client_id, phone_number) VALUES (%s, %s);
        """, (client_id, phone))
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute("""
            UPDATE client SET first_name=%s WHERE id=%s;
            """, (first_name, client_id))
        if last_name != None:
            cur.execute("""
            UPDATE client SET last_name=%s WHERE id=%s;
            """, (last_name, client_id))
        if email != None:
            cur.execute("""
            UPDATE client SET email=%s WHERE id=%s;
            """, (email, client_id))
        conn.commit()

def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE phone_number=%s;
        """, (phone,))
        conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id=%s;
        """, (client_id,))
        cur.execute("""
        DELETE FROM client
        WHERE id=%s;
        """, (client_id,))
        conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client c
        JOIN phones p ON p.client_id = c.id
        WHERE first_name=%s OR last_name=%s OR email=%s OR phone_number=%s;
        """, (first_name, last_name, email, phone))
        return cur.fetchall()

with psycopg2.connect(database="homework", user="postgres", password="260520") as conn:
    client_bd = create_db(conn)
    client_1 = add_client(conn, 'Viktoria',' Trish', 'vik@mail.ru')
    client_1_phone = add_phone(conn, 1, 8800895278)
    client_2 = add_client(conn, 'Nina', 'Richi', 'nina2774@gmail.com')
    client_2_phone = add_phone(conn, 2, 89200214756)
    client_3 = add_client(conn, 'Eric', 'Rose', 'eric264@yd.ru')
    client_2_phone_2 = add_phone(conn, 2, 89508887152)
    updates = change_client(conn, 3, 'Eric', 'Rosarium')
    delete_ph2= delete_phone(conn, '89508887152')
    delete_cl = delete_client(conn, 3)
    delete_cl_2 = delete_client(conn, 2)
conn.close()
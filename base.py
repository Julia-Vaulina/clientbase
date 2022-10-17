import psycopg2


def new_client(cursor, name, surname, email):
    cursor.execute("""
    INSERT INTO clients(name, surname, email) 
    VALUES (%s, %s, %s) RETURNING id;
    """, (name, surname, email,))
    return cur.fetchone()


def client_number(cursor, client_id, number):
    cursor.execute("""
    INSERT INTO phones(client_id, number) 
    VALUES (%s, %s) RETURNING id;
    """, (client_id, number,))
    return cur.fetchone()


def update_client(cursor, email, name, surname, id):
    cursor.execute("""
    UPDATE clients 
    SET email=%s, name = %s, surname = %s WHERE id=%s;
    """, (email, name, surname, id,))
    cur.execute("""
    SELECT * FROM clients WHERE id=%s;
    """, (id,))
    return cur.fetchone()


def delete_client_number(cursor, client_id):
    cursor.execute("""
    DELETE FROM phones WHERE client_id=%s;""", (client_id,))
    cur.execute("""
    SELECT * FROM phones;
    """)
    return cur.fetchall()


def delete_client(cursor, id):
    cursor.execute("""
    DELETE FROM clients WHERE id=%s;""", (id,))
    cur.execute("""
    SELECT * FROM clients;
    """)
    return cur.fetchall()


def search_client(cursor, name, surname, email):
    cursor.execute("""
    SELECT clients.id, name, surname, email, number 
    FROM clients 
    JOIN phones ON clients.id = phones.client_id 
    WHERE name=%s OR surname=%s OR email=%s;
    """, (name, surname, email,))
    return cur.fetchall()


with psycopg2.connect(database="clientbase",
                      user="postgres",
                      password="") as conn:
    with conn.cursor() as cur:
        # cur.execute("""
        # DROP TABLE homework;
        # DROP TABLE course;
        # """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40),
        surname VARCHAR(40),
        email VARCHAR(40) UNIQUE);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES clients(id),
        number INTEGER NOT NULL);""")

        conn.commit()

        cur.execute("""
                INSERT INTO clients(name, surname, email)
                VALUES ('Joe', 'Smith', 'joe@gmail.com'),
                ('Barbara', 'Brown', 'barbara@gmail.com'),
                ('Ivan', 'Petrov', 'ivan@gmail.com');""")
        print(cur.fetchone())

        cur.execute("""
                        INSERT INTO phones(client_id, number)
                        VALUES (1, 123456),
                        (2, 456789),
                        (2, 789456),
                        (3, 147852);""")
        conn.commit()

        add_new_client = new_client(cur, 'Julia', 'Black', 'julia@gmail.com')
        print(add_new_client)

        add_client_number = client_number(cur, 9, 582639)
        print(add_client_number)

        update = update_client(cur, 'juli_white@gmail.com', 'Julia', 'White', 1)
        print(update)

        delete_number = delete_client_number(cur, 9)
        print(delete_number)

        del_client = delete_client(cur, 9)
        print(del_client)

        search_client = search_client(cur, 'Julia', 'Brown', 'julia_black@gmail.com')
        print(search_client)



conn.close()

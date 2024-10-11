steps = [
    [
        # "Up" SQL statement for users
        """--sql
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR NOT NULL UNIQUE,
            email VARCHAR NOT NULL UNIQUE,
            hashed_password VARCHAR NOT NULL,
            first_name VARCHAR,
            last_name VARCHAR
        );
        """,
        # "Down" SQL statement for users
        """--sql
        DROP TABLE users;
        """,
    ]
]

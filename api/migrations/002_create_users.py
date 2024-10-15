steps = [
    [
        # "Up" SQL statement for users
        """--sql
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(256) NOT NULL UNIQUE,
            hashed_password VARCHAR(256) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100)
        );
        """,
        # "Down" SQL statement for users
        """--sql
        DROP TABLE users;
        """,
    ]
]

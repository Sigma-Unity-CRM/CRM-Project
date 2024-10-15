steps = [
    [
        # "Up" SQL statement for countries
        """--sql
        CREATE TABLE countries (
            country_id SERIAL PRIMARY KEY,
            country_name VARCHAR(100) NOT NULL,
            country_code VARCHAR(3) NOT NULL UNIQUE
        );
        """,
        # "Down" SQL statement for countries
        """--sql
        DROP TABLE countries;
        """,
    ]
]

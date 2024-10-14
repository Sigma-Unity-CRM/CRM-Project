steps = [
    [
        # "Up" SQL statement for stages
        """--sql
        CREATE TABLE stages (
            stage_id SERIAL PRIMARY KEY,
            stage_name VARCHAR NOT NULL,
            description VARCHAR
        );
        """,
        # "Down" SQL statement for stages
        """--sql
        DROP TABLE stages;
        """,
    ]
]

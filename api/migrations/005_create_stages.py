steps = [
    [
        # "Up" SQL statement for stages
        """--sql
        CREATE TABLE stages (
            stage_id SERIAL PRIMARY KEY,
            stage_name VARCHAR(100) NOT NULL,
            description VARCHAR(255)
        );
        """,
        # "Down" SQL statement for stages
        """--sql
        DROP TABLE stages;
        """,
    ]
]

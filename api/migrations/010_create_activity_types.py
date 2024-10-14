steps = [
    [
        # "Up" SQL statement for activity types
        """--sql
        CREATE TABLE activity_types (
            activity_type_id SERIAL PRIMARY KEY,
            type_name VARCHAR NOT NULL,
            description VARCHAR
        );
        """,
        # "Down" SQL statement for activity_types
        """--sql
        DROP TABLE activity_types;
        """,
    ]
]

steps = [
    [
        # "Up" SQL statement for activities
        """--sql
        CREATE TABLE activities (
            activity_id SERIAL PRIMARY KEY,
            activity_type_id INTEGER NOT NULL REFERENCES activity_types(activity_type_id),
            opportunity_id INTEGER REFERENCES opportunities(opportunity_id),
            description VARCHAR,
            due_date DATE,
            completed BOOLEAN DEFAULT FALSE
        );
        """,
        # "Down" SQL statement for activities
        """--sql
        DROP TABLE activities;
        """,
    ]
]

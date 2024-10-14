steps = [
    [
        # "Up" SQL statement for opportunity_owners
        """--sql
        CREATE TABLE opportunity_owners (
            opportunity_id INTEGER NOT NULL REFERENCES opportunities(opportunity_id),
            user_id INTEGER NOT NULL REFERENCES users(user_id),
            PRIMARY KEY (opportunity_id, user_id)
        );
        """,
        # "Down" SQL statement for opportunity_owners
        """--sql
        DROP TABLE opportunity_owners;
        """,
    ]
]

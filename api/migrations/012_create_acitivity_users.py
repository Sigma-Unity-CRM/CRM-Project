steps = [
    [
        # "Up" SQL statement for activity_users
        """--sql
        CREATE TABLE activity_users (
            activity_id INTEGER NOT NULL REFERENCES activities(activity_id),
            user_id INTEGER NOT NULL REFERENCES users(user_id),
            PRIMARY KEY (activity_id, user_id)
        );
        """,
        # "Down" SQL statement for activity_users
        """--sql
        DROP TABLE activity_users;
        """,
    ]
]

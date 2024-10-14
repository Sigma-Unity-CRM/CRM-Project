steps = [
    [
        # "Up" SQL statement for activity_contacts
        """--sql
        CREATE TABLE activity_contacts (
            activity_id INTEGER NOT NULL REFERENCES activities(activity_id),
            contact_id INTEGER NOT NULL REFERENCES contacts(contact_id),
            PRIMARY KEY (activity_id, contact_id)
        );
        """,
        # "Down" SQL statement for activity_contacts
        """--sql
        DROP TABLE activity_contacts;
        """,
    ]
]

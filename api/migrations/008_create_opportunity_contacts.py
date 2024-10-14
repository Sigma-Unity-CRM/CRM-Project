steps = [
    [
        # "Up" SQL statement for opportunity_contacts
        """--sql
        CREATE TABLE opportunity_contacts (
            opportunity_id INTEGER NOT NULL REFERENCES opportunities(opportunity_id),
            contact_id INTEGER NOT NULL REFERENCES contacts(contact_id),
            PRIMARY KEY (opportunity_id, contact_id)
        );
        """,
        # "Down" SQL statement for opportunity_contacts
        """--sql
        DROP TABLE opportunity_contacts;
        """,
    ]
]

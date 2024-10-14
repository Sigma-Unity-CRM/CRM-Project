steps = [
    [
        # "Up" SQL statement for contacts
        """--sql
        CREATE TABLE contacts (
            contact_id SERIAL PRIMARY KEY,
            account_id INTEGER NOT NULL REFERENCES accounts(account_id),
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            title VARCHAR,
            email VARCHAR NOT NULL,
            primary_phone VARCHAR,
            secondary_phone VARCHAR,
            site_name VARCHAR,
            site_street_1 VARCHAR,
            site_street_2 VARCHAR,
            site_city VARCHAR,
            site_state VARCHAR,
            site_zipcode VARCHAR,
            site_country_id INTEGER REFERENCES countries(country_id)
        );
        """,
        # "Down" SQL statement for contacts
        """--sql
        DROP TABLE contacts;
        """,
    ]
]

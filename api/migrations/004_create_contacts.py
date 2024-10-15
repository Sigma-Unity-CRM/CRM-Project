steps = [
    [
        # "Up" SQL statement for contacts
        """--sql
        CREATE TABLE contacts (
            contact_id SERIAL PRIMARY KEY,
            account_id INTEGER NOT NULL REFERENCES accounts(account_id),
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            title VARCHAR(100),
            email VARCHAR(256) NOT NULL,
            primary_phone VARCHAR(20),
            secondary_phone VARCHAR(20),
            site_name VARCHAR(150),
            site_street_1 VARCHAR(100),
            site_street_2 VARCHAR(100),
            site_city VARCHAR(100),
            site_state VARCHAR(100),
            site_zipcode VARCHAR(10),
            site_country_id INTEGER REFERENCES countries(country_id)
        );
        """,
        # "Down" SQL statement for contacts
        """--sql
        DROP TABLE contacts;
        """,
    ]
]

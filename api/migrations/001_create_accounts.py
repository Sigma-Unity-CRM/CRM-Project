steps = [
    [
        # "Up" SQL statement
        """--sql
        CREATE TABLE accounts (
            account_id SERIAL PRIMARY KEY,
            parent_account_id INTEGER REFERENCES accounts(account_id),
            account_name VARCHAR NOT NULL,
            website VARCHAR,
            type VARCHAR,
            description VARCHAR,
            primary_phone VARCHAR,
            secondary_phone VARCHAR,
            billing_street_1 VARCHAR,
            billing_street_2 VARCHAR,
            billing_city VARCHAR,
            billing_state VARCHAR,
            billing_zipcode VARCHAR,
            billing_country_id INTEGER REFERENCES countries(country_id),
            shipping_street_1 VARCHAR,
            shipping_street_2 VARCHAR,
            shipping_city VARCHAR,
            shipping_state VARCHAR,
            shipping_zipcode VARCHAR,
            shipping_country_id INTEGER REFERENCES countries(country_id),
            account_owner_id INTEGER REFERENCES users(user_id)
        );
        """,
        # "Down" SQL statement
        """--sql
        DROP TABLE accounts;
        """,
    ]
]

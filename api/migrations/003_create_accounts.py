steps = [
    [
        # "Up" SQL statement
        """--sql
        CREATE TABLE accounts (
            account_id SERIAL PRIMARY KEY,
            parent_account_id INTEGER REFERENCES accounts(account_id),
            account_name VARCHAR(150) NOT NULL,
            website VARCHAR(2083),
            type VARCHAR(50),
            description VARCHAR,
            primary_phone VARCHAR(20),
            secondary_phone VARCHAR(20),
            billing_street_1 VARCHAR(100),
            billing_street_2 VARCHAR(100),
            billing_city VARCHAR(100),
            billing_state VARCHAR(100),
            billing_zipcode VARCHAR(10),
            billing_country_id INTEGER REFERENCES countries(country_id),
            shipping_street_1 VARCHAR(100),
            shipping_street_2 VARCHAR(100),
            shipping_city VARCHAR(100),
            shipping_state VARCHAR(100),
            shipping_zipcode VARCHAR(10),
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

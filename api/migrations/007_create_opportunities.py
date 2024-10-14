steps = [
    [
        # "Up" SQL statement for opportunities
        """--sql
        CREATE TABLE opportunities (
            opportunity_id SERIAL PRIMARY KEY,
            account_id INTEGER NOT NULL REFERENCES accounts(account_id),
            opportunity_name VARCHAR NOT NULL,
            stage_id INTEGER NOT NULL REFERENCES stages(stage_id),
            forecast_category_id INTEGER REFERENCES forecast_categories(forecast_category_id),
            amount NUMERIC,
            close_date DATE,
            description VARCHAR
        );
        """,
        # "Down" SQL statement for opportunities
        """--sql
        DROP TABLE opportunities;
        """,
    ]
]

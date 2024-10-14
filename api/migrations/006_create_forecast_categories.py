steps = [
    [
        # "Up" SQL statement for forecast categories
        """--sql
        CREATE TABLE forecast_categories (
            forecast_category_id SERIAL PRIMARY KEY,
            category_name VARCHAR NOT NULL,
            description VARCHAR
        );
        """,
        # "Down" SQL statement for forecast categories
        """--sql
        DROP TABLE forecast_categories;
        """,
    ]
]

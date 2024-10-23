import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.country import Country, CountryCreate
from utils.exceptions import (
    CountryDatabaseError,
    CountryDoesNotExist,
    CountryCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class CountryQueries:
    def get_all_countries(self) -> List[Country]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Country)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM countries;
                        """
                    )
                    countries = cur.fetchall()
                    return countries
        except psycopg.Error as e:
            print(f"Error retrieving all countries: {e}")
            raise CountryDatabaseError("Error retrieving all countries")

    def get_country(self, country_id: int) -> Country:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Country)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM countries
                        WHERE country_id = %s;
                        """,
                        (country_id,),
                    )
                    country = cur.fetchone()
                    if country is None:
                        raise CountryDoesNotExist(
                            f"No country with id {country_id}.",
                        )
                    return country
        except psycopg.Error as e:
            print(f"Error retrieving country with id {country_id}: {e}")
            raise CountryDatabaseError(
                f"Error retrieving country with id {country_id}",
            )

    def create_country(self, country: CountryCreate) -> Country:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Country)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO countries (
                            country_name,
                            country_code
                        )
                        VALUES (
                            %(country_name)s,
                            %(country_code)s
                        )
                        RETURNING *;
                        """,
                        {
                            "country_name": country.country_name,
                            "country_code": country.country_code,
                        },
                    )
                    new_country = cur.fetchone()
                    if new_country is None:
                        raise CountryCreationError("Error creating country")
                    return new_country

        except psycopg.Error as e:
            print(f"Error creating country: {e}")
            raise CountryDatabaseError("Error creating country")

    def delete_country(self, country_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM countries
                        WHERE country_id = %s;
                        """,
                        (country_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting country with id {country_id}: {e}")
            raise CountryDatabaseError(
                f"Error deleting country with id {country_id}",
            )

    def edit_country(
        self,
        country_id: int,
        country_name: Optional[str] = None,
        country_code: Optional[str] = None,
    ) -> Country:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Country)) as cur:
                    update_fields = []
                    update_values = []

                    if country_name:
                        update_fields.append("country_name = %s")
                        update_values.append(country_name)
                    if country_code:
                        update_fields.append("country_code = %s")
                        update_values.append(country_code)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(country_id)
                    sql = f"""--sql
                        UPDATE countries
                        SET {', '.join(update_fields)}
                        WHERE country_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_country = cur.fetchone()
                    if not updated_country:
                        raise CountryDoesNotExist(
                            f"Country with id {country_id} does not exist."
                        )
                    return updated_country

        except psycopg.Error as e:
            print(e)
            raise CountryDatabaseError(
                f"Could not update country {country_id}",
            )
        except ValueError as e:
            print(e)
            raise CountryDatabaseError("No fields provided for update.")

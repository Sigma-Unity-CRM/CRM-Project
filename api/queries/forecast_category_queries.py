import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.forecast_category import ForecastCategory, ForecastCategoryCreate
from utils.exceptions import (
    ForecastCategoryDatabaseError,
    ForecastCategoryDoesNotExist,
    ForecastCategoryCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class ForecastCategoryQueries:
    def get_all_forecast_categories(self) -> List[ForecastCategory]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ForecastCategory)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM forecast_categories;
                        """
                    )
                    forecast_categories = cur.fetchall()
                    return forecast_categories
        except psycopg.Error as e:
            print(f"Error retrieving all forecast categories: {e}")
            raise ForecastCategoryDatabaseError(
                "Error retrieving all forecast categories"
            )

    def get_forecast_category(self, forecast_category_id: int) -> ForecastCategory:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ForecastCategory)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM forecast_categories
                        WHERE forecast_category_id = %s;
                        """,
                        (forecast_category_id,),
                    )
                    forecast_category = cur.fetchone()
                    if forecast_category is None:
                        raise ForecastCategoryDoesNotExist(
                            f"No forecast category {forecast_category_id}."
                        )
                    return forecast_category
        except psycopg.Error as e:
            print(f"Error retrieving category {forecast_category_id}: {e}")
            raise ForecastCategoryDatabaseError(
                f"Error retrieving forecast category {forecast_category_id}"
            )

    def create_forecast_category(
        self, forecast_category: ForecastCategoryCreate
    ) -> ForecastCategory:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ForecastCategory)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO forecast_categories (
                            category_name,
                            description
                        )
                        VALUES (
                            %(category_name)s,
                            %(description)s
                        )
                        RETURNING *;
                        """,
                        forecast_category.dict(),
                    )
                    new_forecast_category = cur.fetchone()
                    if new_forecast_category is None:
                        raise ForecastCategoryCreationError(
                            "Error creating forecast category"
                        )
                    return new_forecast_category

        except psycopg.Error as e:
            print(f"Error creating forecast category: {e}")
            raise ForecastCategoryDatabaseError(
                "Error creating forecast category",
            )

    def delete_forecast_category(self, forecast_category_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM forecast_categories
                        WHERE forecast_category_id = %s;
                        """,
                        (forecast_category_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting category {forecast_category_id}: {e}")
            raise ForecastCategoryDatabaseError(
                f"Error deleting forecast category {forecast_category_id}"
            )

    def edit_forecast_category(
        self,
        forecast_category_id: int,
        category_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ForecastCategory:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ForecastCategory)) as cur:
                    update_fields = []
                    update_values = []

                    if category_name:
                        update_fields.append("category_name = %s")
                        update_values.append(category_name)
                    if description:
                        update_fields.append("description = %s")
                        update_values.append(description)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(forecast_category_id)
                    sql = f"""--sql
                        UPDATE forecast_categories
                        SET {', '.join(update_fields)}
                        WHERE forecast_category_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_forecast_category = cur.fetchone()
                    if not updated_forecast_category:
                        raise ForecastCategoryDoesNotExist(
                            f"Forecast category {forecast_category_id} does not exist."
                        )
                    return updated_forecast_category

        except psycopg.Error as e:
            print(e)
            raise ForecastCategoryDatabaseError(
                f"Could not update forecast category {forecast_category_id}"
            )
        except ValueError as e:
            print(e)
            raise ForecastCategoryDatabaseError(
                "No fields provided for update.",
            )

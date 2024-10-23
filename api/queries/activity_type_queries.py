import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.activity_type import ActivityType, ActivityTypeCreate
from utils.exceptions import (
    ActivityTypeDatabaseError,
    ActivityTypeDoesNotExist,
    ActivityTypeCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class ActivityTypeQueries:
    def get_all_activity_types(self) -> List[ActivityType]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityType)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activity_types;
                        """
                    )
                    activity_types = cur.fetchall()
                    return activity_types
        except psycopg.Error as e:
            print(f"Error retrieving all activity types: {e}")
            raise ActivityTypeDatabaseError(
                "Error retrieving all activity types",
            )

    def get_activity_type(self, activity_type_id: int) -> ActivityType:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityType)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activity_types
                        WHERE activity_type_id = %s;
                        """,
                        (activity_type_id,),
                    )
                    activity_type = cur.fetchone()
                    if activity_type is None:
                        raise ActivityTypeDoesNotExist(
                            f"No activity type with id {activity_type_id}."
                        )
                    return activity_type
        except psycopg.Error as e:
            print(
                f"Error retrieving activity type {activity_type_id}: {e}",
            )
            raise ActivityTypeDatabaseError(
                f"Error retrieving activity type with id {activity_type_id}"
            )

    def create_activity_type(self, activity_type: ActivityTypeCreate) -> ActivityType:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityType)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO activity_types (
                            type_name,
                            description
                        )
                        VALUES (
                            %(type_name)s,
                            %(description)s
                        )
                        RETURNING *;
                        """,
                        activity_type.dict(),
                    )
                    new_activity_type = cur.fetchone()
                    if new_activity_type is None:
                        raise ActivityTypeCreationError(
                            "Error creating activity type",
                        )
                    return new_activity_type

        except psycopg.Error as e:
            print(f"Error creating activity type: {e}")
            raise ActivityTypeDatabaseError("Error creating activity type")

    def delete_activity_type(self, activity_type_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM activity_types
                        WHERE activity_type_id = %s;
                        """,
                        (activity_type_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(
                f"Error deleting activity type {activity_type_id}: {e}",
            )
            raise ActivityTypeDatabaseError(
                f"Error deleting activity type with id {activity_type_id}"
            )

    def edit_activity_type(
        self,
        activity_type_id: int,
        type_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ActivityType:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityType)) as cur:
                    update_fields = []
                    update_values = []

                    if type_name:
                        update_fields.append("type_name = %s")
                        update_values.append(type_name)
                    if description:
                        update_fields.append("description = %s")
                        update_values.append(description)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(activity_type_id)
                    sql = f"""--sql
                        UPDATE activity_types
                        SET {', '.join(update_fields)}
                        WHERE activity_type_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_activity_type = cur.fetchone()
                    if not updated_activity_type:
                        raise ActivityTypeDoesNotExist(
                            f"Activity type {activity_type_id} does not exist."
                        )
                    return updated_activity_type

        except psycopg.Error as e:
            print(e)
            raise ActivityTypeDatabaseError(
                f"Could not update activity type {activity_type_id}"
            )
        except ValueError as e:
            print(e)
            raise ActivityTypeDatabaseError("No fields provided for update.")

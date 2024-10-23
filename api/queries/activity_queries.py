import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.activity import Activity, ActivityCreate
from utils.exceptions import (
    ActivityDatabaseError,
    ActivityDoesNotExist,
    ActivityCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class ActivityQueries:
    def get_all_activities(self) -> List[Activity]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Activity)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activities;
                        """
                    )
                    activities = cur.fetchall()
                    return activities
        except psycopg.Error as e:
            print(f"Error retrieving all activities: {e}")
            raise ActivityDatabaseError("Error retrieving all activities")

    def get_activity(self, activity_id: int) -> Activity:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Activity)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activities
                        WHERE activity_id = %s;
                        """,
                        (activity_id,),
                    )
                    activity = cur.fetchone()
                    if activity is None:
                        raise ActivityDoesNotExist(
                            f"No activity with id {activity_id}."
                        )
                    return activity
        except psycopg.Error as e:
            print(f"Error retrieving activity with id {activity_id}: {e}")
            raise ActivityDatabaseError(
                f"Error retrieving activity with id {activity_id}"
            )

    def create_activity(self, activity: ActivityCreate) -> Activity:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Activity)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO activities (
                            activity_type_id,
                            opportunity_id,
                            description,
                            due_date,
                            completed
                        )
                        VALUES (
                            %(activity_type_id)s,
                            %(opportunity_id)s,
                            %(description)s,
                            %(due_date)s,
                            %(completed)s
                        )
                        RETURNING *;
                        """,
                        activity.dict(),
                    )
                    new_activity = cur.fetchone()
                    if new_activity is None:
                        raise ActivityCreationError("Error creating activity")
                    return new_activity

        except psycopg.Error as e:
            print(f"Error creating activity: {e}")
            raise ActivityDatabaseError("Error creating activity")

    def delete_activity(self, activity_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM activities
                        WHERE activity_id = %s;
                        """,
                        (activity_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting activity with id {activity_id}: {e}")
            raise ActivityDatabaseError(
                f"Error deleting activity with id {activity_id}"
            )

    def edit_activity(
        self,
        activity_id: int,
        activity_type_id: Optional[int] = None,
        opportunity_id: Optional[int] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Activity:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Activity)) as cur:
                    update_fields = []
                    update_values = []

                    if activity_type_id is not None:
                        update_fields.append("activity_type_id = %s")
                        update_values.append(activity_type_id)
                    if opportunity_id is not None:
                        update_fields.append("opportunity_id = %s")
                        update_values.append(opportunity_id)
                    if description is not None:
                        update_fields.append("description = %s")
                        update_values.append(description)
                    if due_date is not None:
                        update_fields.append("due_date = %s")
                        update_values.append(due_date)
                    if completed is not None:
                        update_fields.append("completed = %s")
                        update_values.append(completed)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(activity_id)
                    sql = f"""--sql
                        UPDATE activities
                        SET {', '.join(update_fields)}
                        WHERE activity_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_activity = cur.fetchone()
                    if not updated_activity:
                        raise ActivityDoesNotExist(
                            f"Activity with id {activity_id} does not exist."
                        )
                    return updated_activity

        except psycopg.Error as e:
            print(e)
            raise ActivityDatabaseError(
                f"Could not update activity {activity_id}",
            )
        except ValueError as e:
            print(e)
            raise ActivityDatabaseError("No fields provided for update.")

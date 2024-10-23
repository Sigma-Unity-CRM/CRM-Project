import os
import psycopg
from typing import List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.activity_user import ActivityUser
from utils.exceptions import (
    ActivityUserDatabaseError,
    ActivityUserDoesNotExist,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class ActivityUserQueries:
    def get_all_activity_users(self) -> List[ActivityUser]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityUser)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activity_users;
                        """
                    )
                    activity_users = cur.fetchall()
                    return activity_users
        except psycopg.Error as e:
            print(f"Error retrieving all activity users: {e}")
            raise ActivityUserDatabaseError(
                "Error retrieving all activity users",
            )

    def get_activity_user(self, activity_id: int, user_id: int) -> ActivityUser:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityUser)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activity_users
                        WHERE activity_id = %s AND user_id = %s;
                        """,
                        (activity_id, user_id),
                    )
                    activity_user = cur.fetchone()
                    if activity_user is None:
                        raise ActivityUserDoesNotExist(
                            f"No activity user with activity_id {activity_id} and user_id {user_id}."
                        )
                    return activity_user
        except psycopg.Error as e:
            print(
                f"Error retrieving activity user with activity_id {activity_id} and user_id {user_id}: {e}"
            )
            raise ActivityUserDatabaseError(
                f"Error retrieving activity user with activity_id {activity_id} and user_id {user_id}"
            )

    def create_activity_user(self, activity_id: int, user_id: int) -> ActivityUser:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityUser)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO activity_users (
                            activity_id,
                            user_id
                        )
                        VALUES (
                            %s,
                            %s
                        )
                        RETURNING *;
                        """,
                        (activity_id, user_id),
                    )
                    new_activity_user = cur.fetchone()
                    if new_activity_user is None:
                        raise ActivityUserDatabaseError(
                            "Error creating activity user",
                        )
                    return new_activity_user

        except psycopg.Error as e:
            print(f"Error creating activity user: {e}")
            raise ActivityUserDatabaseError("Error creating activity user")

    def delete_activity_user(self, activity_id: int, user_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM activity_users
                        WHERE activity_id = %s AND user_id = %s;
                        """,
                        (activity_id, user_id),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(
                f"Error deleting activity user with activity_id {activity_id} and user_id {user_id}: {e}"
            )
            raise ActivityUserDatabaseError(
                f"Error deleting activity user with activity_id {activity_id} and user_id {user_id}"
            )

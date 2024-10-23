import os
import psycopg
from typing import List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.activity_contact import ActivityContact
from utils.exceptions import (
    ActivityContactDatabaseError,
    ActivityContactDoesNotExist,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class ActivityContactQueries:
    def get_all_activity_contacts(self) -> List[ActivityContact]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityContact)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activity_contacts;
                        """
                    )
                    activity_contacts = cur.fetchall()
                    return activity_contacts
        except psycopg.Error as e:
            print(f"Error retrieving all activity contacts: {e}")
            raise ActivityContactDatabaseError(
                "Error retrieving all activity contacts",
            )

    def get_activity_contact(
        self, activity_id: int, contact_id: int
    ) -> ActivityContact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityContact)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM activity_contacts
                        WHERE activity_id = %s AND contact_id = %s;
                        """,
                        (activity_id, contact_id),
                    )
                    activity_contact = cur.fetchone()
                    if activity_contact is None:
                        raise ActivityContactDoesNotExist(
                            f"No activity contact with activity_id {activity_id} and contact_id {contact_id}."
                        )
                    return activity_contact
        except psycopg.Error as e:
            print(
                f"Error retrieving activity contact with activity_id {activity_id} and contact_id {contact_id}: {e}"
            )
            raise ActivityContactDatabaseError(
                f"Error retrieving activity contact with activity_id {activity_id} and contact_id {contact_id}"
            )

    def create_activity_contact(
        self, activity_id: int, contact_id: int
    ) -> ActivityContact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(ActivityContact)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO activity_contacts (
                            activity_id,
                            contact_id
                        )
                        VALUES (
                            %s,
                            %s
                        )
                        RETURNING *;
                        """,
                        (activity_id, contact_id),
                    )
                    new_activity_contact = cur.fetchone()
                    if new_activity_contact is None:
                        raise ActivityContactDatabaseError(
                            "Error creating activity contact"
                        )
                    return new_activity_contact

        except psycopg.Error as e:
            print(f"Error creating activity contact: {e}")
            raise ActivityContactDatabaseError(
                "Error creating activity contact",
            )

    def delete_activity_contact(self, activity_id: int, contact_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM activity_contacts
                        WHERE activity_id = %s AND contact_id = %s;
                        """,
                        (activity_id, contact_id),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(
                f"Error deleting activity contact with activity_id {activity_id} and contact_id {contact_id}: {e}"
            )
            raise ActivityContactDatabaseError(
                f"Error deleting activity contact with activity_id {activity_id} and contact_id {contact_id}"
            )

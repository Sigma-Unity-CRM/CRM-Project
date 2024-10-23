import os
import psycopg
from typing import List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.opportunity_contact import OpportunityContact
from utils.exceptions import (
    OpportunityContactDatabaseError,
    OpportunityContactDoesNotExist,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class OpportunityContactQueries:
    def get_all_opportunity_contacts(self) -> List[OpportunityContact]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(OpportunityContact)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM opportunity_contacts;
                        """
                    )
                    opportunity_contacts = cur.fetchall()
                    return opportunity_contacts
        except psycopg.Error as e:
            print(f"Error retrieving all opportunity contacts: {e}")
            raise OpportunityContactDatabaseError(
                "Error retrieving all opportunity contacts"
            )

    def get_opportunity_contact(
        self, opportunity_id: int, contact_id: int
    ) -> OpportunityContact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(OpportunityContact)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM opportunity_contacts
                        WHERE opportunity_id = %s AND contact_id = %s;
                        """,
                        (opportunity_id, contact_id),
                    )
                    opportunity_contact = cur.fetchone()
                    if opportunity_contact is None:
                        raise OpportunityContactDoesNotExist(
                            f"No opportunity contact with opportunity_id {opportunity_id} and contact_id {contact_id}."
                        )
                    return opportunity_contact
        except psycopg.Error as e:
            print(
                f"Error retrieving opportunity contact with opportunity_id {opportunity_id} and contact_id {contact_id}: {e}"
            )
            raise OpportunityContactDatabaseError(
                f"Error retrieving opportunity contact with opportunity_id {opportunity_id} and contact_id {contact_id}"
            )

    def create_opportunity_contact(
        self, opportunity_id: int, contact_id: int
    ) -> OpportunityContact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(OpportunityContact)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO opportunity_contacts (
                            opportunity_id,
                            contact_id
                        )
                        VALUES (
                            %s,
                            %s
                        )
                        RETURNING *;
                        """,
                        (opportunity_id, contact_id),
                    )
                    new_opportunity_contact = cur.fetchone()
                    if new_opportunity_contact is None:
                        raise OpportunityContactDatabaseError(
                            "Error creating opportunity contact"
                        )
                    return new_opportunity_contact

        except psycopg.Error as e:
            print(f"Error creating opportunity contact: {e}")
            raise OpportunityContactDatabaseError(
                "Error creating opportunity contact",
            )

    def delete_opportunity_contact(self, opportunity_id: int, contact_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM opportunity_contacts
                        WHERE opportunity_id = %s AND contact_id = %s;
                        """,
                        (opportunity_id, contact_id),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(
                f"Error deleting opportunity contact with opportunity_id {opportunity_id} and contact_id {contact_id}: {e}"
            )
            raise OpportunityContactDatabaseError(
                f"Error deleting opportunity contact with opportunity_id {opportunity_id} and contact_id {contact_id}"
            )

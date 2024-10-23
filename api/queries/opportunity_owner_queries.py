import os
import psycopg
from typing import List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.opportunity_owner import OpportunityOwner
from utils.exceptions import (
    OpportunityOwnerDatabaseError,
    OpportunityOwnerDoesNotExist,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class OpportunityOwnerQueries:
    def get_all_opportunity_owners(self) -> List[OpportunityOwner]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(OpportunityOwner)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM opportunity_owners;
                        """
                    )
                    opportunity_owners = cur.fetchall()
                    return opportunity_owners
        except psycopg.Error as e:
            print(f"Error retrieving all opportunity owners: {e}")
            raise OpportunityOwnerDatabaseError(
                "Error retrieving all opportunity owners"
            )

    def get_opportunity_owner(
        self, opportunity_id: int, user_id: int
    ) -> OpportunityOwner:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(OpportunityOwner)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM opportunity_owners
                        WHERE opportunity_id = %s AND user_id = %s;
                        """,
                        (opportunity_id, user_id),
                    )
                    opportunity_owner = cur.fetchone()
                    if opportunity_owner is None:
                        raise OpportunityOwnerDoesNotExist(
                            f"No opportunity owner with opportunity_id {opportunity_id} and user_id {user_id}."
                        )
                    return opportunity_owner
        except psycopg.Error as e:
            print(
                f"Error retrieving opportunity owner with opportunity_id {opportunity_id} and user_id {user_id}: {e}"
            )
            raise OpportunityOwnerDatabaseError(
                f"Error retrieving opportunity owner with opportunity_id {opportunity_id} and user_id {user_id}"
            )

    def create_opportunity_owner(
        self, opportunity_id: int, user_id: int
    ) -> OpportunityOwner:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(OpportunityOwner)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO opportunity_owners (
                            opportunity_id,
                            user_id
                        )
                        VALUES (
                            %s,
                            %s
                        )
                        RETURNING *;
                        """,
                        (opportunity_id, user_id),
                    )
                    new_opportunity_owner = cur.fetchone()
                    if new_opportunity_owner is None:
                        raise OpportunityOwnerDatabaseError(
                            "Error creating opportunity owner"
                        )
                    return new_opportunity_owner

        except psycopg.Error as e:
            print(f"Error creating opportunity owner: {e}")
            raise OpportunityOwnerDatabaseError(
                "Error creating opportunity owner",
            )

    def delete_opportunity_owner(self, opportunity_id: int, user_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM opportunity_owners
                        WHERE opportunity_id = %s AND user_id = %s;
                        """,
                        (opportunity_id, user_id),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(
                f"Error deleting opportunity owner with opportunity_id {opportunity_id} and user_id {user_id}: {e}"
            )
            raise OpportunityOwnerDatabaseError(
                f"Error deleting opportunity owner with opportunity_id {opportunity_id} and user_id {user_id}"
            )

import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation
from models.opportunity import Opportunity, OpportunityCreate
from utils.exceptions import (
    OpportunityDatabaseError,
    OpportunityDoesNotExist,
    OpportunityCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class OpportunityQueries:
    def get_all_opportunities(self) -> List[Opportunity]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Opportunity)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM opportunities;
                        """
                    )
                    opportunities = cur.fetchall()
                    return opportunities
        except psycopg.Error as e:
            print(f"Error retrieving all opportunities: {e}")
            raise OpportunityDatabaseError(
                "Error retrieving all opportunities",
            )

    def get_opportunity(self, opportunity_id: int) -> Opportunity:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Opportunity)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM opportunities
                        WHERE opportunity_id = %s;
                        """,
                        (opportunity_id,),
                    )
                    opportunity = cur.fetchone()
                    if opportunity is None:
                        raise OpportunityDoesNotExist(
                            f"No opportunity with id {opportunity_id}."
                        )
                    return opportunity
        except psycopg.Error as e:
            print(f"Error retrieving opportunity with id {opportunity_id}: {e}")
            raise OpportunityDatabaseError(
                f"Error retrieving opportunity with id {opportunity_id}"
            )

    def create_opportunity(self, opportunity: OpportunityCreate) -> Opportunity:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Opportunity)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO opportunities (
                            account_id,
                            opportunity_name,
                            stage_id,
                            forecast_category_id,
                            amount,
                            close_date,
                            description
                        )
                        VALUES (
                            %(account_id)s,
                            %(opportunity_name)s,
                            %(stage_id)s,
                            %(forecast_category_id)s,
                            %(amount)s,
                            %(close_date)s,
                            %(description)s
                        )
                        RETURNING *;
                        """,
                        {
                            "account_id": opportunity.account_id,
                            "opportunity_name": opportunity.opportunity_name,
                            "stage_id": opportunity.stage_id,
                            "forecast_category_id": opportunity.forecast_category_id,
                            "amount": opportunity.amount,
                            "close_date": opportunity.close_date,
                            "description": opportunity.description,
                        },
                    )
                    new_opportunity = cur.fetchone()
                    if new_opportunity is None:
                        raise OpportunityCreationError("Error creating opportunity")
                    return new_opportunity

        except UniqueViolation:
            raise OpportunityCreationError(
                f"Opportunity '{opportunity.opportunity_name}' already exists."
            )
        except psycopg.Error as e:
            print(f"Error creating opportunity: {e}")
            raise OpportunityDatabaseError("Error creating opportunity")

    def delete_opportunity(self, opportunity_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM opportunities
                        WHERE opportunity_id = %s;
                        """,
                        (opportunity_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting opportunity with id {opportunity_id}: {e}")
            raise OpportunityDatabaseError(
                f"Error deleting opportunity with id {opportunity_id}"
            )

    def edit_opportunity(
        self,
        opportunity_id: int,
        opportunity_name: Optional[str] = None,
        stage_id: Optional[int] = None,
        forecast_category_id: Optional[int] = None,
        amount: Optional[float] = None,
        close_date: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Opportunity:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Opportunity)) as cur:
                    update_fields = []
                    update_values = []

                    if opportunity_name:
                        update_fields.append("opportunity_name = %s")
                        update_values.append(opportunity_name)
                    if stage_id:
                        update_fields.append("stage_id = %s")
                        update_values.append(stage_id)
                    if forecast_category_id:
                        update_fields.append("forecast_category_id = %s")
                        update_values.append(forecast_category_id)
                    if amount is not None:
                        update_fields.append("amount = %s")
                        update_values.append(amount)
                    if close_date:
                        update_fields.append("close_date = %s")
                        update_values.append(close_date)
                    if description:
                        update_fields.append("description = %s")
                        update_values.append(description)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(opportunity_id)
                    sql = f"""--sql
                        UPDATE opportunities
                        SET {', '.join(update_fields)}
                        WHERE opportunity_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_opportunity = cur.fetchone()
                    if not updated_opportunity:
                        raise OpportunityDoesNotExist(
                            f"Opportunity with id {opportunity_id} does not exist."
                        )
                    return updated_opportunity

        except psycopg.Error as e:
            print(e)
            raise OpportunityDatabaseError(
                f"Could not update opportunity {opportunity_id}"
            )
        except ValueError as e:
            print(e)
            raise OpportunityDatabaseError("No fields provided for update.")

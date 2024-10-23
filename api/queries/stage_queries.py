import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.stage import Stage, StageCreate
from utils.exceptions import (
    StageDatabaseError,
    StageDoesNotExist,
    StageCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class StageQueries:
    def get_all_stages(self) -> List[Stage]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Stage)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM stages;
                        """
                    )
                    stages = cur.fetchall()
                    return stages
        except psycopg.Error as e:
            print(f"Error retrieving all stages: {e}")
            raise StageDatabaseError("Error retrieving all stages")

    def get_stage(self, stage_id: int) -> Stage:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Stage)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM stages
                        WHERE stage_id = %s;
                        """,
                        (stage_id,),
                    )
                    stage = cur.fetchone()
                    if stage is None:
                        raise StageDoesNotExist(
                            f"No stage with id {stage_id}.",
                        )
                    return stage
        except psycopg.Error as e:
            print(f"Error retrieving stage with id {stage_id}: {e}")
            raise StageDatabaseError(
                f"Error retrieving stage with id {stage_id}",
            )

    def create_stage(self, stage: StageCreate) -> Stage:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Stage)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO stages (
                            stage_name,
                            description
                        )
                        VALUES (
                            %(stage_name)s,
                            %(description)s
                        )
                        RETURNING *;
                        """,
                        stage.dict(),
                    )
                    new_stage = cur.fetchone()
                    if new_stage is None:
                        raise StageCreationError("Error creating stage")
                    return new_stage

        except psycopg.Error as e:
            print(f"Error creating stage: {e}")
            raise StageDatabaseError("Error creating stage")

    def delete_stage(self, stage_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM stages
                        WHERE stage_id = %s;
                        """,
                        (stage_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting stage with id {stage_id}: {e}")
            raise StageDatabaseError(
                f"Error deleting stage with id {stage_id}",
            )

    def edit_stage(
        self,
        stage_id: int,
        stage_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Stage:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Stage)) as cur:
                    update_fields = []
                    update_values = []

                    if stage_name:
                        update_fields.append("stage_name = %s")
                        update_values.append(stage_name)
                    if description:
                        update_fields.append("description = %s")
                        update_values.append(description)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(stage_id)
                    sql = f"""--sql
                        UPDATE stages
                        SET {', '.join(update_fields)}
                        WHERE stage_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_stage = cur.fetchone()
                    if not updated_stage:
                        raise StageDoesNotExist(
                            f"Stage with id {stage_id} does not exist."
                        )
                    return updated_stage

        except psycopg.Error as e:
            print(e)
            raise StageDatabaseError(f"Could not update stage {stage_id}")
        except ValueError as e:
            print(e)
            raise StageDatabaseError("No fields provided for update.")

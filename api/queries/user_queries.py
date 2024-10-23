import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.user import User, UserCreate
from utils.exceptions import (
    UserDatabaseError,
    UserDoesNotExist,
    UserCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class UserQueries:
    def get_all_users(self) -> List[User]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(User)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM users;
                        """
                    )
                    users = cur.fetchall()
                    return users
        except psycopg.Error as e:
            print(f"Error retrieving all users: {e}")
            raise UserDatabaseError("Error retrieving all users")

    def get_user(self, user_id: int) -> User:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(User)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM users
                        WHERE user_id = %s;
                        """,
                        (user_id,),
                    )
                    user = cur.fetchone()
                    if user is None:
                        raise UserDoesNotExist(f"No user with id {user_id}.")
                    return user
        except psycopg.Error as e:
            print(f"Error retrieving user with id {user_id}: {e}")
            raise UserDatabaseError(f"Error retrieving user with id {user_id}")

    def create_user(self, user: UserCreate) -> User:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(User)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO users (
                            username,
                            email,
                            hashed_password,
                            first_name,
                            last_name
                        )
                        VALUES (
                            %(username)s,
                            %(email)s,
                            %(hashed_password)s,
                            %(first_name)s,
                            %(last_name)s
                        )
                        RETURNING *;
                        """,
                        {
                            "username": user.username,
                            "email": user.email,
                            "hashed_password": user.password,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                        },
                    )
                    new_user = cur.fetchone()
                    if new_user is None:
                        raise UserCreationError("Error creating user")
                    return new_user

        except psycopg.Error as e:
            print(f"Error creating user: {e}")
            raise UserDatabaseError("Error creating user")

    def delete_user(self, user_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM users
                        WHERE user_id = %s;
                        """,
                        (user_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting user with id {user_id}: {e}")
            raise UserDatabaseError(f"Error deleting user with id {user_id}")

    def edit_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        hashed_password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> User:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(User)) as cur:
                    update_fields = []
                    update_values = []

                    if username:
                        update_fields.append("username = %s")
                        update_values.append(username)
                    if email:
                        update_fields.append("email = %s")
                        update_values.append(email)
                    if hashed_password:
                        update_fields.append("hashed_password = %s")
                        update_values.append(hashed_password)
                    if first_name:
                        update_fields.append("first_name = %s")
                        update_values.append(first_name)
                    if last_name:
                        update_fields.append("last_name = %s")
                        update_values.append(last_name)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(user_id)
                    sql = f"""--sql
                        UPDATE users
                        SET {', '.join(update_fields)}
                        WHERE user_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_user = cur.fetchone()
                    if not updated_user:
                        raise UserDoesNotExist(
                            f"User with id {user_id} does not exist."
                        )
                    return updated_user

        except psycopg.Error as e:
            print(e)
            raise UserDatabaseError(f"Could not update user {user_id}")
        except ValueError as e:
            print(e)
            raise UserDatabaseError("No fields provided for update.")

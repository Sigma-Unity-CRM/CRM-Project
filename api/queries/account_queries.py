import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.account import Account, AccountCreate
from utils.exceptions import (
    AccountDatabaseError,
    AccountDoesNotExist,
    AccountCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class AccountQueries:
    def get_all_accounts(self) -> List[Account]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Account)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM accounts;
                        """
                    )
                    accounts = cur.fetchall()
                    return accounts
        except psycopg.Error as e:
            print(f"Error retrieving all accounts: {e}")
            raise AccountDatabaseError("Error retrieving all accounts")

    def get_account(self, account_id: int) -> Account:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Account)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM accounts
                        WHERE account_id = %s;
                        """,
                        (account_id,),
                    )
                    account = cur.fetchone()
                    if account is None:
                        raise AccountDoesNotExist(
                            f"No account with id {account_id}.",
                        )
                    return account
        except psycopg.Error as e:
            print(f"Error retrieving account with id {account_id}: {e}")
            raise AccountDatabaseError(
                f"Error retrieving account with id {account_id}",
            )

    def create_account(self, account: AccountCreate) -> Account:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Account)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO accounts (
                            account_name,
                            website,
                            type,
                            description,
                            primary_phone,
                            secondary_phone,
                            billing_street_1,
                            billing_street_2,
                            billing_city,
                            billing_state,
                            billing_zipcode,
                            billing_country_id,
                            shipping_street_1,
                            shipping_street_2,
                            shipping_city,
                            shipping_state,
                            shipping_zipcode,
                            shipping_country_id,
                            account_owner_id
                        )
                        VALUES (
                            %(account_name)s,
                            %(website)s,
                            %(type)s,
                            %(description)s,
                            %(primary_phone)s,
                            %(secondary_phone)s,
                            %(billing_street_1)s,
                            %(billing_street_2)s,
                            %(billing_city)s,
                            %(billing_state)s,
                            %(billing_zipcode)s,
                            %(billing_country_id)s,
                            %(shipping_street_1)s,
                            %(shipping_street_2)s,
                            %(shipping_city)s,
                            %(shipping_state)s,
                            %(shipping_zipcode)s,
                            %(shipping_country_id)s,
                            %(account_owner_id)s
                        )
                        RETURNING *;
                        """,
                        account.dict(),
                    )
                    new_account = cur.fetchone()
                    if new_account is None:
                        raise AccountCreationError("Error creating account")
                    return new_account

        except psycopg.Error as e:
            print(f"Error creating account: {e}")
            raise AccountDatabaseError("Error creating account")

    def delete_account(self, account_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM accounts
                        WHERE account_id = %s;
                        """,
                        (account_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting account with id {account_id}: {e}")
            raise AccountDatabaseError(
                f"Error deleting account with id {account_id}",
            )

    def edit_account(
        self,
        account_id: int,
        account_name: Optional[str] = None,
        website: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        primary_phone: Optional[str] = None,
        secondary_phone: Optional[str] = None,
        billing_street_1: Optional[str] = None,
        billing_street_2: Optional[str] = None,
        billing_city: Optional[str] = None,
        billing_state: Optional[str] = None,
        billing_zipcode: Optional[str] = None,
        billing_country_id: Optional[int] = None,
        shipping_street_1: Optional[str] = None,
        shipping_street_2: Optional[str] = None,
        shipping_city: Optional[str] = None,
        shipping_state: Optional[str] = None,
        shipping_zipcode: Optional[str] = None,
        shipping_country_id: Optional[int] = None,
        account_owner_id: Optional[int] = None,
    ) -> Account:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Account)) as cur:
                    update_fields = []
                    update_values = []

                    if account_name:
                        update_fields.append("account_name = %s")
                        update_values.append(account_name)
                    if website:
                        update_fields.append("website = %s")
                        update_values.append(website)
                    if type:
                        update_fields.append("type = %s")
                        update_values.append(type)
                    if description:
                        update_fields.append("description = %s")
                        update_values.append(description)
                    if primary_phone:
                        update_fields.append("primary_phone = %s")
                        update_values.append(primary_phone)
                    if secondary_phone:
                        update_fields.append("secondary_phone = %s")
                        update_values.append(secondary_phone)
                    if billing_street_1:
                        update_fields.append("billing_street_1 = %s")
                        update_values.append(billing_street_1)
                    if billing_street_2:
                        update_fields.append("billing_street_2 = %s")
                        update_values.append(billing_street_2)
                    if billing_city:
                        update_fields.append("billing_city = %s")
                        update_values.append(billing_city)
                    if billing_state:
                        update_fields.append("billing_state = %s")
                        update_values.append(billing_state)
                    if billing_zipcode:
                        update_fields.append("billing_zipcode = %s")
                        update_values.append(billing_zipcode)
                    if billing_country_id:
                        update_fields.append("billing_country_id = %s")
                        update_values.append(billing_country_id)
                    if shipping_street_1:
                        update_fields.append("shipping_street_1 = %s")
                        update_values.append(shipping_street_1)
                    if shipping_street_2:
                        update_fields.append("shipping_street_2 = %s")
                        update_values.append(shipping_street_2)
                    if shipping_city:
                        update_fields.append("shipping_city = %s")
                        update_values.append(shipping_city)
                    if shipping_state:
                        update_fields.append("shipping_state = %s")
                        update_values.append(shipping_state)
                    if shipping_zipcode:
                        update_fields.append("shipping_zipcode = %s")
                        update_values.append(shipping_zipcode)
                    if shipping_country_id:
                        update_fields.append("shipping_country_id = %s")
                        update_values.append(shipping_country_id)
                    if account_owner_id:
                        update_fields.append("account_owner_id = %s")
                        update_values.append(account_owner_id)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(account_id)
                    sql = f"""--sql
                        UPDATE accounts
                        SET {', '.join(update_fields)}
                        WHERE account_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_account = cur.fetchone()
                    if not updated_account:
                        raise AccountDoesNotExist(
                            f"Account with id {account_id} does not exist."
                        )
                    return updated_account

        except psycopg.Error as e:
            print(e)
            raise AccountDatabaseError(
                f"Could not update account {account_id}",
            )
        except ValueError as e:
            print(e)
            raise AccountDatabaseError("No fields provided for update.")

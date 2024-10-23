import os
import psycopg
from typing import Optional, List
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.contact import Contact, ContactCreate
from utils.exceptions import (
    ContactDatabaseError,
    ContactDoesNotExist,
    ContactCreationError,
    DatabaseURLException,
)

# Initialize Connection Pool
database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your environment.",
    )

pool = ConnectionPool(database_url)


class ContactQueries:
    def get_all_contacts(self) -> List[Contact]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Contact)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM contacts;
                        """
                    )
                    contacts = cur.fetchall()
                    return contacts
        except psycopg.Error as e:
            print(f"Error retrieving all contacts: {e}")
            raise ContactDatabaseError("Error retrieving all contacts")

    def get_contact(self, contact_id: int) -> Contact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Contact)) as cur:
                    cur.execute(
                        """--sql
                        SELECT * FROM contacts
                        WHERE contact_id = %s;
                        """,
                        (contact_id,),
                    )
                    contact = cur.fetchone()
                    if contact is None:
                        raise ContactDoesNotExist(
                            f"No contact with id {contact_id}.",
                        )
                    return contact
        except psycopg.Error as e:
            print(f"Error retrieving contact with id {contact_id}: {e}")
            raise ContactDatabaseError(
                f"Error retrieving contact with id {contact_id}",
            )

    def create_contact(self, contact: ContactCreate) -> Contact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Contact)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO contacts (
                            account_id,
                            first_name,
                            last_name,
                            title,
                            email,
                            primary_phone,
                            secondary_phone,
                            site_name,
                            site_street_1,
                            site_street_2,
                            site_city,
                            site_state,
                            site_zipcode,
                            site_country_id
                        )
                        VALUES (
                            %(account_id)s,
                            %(first_name)s,
                            %(last_name)s,
                            %(title)s,
                            %(email)s,
                            %(primary_phone)s,
                            %(secondary_phone)s,
                            %(site_name)s,
                            %(site_street_1)s,
                            %(site_street_2)s,
                            %(site_city)s,
                            %(site_state)s,
                            %(site_zipcode)s,
                            %(site_country_id)s
                        )
                        RETURNING *;
                        """,
                        contact.dict(),
                    )
                    new_contact = cur.fetchone()
                    if new_contact is None:
                        raise ContactCreationError("Error creating contact")
                    return new_contact

        except psycopg.Error as e:
            print(f"Error creating contact: {e}")
            raise ContactDatabaseError("Error creating contact")

    def delete_contact(self, contact_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM contacts
                        WHERE contact_id = %s;
                        """,
                        (contact_id,),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting contact with id {contact_id}: {e}")
            raise ContactDatabaseError(
                f"Error deleting contact with id {contact_id}",
            )

    def edit_contact(
        self,
        contact_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        title: Optional[str] = None,
        email: Optional[str] = None,
        primary_phone: Optional[str] = None,
        secondary_phone: Optional[str] = None,
        site_name: Optional[str] = None,
        site_street_1: Optional[str] = None,
        site_street_2: Optional[str] = None,
        site_city: Optional[str] = None,
        site_state: Optional[str] = None,
        site_zipcode: Optional[str] = None,
        site_country_id: Optional[int] = None,
    ) -> Contact:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Contact)) as cur:
                    update_fields = []
                    update_values = []

                    if first_name:
                        update_fields.append("first_name = %s")
                        update_values.append(first_name)
                    if last_name:
                        update_fields.append("last_name = %s")
                        update_values.append(last_name)
                    if title:
                        update_fields.append("title = %s")
                        update_values.append(title)
                    if email:
                        update_fields.append("email = %s")
                        update_values.append(email)
                    if primary_phone:
                        update_fields.append("primary_phone = %s")
                        update_values.append(primary_phone)
                    if secondary_phone:
                        update_fields.append("secondary_phone = %s")
                        update_values.append(secondary_phone)
                    if site_name:
                        update_fields.append("site_name = %s")
                        update_values.append(site_name)
                    if site_street_1:
                        update_fields.append("site_street_1 = %s")
                        update_values.append(site_street_1)
                    if site_street_2:
                        update_fields.append("site_street_2 = %s")
                        update_values.append(site_street_2)
                    if site_city:
                        update_fields.append("site_city = %s")
                        update_values.append(site_city)
                    if site_state:
                        update_fields.append("site_state = %s")
                        update_values.append(site_state)
                    if site_zipcode:
                        update_fields.append("site_zipcode = %s")
                        update_values.append(site_zipcode)
                    if site_country_id:
                        update_fields.append("site_country_id = %s")
                        update_values.append(site_country_id)

                    if not update_fields:
                        raise ValueError("No fields provided for update.")

                    update_values.append(contact_id)
                    sql = f"""--sql
                        UPDATE contacts
                        SET {', '.join(update_fields)}
                        WHERE contact_id = %s
                        RETURNING *;
                    """
                    cur.execute(sql, update_values)

                    updated_contact = cur.fetchone()
                    if not updated_contact:
                        raise ContactDoesNotExist(
                            f"Contact with id {contact_id} does not exist."
                        )
                    return updated_contact

        except psycopg.Error as e:
            print(e)
            raise ContactDatabaseError(
                f"Could not update contact {contact_id}",
            )
        except ValueError as e:
            print(e)
            raise ContactDatabaseError("No fields provided for update.")

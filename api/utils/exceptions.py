# Customer exceptions for the application


class OpportunityDatabaseError(Exception):
    pass


class OpportunityDoesNotExist(Exception):
    pass


class OpportunityCreationError(Exception):
    pass


class DatabaseURLException(Exception):
    pass


class CountryDatabaseError(Exception):
    pass


class CountryDoesNotExist(Exception):
    pass


class CountryCreationError(Exception):
    pass


class UserDatabaseError(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class UserCreationError(Exception):
    pass


class ContactDatabaseError(Exception):
    pass


class ContactDoesNotExist(Exception):
    pass


class ContactCreationError(Exception):
    pass


class AccountDatabaseError(Exception):
    pass


class AccountDoesNotExist(Exception):
    pass


class AccountCreationError(Exception):
    pass

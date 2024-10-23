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

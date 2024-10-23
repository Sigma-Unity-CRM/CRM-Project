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


class StageDatabaseError(Exception):
    pass


class StageDoesNotExist(Exception):
    pass


class StageCreationError(Exception):
    pass


class ForecastCategoryDatabaseError(Exception):
    pass


class ForecastCategoryDoesNotExist(Exception):
    pass


class ForecastCategoryCreationError(Exception):
    pass


class ActivityTypeDatabaseError(Exception):
    pass


class ActivityTypeDoesNotExist(Exception):
    pass


class ActivityTypeCreationError(Exception):
    pass


class ActivityDatabaseError(Exception):
    pass


class ActivityDoesNotExist(Exception):
    pass


class ActivityCreationError(Exception):
    pass


class OpportunityContactDatabaseError(Exception):
    pass


class OpportunityContactDoesNotExist(Exception):
    pass


class OpportunityOwnerDatabaseError(Exception):
    pass


class OpportunityOwnerDoesNotExist(Exception):
    pass


class ActivityUserDatabaseError(Exception):
    pass


class ActivityUserDoesNotExist(Exception):
    pass


class ActivityContactDatabaseError(Exception):
    pass


class ActivityContactDoesNotExist(Exception):
    pass

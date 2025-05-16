# account domain exceptions
class AccountAlreadyExists(Exception):
    pass


# users domain exceptions
class UserAlreadyExists(Exception):
    pass


class InvalidLoginDetails(Exception):
    pass


# category exceptions
class CategoryAlreadyExists(Exception):
    pass


# global exceptions
class DatabaseError(Exception):
    pass


# user exception
class UserNotFound(Exception):
    pass

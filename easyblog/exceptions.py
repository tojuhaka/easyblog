class UsernameAlreadyInUseException(Exception):
    def __init__(self, username):
        self.username = username
    def __str__(self):
        return "Username " + self.username + " already in use."

class FieldsNotDefinedException(Exception):
    pass    




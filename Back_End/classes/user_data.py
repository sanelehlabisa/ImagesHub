class User_Data:
    def __init__(self, id: int, email_address: str, type: int) -> None:
        self.id = id
        self.email_address = email_address
        self.type = type

    def toJSON(self):
            return {
                "id": self.id,
                "email_address": self.email_address,
                "type": self.type
            }
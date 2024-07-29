class Request_Data():
    def __init__(self, id: int, guest_id: int, img_id: int, reason: str, status: int) -> None:
        self.id = id
        self.guest_id = guest_id
        self.img_id = img_id
        self.reason = reason
        self.status = status

    def toJSON(self):
            return {
                "id": self.id,
                "guest_id": self.guest_id,
                "img_id": self.img_id,
                "reason": self.reason,
                "status": self.status
            }
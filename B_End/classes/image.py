class Image():
    def __init__(self, id: int, high_res_img_fname: str, low_res_img_fname: str) -> None:
        self.id = id
        self.high_res_img_fname = high_res_img_fname
        self.low_res_img_fname = low_res_img_fname

    def toJSON(self) -> dict:
            return {
                "id": self.id,
                "high_res_img_fname": self.high_res_img_fname,
                "low_res_img_fname": self.low_res_img_fname
            }
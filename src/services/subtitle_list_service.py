from src.data.SubtitleList import SubtitleList
from src.repositories.subtitle_list_repository import SubtitleListRepository


class SubtitleListService:
    def __init__(self):
        self.repo = SubtitleListRepository()

    def list_subtitle_list_by_user_id(self, user_id: int):
        return self.repo.get_subtitle_lists_by_user_id(user_id)

    def add_subtitle_list_by_user_id(self, user_id: int, subtitle_list: SubtitleList):
        return self.repo.add_for_user(user_id, name)

    def delete_product(self, product_id: int, user_id: int):
        self.repo.delete_for_user(product_id, user_id)

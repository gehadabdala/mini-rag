# بيكون معاه ال setting , project_id , و ال db_client عشان اوفر علي نفسي مديهوش لحد من عياله
from helpers.config import get_settings, Settings


class BaseDataModel:

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_settings = get_settings()

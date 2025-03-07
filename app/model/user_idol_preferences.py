from common.db_setting import Base
from sqlalchemy import Column, Integer, JSON


class UserIdolPreferences(Base):
    """ユーザーのアイドルの好み

    Parameters
    ----------
    Base : any
    """

    __tablename__ = "user_idol_preferences"

    user_id = Column(Integer, primary_key=True)
    """ユーザーid
    """
    tantou_idols = Column(JSON)
    """担当アイドル
    """
    favorite_idols = Column(JSON)
    """好きなアイドル
    """

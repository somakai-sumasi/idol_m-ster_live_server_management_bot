from sqlalchemy import JSON, Column, Integer

from app.common.db_setting import Base


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

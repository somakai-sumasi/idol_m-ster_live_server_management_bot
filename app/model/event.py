from sqlalchemy import Column, Integer

from db.setting import Base


class Event(Base):
    """イベント

    Parameters
    ----------
    Base : any
    """

    __tablename__ = "events"

    scheduled_event_id = Column(Integer, primary_key=True)
    """イベントid
    """
    category_id = Column(Integer)
    """カテゴリーid
    """
    message_id = Column(Integer)
    """メッセージid
    """

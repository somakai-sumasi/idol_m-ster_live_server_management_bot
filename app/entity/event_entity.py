from dataclasses import dataclass


@dataclass
class EventEntity:
    """イベント"""

    scheduled_event_id: int
    """イベントid
    """
    category_id: int
    """カテゴリーid
    """
    message_id: int
    """メッセージid
    """

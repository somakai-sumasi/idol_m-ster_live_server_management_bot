from dataclasses import dataclass


@dataclass
class UserIdolPreferencesEntity:
    """ユーザーのアイドルの好み"""

    user_id: int
    """ユーザid
    """
    tantou_idols: list[str]
    """担当アイドル
    """
    favorite_idols: list[str]
    """好きなアイドル
    """

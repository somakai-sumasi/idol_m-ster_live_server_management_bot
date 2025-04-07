from dataclasses import asdict

from db.setting import session
from app.common.model_entity_converter import (
    entity_to_model,
    model_to_entity,
    models_to_entities,
)
from app.entity.user_idol_preference_entity import UserIdolPreferencesEntity
from app.model.user_idol_preferences import UserIdolPreferences


class UserIdolPreferencesRepository:
    @classmethod
    def get_by_user_id(cls, user_id: int) -> UserIdolPreferencesEntity | None:
        """ユーザの好みを検索

        Parameters
        ----------
        user_id : int
            user_id

        Returns
        -------
        UserIdolPreferencesEntity | None
            検索結果
        """
        user_idol_preferences_model: UserIdolPreferences = (
            session.query(UserIdolPreferences).filter_by(user_id=user_id).first()
        )

        if user_idol_preferences_model is None:
            return None

        return model_to_entity(user_idol_preferences_model, UserIdolPreferencesEntity)

    @classmethod
    def get_by_tantou(cls, search_text: str) -> list[UserIdolPreferencesEntity]:
        """担当を検索

        Parameters
        ----------
        user_id : int
            user_id

        Returns
        -------
        UserIdolPreferencesEntity | None
            検索結果
        """
        user_idol_preferences_model: UserIdolPreferences = session.query(
            UserIdolPreferences
        ).filter(UserIdolPreferences.tantou_idols.like(f"%{search_text}%"))

        return models_to_entities(
            user_idol_preferences_model, UserIdolPreferencesEntity
        )

    @classmethod
    def get_by_favorite(cls, search_text: str) -> list[UserIdolPreferencesEntity]:
        """好きなアイドルを検索

        Parameters
        ----------
        user_id : int
            user_id

        Returns
        -------
        UserIdolPreferencesEntity | None
            検索結果
        """
        user_idol_preferences_model: UserIdolPreferences = session.query(
            UserIdolPreferences
        ).filter(UserIdolPreferences.favorite_idols.like(f"%{search_text}%"))

        return models_to_entities(
            user_idol_preferences_model, UserIdolPreferencesEntity
        )

    @classmethod
    def create(
        cls, user_idol_preferences_entity: UserIdolPreferencesEntity
    ) -> UserIdolPreferencesEntity:
        """作成

        Parameters
        ----------
        user_idol_preferences_entity : UserIdolPreferencesEntity
            作成情報

        Returns
        -------
        UserIdolPreferencesEntity
            作成後の情報
        """
        user_idol_preferences = entity_to_model(
            user_idol_preferences_entity, UserIdolPreferences
        )

        session.add(user_idol_preferences)
        session.commit()
        return cls.get_by_user_id(user_idol_preferences_entity.user_id)

    @classmethod
    def update(
        cls, user_idol_preferences_entity: UserIdolPreferencesEntity
    ) -> UserIdolPreferencesEntity:
        """更新

        Parameters
        ----------
        user_idol_preferences_entity : UserIdolPreferencesEntity
            更新情報

        Returns
        -------
        UserIdolPreferencesEntity
            更新後の情報
        """
        session.query(UserIdolPreferences).filter_by(
            user_id=user_idol_preferences_entity.user_id
        ).update(asdict(user_idol_preferences_entity))
        session.commit()

        return cls.get_by_user_id(user_idol_preferences_entity.user_id)

    @classmethod
    def delete(cls, user_id: int) -> None:
        """削除

        Parameters
        ----------
        user_id : int
            user_id
        """
        session.query(UserIdolPreferences).filter_by(user_id=user_id).delete()
        session.commit()

        return

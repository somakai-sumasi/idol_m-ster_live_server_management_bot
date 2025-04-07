import time
from dataclasses import asdict

from app.common.model_entity_converter import entity_to_model, model_to_entity
from app.entity.event_entity import EventEntity
from app.model.event import Event
from db.setting import session


class EventRepository:
    @classmethod
    def get_by_scheduled_event_id(cls, scheduled_event_id: int) -> EventEntity | None:
        """イベントを検索

        Parameters
        ----------
        scheduled_event_id : int
            scheduled_event_id

        Returns
        -------
        EventEntity | None
            検索結果
        """
        voice_setting_model: Event = (
            session.query(Event)
            .filter_by(scheduled_event_id=scheduled_event_id)
            .first()
        )

        if voice_setting_model is None:
            return None

        return model_to_entity(voice_setting_model, EventEntity)

    @classmethod
    def wait_for_get_by_scheduled_event_id(
        cls, scheduled_event_id: int, timeout=1, interval=0.1
    ) -> EventEntity:
        """イベントを検索

        Parameters
        ----------
        scheduled_event_id : int
            scheduled_event_id

        Returns
        -------
        EventEntity | None
            検索結果
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            event = EventRepository.get_by_scheduled_event_id(scheduled_event_id)
            if event:
                return event
            time.sleep(interval)
        raise TimeoutError("指定された時間内にキーが見つかりませんでした。")

    @classmethod
    def create(cls, event_entity: EventEntity) -> EventEntity:
        """作成

        Parameters
        ----------
        event_entity : EventEntity
            作成情報

        Returns
        -------
        EventEntity
            作成後の情報
        """
        voice_setting = entity_to_model(event_entity, Event)

        session.add(voice_setting)
        session.commit()
        return cls.get_by_scheduled_event_id(event_entity.scheduled_event_id)

    @classmethod
    def update(cls, event_entity: EventEntity) -> EventEntity:
        """更新

        Parameters
        ----------
        event_entity : EventEntity
            更新情報

        Returns
        -------
        EventEntity
            更新後の情報
        """
        session.query(Event).filter_by(
            scheduled_event_id=event_entity.scheduled_event_id
        ).update(asdict(event_entity))
        session.commit()

        return cls.get_by_scheduled_event_id(event_entity.scheduled_event_id)

    @classmethod
    def delete(cls, scheduled_event_id: int) -> None:
        """削除

        Parameters
        ----------
        scheduled_event_id : int
            scheduled_event_id
        """
        session.query(Event).filter_by(scheduled_event_id=scheduled_event_id).delete()
        session.commit()

        return

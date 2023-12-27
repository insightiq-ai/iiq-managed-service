import logging

from app.events.base_event import BaseEvent


class EventExecutorRegistry:
    """ Class for registering event executors"""

    registry = {}

    @classmethod
    def register(cls, identifier: str, executor_class):
        """
        :param identifier: To identify the type of class
        :param executor_class: The class which needs to handle the event. It should inherit
        app.events.base_event.BaseEvent class.
        """
        if not issubclass(executor_class, BaseEvent):
            raise Exception("Executor classes should inherit app.events.base_event.BaseEvent class")

        if identifier in cls.registry:
            logging.warning('Executor %s already exists. Will replace it', identifier)
        else:
            logging.warning('Registering event-executor %s', identifier)
        cls.registry[identifier] = executor_class

    @classmethod
    def get_all_events(cls):
        return cls.registry.values()

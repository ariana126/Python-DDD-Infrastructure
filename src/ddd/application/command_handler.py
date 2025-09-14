from abc import ABC
from ddd.framework.service import ServiceClass


class CommandHandler(ServiceClass, ABC):
    pass
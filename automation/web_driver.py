from abc import ABC, abstractmethod


class WebAutomationDriver(ABC):

    @abstractmethod
    def open_url(self, url: str):
        pass

    @abstractmethod
    def click(self, selector: str):
        pass

    @abstractmethod
    def type(self, selector: str, text: str):
        pass

    @abstractmethod
    def upload_file(self, selector: str, file_path: str):
        pass

    @abstractmethod
    def get_text(self, selector: str) -> str:
        pass

    @abstractmethod
    def close(self):
        pass

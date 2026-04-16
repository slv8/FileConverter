from app.domain.services.conversion_service import ConversionService
from app.domain.services.file_service import FileService
from app.repositories.conversion_repository import ConversionRepository
from app.repositories.file_repository import FileRepository


class AppContext:

    def __init__(self):
        self.file_repo = FileRepository()
        self.file_service = FileService(file_repo=self.file_repo)
        self.conversion_repo = ConversionRepository()
        self.conversion_service = ConversionService(conversion_repo=self.conversion_repo, file_repo=self.file_repo)


app_context = AppContext()

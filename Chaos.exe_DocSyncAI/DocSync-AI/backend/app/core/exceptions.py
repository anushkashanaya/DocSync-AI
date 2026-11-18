"""Application errors mapped to HTTP responses by the routes."""


class DocSyncError(Exception):
    """Base error carrying a safe user-facing message."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ProjectNotFoundError(DocSyncError):
    def __init__(self, project_id: str):
        super().__init__(f"Project '{project_id}' was not found.", status_code=404)


class UploadRejectedError(DocSyncError):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class AnalysisError(DocSyncError):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)

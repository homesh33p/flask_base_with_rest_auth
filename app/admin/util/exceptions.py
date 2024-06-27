from werkzeug.exceptions import NotFound

class ApiNotFound(NotFound):
    """Raise status code 404 with customizable WWW-Authenticate header."""

    def __init__(
        self,
        user_id,
        description="Not Found"
    ):
        self.error = f"{user_id} not found"
        self.description = description
        NotFound.__init__(
            self, description=description, response=None, www_authenticate=None
        )

    def get_headers(self, *args,**kwargs):
        return super().get_headers(*args,**kwargs)

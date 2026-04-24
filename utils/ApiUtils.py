class ApiUtils:

    @staticmethod
    def response(status, message, **kwargs):
        resp = {"status": status, "message": message}

        resp.update(**kwargs)

        return resp
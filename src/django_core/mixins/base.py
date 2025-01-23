class BaseViewSetMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code >= 400:
            response.data = {"status": False, "data": response.data}
        else:
            response.data = {
                "status": True,
                "data": response.data,
            }

        return super().finalize_response(request, response, *args, **kwargs)

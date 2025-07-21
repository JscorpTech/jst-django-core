from typing import Any


class BaseViewSetMixin(object):
    action_serializer_class = {}
    action_permission_classes = {}

    def finalize_response(self, request, response, *args, **kwargs):

        if response.status_code == 204:
            return super().finalize_response(request, response, *args,
                                             **kwargs)
        message = self._extract_first_error(response.data)
        if response.status_code >= 400:
            response.data = {
                "status": False,
                "message": message,
                "data": response.data
            }
        else:
            response.data = {
                "status": True,
                "message": message,
                "data": response.data,
            }

        return super().finalize_response(request, response, *args, **kwargs)

    def get_serializer_class(self) -> Any:
        return self.action_serializer_class.get(self.action,
                                                self.serializer_class)

    def get_permissions(self) -> Any:
        return [
            permission() for permission in self.action_permission_classes.get(
                self.action, self.permission_classes)
        ]

    def _extract_first_error(self, data):
        for key, value in data.items():
            if isinstance(value, list) and value:
                return str(value[0])
            elif isinstance(value, str):
                return value
        return "Invalid data"

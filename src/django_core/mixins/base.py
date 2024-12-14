from django.utils.translation import gettext as _


class BaseViewSetMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code >= 400:
            response.data = {
                "status": False,
                "data": {
                    "detail": (
                        response.data.get("detail", _("Xatolik yuz berdi"))
                        if isinstance(response.data, dict)
                        else _("Xatolik yuz berdi")
                    )
                },
            }
        else:
            response.data = {
                "status": True,
                "data": response.data,
            }

        return super().finalize_response(request, response, *args, **kwargs)

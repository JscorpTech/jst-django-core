import json

from django.conf import settings
import os
from django.templatetags import static
from django.utils import safestring

from django import template

register = template.Library()


def getScript(url: object) -> str:
    ext: str = str(url).split(".")[-1]

    if os.getenv("VITE_LIVE", False):
        url = f"http://{os.getenv('VITE_HOST', "0.0.0.0")}:{os.getenv('VITE_PORT', 5000)}/{url}"
    else:
        url = static.static(f"vite/{url}")

    if ext == "css":
        script = f"<link rel='stylesheet' type='text/css' href='{url}'>"
    else:
        script = (
            "<script type='module' type='text/javascript' src='{" "}'></script>"
        ).format(url)
    return script


@register.simple_tag
def vite_load(*args):
    try:
        fd = open(f"{settings.VITE_APP_DIR}/manifest.json")
        manifest = json.load(fd)
    except Exception:
        raise Exception(
            f"Vite manifest file not found or invalid. Maybe your"
            f" {settings.VITE_APP_DIR}/manifest.json file is empty?"
        )
    if not os.getenv("VITE_LIVE", False):
        imports_files = "".join([getScript(file["file"]) for file in manifest.values()])

    else:
        imports_files = "".join([getScript(file) for file in args])
        imports_files += f""" <script type="module" src="http://{os.getenv('VITE_HOST', "0.0.0.0")}:{os.getenv('VITE_PORT', 5000)}/@vite/client">
        </script> <script type="module" src="{static.static("js/vite-refresh.js")}"></script>"""

    return safestring.mark_safe(imports_files)

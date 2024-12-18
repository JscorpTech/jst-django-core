from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"  # Allow client to set page size
    max_page_size = 200  # Maximum page size allowed

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "previous": self.get_previous_link(),
                    "next": self.get_next_link(),
                },
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.page.paginator.per_page,
                "current_page": self.page.number,
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "links": {
                    "type": "object",
                    "properties": {
                        "previous": {
                            "type": ["string", "null"],
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?page=2",
                        },
                        "next": {
                            "type": ["string", "null"],
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?page=4",
                        },
                    },
                    "required": ["previous", "next"],
                },
                "total_items": {
                    "type": "integer",
                    "example": 100,
                },
                "total_pages": {
                    "type": "integer",
                    "example": 10,
                },
                "page_size": {
                    "type": "integer",
                    "example": 10,
                },
                "current_page": {
                    "type": "integer",
                    "example": 1,
                },
                "results": schema,  # Shema natijalar uchun ishlatiladi
            },
            "required": [
                "links",
                "total_items",
                "total_pages",
                "page_size",
                "current_page",
                "results",
            ],
        }

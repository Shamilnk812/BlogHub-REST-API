from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


#----------------------  Custom Pagination -------------------

class CustomPostPagination(PageNumberPagination):
    page_size = 5  # specify default items per page
    page_size_query_param = 'page_size'  
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "message": "Posts fetched successfully.",
            "pagination": {
                "count": self.page.paginator.count,
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "data": data
        })



# ------------------ Custom Response Message --------------

def success_response(message, data=None, status="success"):
    return {
        "status": status,
        "message": message,
        "data": data
    }

def error_response(message, errors=None, status="error"):
    return {
        "status": status,
        "message": message,
        "errors": errors
    }

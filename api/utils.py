from rest_framework.pagination import PageNumberPagination

def paginate_queryset(queryset, request, page_size=5, max_page_size=100):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginator.page_size_query_param = 'page_size'
    paginator.max_page_size = max_page_size
    paginated_data = paginator.paginate_queryset(queryset, request)
    return paginator, paginated_data

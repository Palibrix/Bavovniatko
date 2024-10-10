def debug_disable(request):
    current_url = request.path_info
    entered_admin_page = '/admin/' not in current_url
    entered_docs = '/api/docs' not in current_url

    status = entered_admin_page or entered_docs
    return status

def success_response(data=None, message=None):
    return {
        "success": True,
        "data": data,
        "message": message
    }

def error_response(message):
    return {
        "success": False,
        "error": message
    }

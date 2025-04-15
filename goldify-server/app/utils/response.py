def success_response(message, data=None, code=200):
    return {
        "status": "success",
        "message": message,
        "data": data
    }, code

def error_response(message, code=400, data=None):
    return {
        "status": "error",
        "message": message,
        "data": data
    }, code

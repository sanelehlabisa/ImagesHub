from bottle import static_file, request, response # type: ignore

SERVER_DIRECTORY = "server"

def serve_image(filename):
    if request.method == 'OPTIONS':
        response.code = 500
        return {}
    response.code = 200
    return static_file(filename, root=SERVER_DIRECTORY)

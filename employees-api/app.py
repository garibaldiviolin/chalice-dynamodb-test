from chalice import Chalice, Response

app = Chalice(app_name='employees-api')


@app.route('/employees', methods=["POST"])
def create_employee():
    return Response(
        body={'id': '1'},
        status_code=201
    )


@app.route('/employees', methods=["GET"])
def list_employees():
    return Response(
        body={
            "results": [
                {'id': '1'}
            ]
        },
        status_code=200
    )


@app.route('/employees/{employee_id}', methods=["GET"])
def get_employee(employee_id):
    return Response(body={'id': employee_id}, status_code=200)


@app.route('/employees/{employee_id}', methods=["DELETE"])
def delete_employee(employee_id):
    return Response(
        body=None,
        status_code=204
    )



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

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

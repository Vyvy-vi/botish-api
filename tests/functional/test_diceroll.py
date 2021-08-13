not_valid_int_error = lambda param: {
    "loc": ["query", param],
    "msg": "value is not a valid integer",
    "type": "type_error.integer"
}

ge_error = lambda param, lim: {
    "loc": ["query", param],
    "msg": f"ensure this value is greater than or equal to {lim}",
    "type": "value_error.number.not_ge",
    "ctx": {"limit_value": lim}
}

le_error = lambda param, lim: {
    "loc": ["query", param],
    "msg": f"ensure this value is less than or equal to {lim}",
    "type": "value_error.number.not_le",
    "ctx": {"limit_value": lim}
}


def test_roll_dice(test_client):
    # Check if it works
    response = test_client.get("/diceroll")
    assert response.status_code == 200
    assert response.json()["task"] == "diceroll - d6 x 1"
    assert len(response.json()["result"]) == 1

    for result in response.json()["result"]:
        assert type(result) == int
        assert result > 0 and result < 7


def test_roll_dice_sides_and_num(test_client):
    # Check if it works for custom sides and multiple rounds
    response = test_client.get("/diceroll?sides=3")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d3 x 1"

    for result in response.json()["result"]:
        assert type(result) == int
        assert result > 0 and result < 4

    response = test_client.get("/diceroll?num=3")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d6 x 3"
    assert len(response.json()['result']) == 3

    for result in response.json()["result"]:
        assert type(result) == int
        assert result > 0 and result < 7

    response = test_client.get("/diceroll?num=3&sides=3")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d3 x 3"
    assert len(response.json()['result']) == 3

    for result in response.json()["result"]:
        assert type(result) == int
        assert result > 0 and result < 4


def test_roll_dice_errors(test_client):
    # Check if it errors out
    response = test_client.get("/diceroll/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

    # non-integral values
    response = test_client.get("/diceroll?num=abcd")
    assert response.status_code == 422
    assert not_valid_int_error("num") in response.json()['detail']

    response = test_client.get("/diceroll?sides=abcd")
    assert response.status_code == 422
    assert not_valid_int_error("sides") in response.json()['detail']

    response = test_client.get("/diceroll?sides=abcd&num=abcd")
    assert response.status_code == 422
    assert len(response.json()['detail']) == 2
    assert not_valid_int_error("num") in response.json()['detail']
    assert not_valid_int_error("sides") in response.json()['detail']


    # negative and zero values
    response = test_client.get("/diceroll?sides=-1")
    assert response.status_code == 422
    assert ge_error("sides", 3) in response.json()['detail']

    response = test_client.get("/diceroll?sides=0")
    assert response.status_code == 422
    assert ge_error("sides", 3) in response.json()['detail']

    response = test_client.get("/diceroll?num=-1")
    assert response.status_code == 422
    assert ge_error("num", 1) in response.json()['detail']

    response = test_client.get("/diceroll?num=0")
    assert response.status_code == 422
    assert ge_error("num", 1) in response.json()['detail']

    response = test_client.get("/diceroll?sides=0&num=0")
    assert response.status_code == 422
    assert len(response.json()['detail']) == 2
    assert ge_error("num", 1) in response.json()['detail']
    assert ge_error("sides", 3) in response.json()['detail']

    response = test_client.get("/diceroll?sides=1&num=-1")
    assert response.status_code == 422
    assert len(response.json()['detail']) == 2
    assert ge_error("num", 1) in response.json()['detail']
    assert ge_error("sides", 3) in response.json()['detail']

    # invalid int and zero values
    response = test_client.get("/diceroll?sides=1&num=abcd")
    assert response.status_code == 422
    assert len(response.json()['detail']) == 2
    assert ge_error("sides", 3) in response.json()['detail']
    assert not_valid_int_error("num") in response.json()['detail']

    response = test_client.get("/diceroll?sides=abcd&num=0")
    assert response.status_code == 422
    assert len(response.json()['detail']) == 2
    assert ge_error("num", 1) in response.json()['detail']
    assert not_valid_int_error("sides") in response.json()['detail']


def test_roll_dice_limits(test_client):
    response = test_client.get("/diceroll?sides=2")
    assert response.status_code == 422
    assert ge_error("sides", 3) in response.json()['detail']

    response = test_client.get("/diceroll?sides=10001")
    assert response.status_code == 422
    assert le_error("sides", 10000) in response.json()['detail']

    response = test_client.get("/diceroll?sides=3")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d3 x 1"
    assert len(response.json()['result']) == 1
    for result in response.json()['result']:
        assert type(result) == int
        assert result > 0 and result < 4

    response = test_client.get("/diceroll?sides=10000")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d10000 x 1"
    assert len(response.json()['result']) == 1
    for result in response.json()['result']:
        assert type(result) == int
        assert result > 1 and result < 10000

    response = test_client.get("/diceroll?num=10001")
    assert response.status_code == 422
    assert le_error("num", 10000) in response.json()['detail']

    response = test_client.get("/diceroll?num=1")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d6 x 1"
    assert len(response.json()['result']) == 1
    for result in response.json()['result']:
        assert type(result) == int
        assert result > 0 and result < 7

    response = test_client.get("/diceroll?num=10000")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d6 x 10000"
    assert len(response.json()['result']) == 10000
    for result in response.json()['result']:
        assert type(result) == int
        assert result > 0 and result < 7

    response = test_client.get("/diceroll?num=1&sides=1")
    assert response.status_code == 422
    assert ge_error("sides", 3) in response.json()['detail']

    response = test_client.get("/diceroll?num=1&sides=3")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d3 x 1"
    for result in response.json()['result']:
        assert type(result) == int
        assert result > 0 and result < 4

    response = test_client.get("/diceroll?num=0&sides=9")
    assert response.status_code == 422
    assert ge_error("num", 1) in response.json()['detail']

    response = test_client.get("/diceroll?num=5&sides=9")
    assert response.status_code == 200
    assert response.json()['task'] == "diceroll - d9 x 5"
    assert len(response.json()['result']) == 5
    for result in response.json()['result']:
        assert type(result) == int
        assert result > 0 and result < 10


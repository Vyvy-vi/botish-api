not_valid_int_error = lambda param: {
    "loc": ["query", param],
    "msg": "value is not a valid integer",
    "type": "type_error.integer",
}

ge_error = lambda param, lim: {
    "loc": ["query", param],
    "msg": f"ensure this value is greater than or equal to {lim}",
    "type": "value_error.number.not_ge",
    "ctx": {"limit_value": lim},
}

le_error = lambda param, lim: {
    "loc": ["query", param],
    "msg": f"ensure this value is less than or equal to {lim}",
    "type": "value_error.number.not_le",
    "ctx": {"limit_value": lim},
}


def test_flip_coin(test_client):
    # Check if it works
    response = test_client.get("/coinflip")
    assert response.status_code == 200
    assert response.json()["task"] == "coinflip x 1"
    assert len(response.json()["result"]) == 1

    for result in response.json()["result"]:
        assert type(result) == str
        assert result in ["Heads", "Tails"]


def test_coinflip_num(test_client):
    # Check if it works for custom num
    response = test_client.get("/coinflip?num=10")
    assert response.status_code == 200
    assert response.json()["task"] == "coinflip x 10"
    assert len(response.json()["result"]) == 10

    for result in response.json()["result"]:
        assert type(result) == str
        assert result in ["Heads", "Tails"]

    response = test_client.get("/coinflip?num=1")
    assert response.status_code == 200
    assert response.json()["task"] == "coinflip x 1"
    assert len(response.json()["result"]) == 1

    for result in response.json()["result"]:
        assert type(result) == str
        assert result in ["Heads", "Tails"]


def test_flip_coin_errors(test_client):
    # Check if it errors out
    response = test_client.get("/coinflip/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

    # non-integral values
    response = test_client.get("/coinflip?num=abcd")
    assert response.status_code == 422
    assert not_valid_int_error("num") in response.json()["detail"]

    # negative and zero values
    response = test_client.get("/coinflip?num=-1")
    assert response.status_code == 422
    assert ge_error("num", 1) in response.json()["detail"]

    response = test_client.get("/coinflip?num=0")
    assert response.status_code == 422
    assert ge_error("num", 1) in response.json()["detail"]


def test_flip_coin_limits(test_client):
    response = test_client.get("/coinflip?num=10001")
    assert response.status_code == 422
    assert le_error("num", 10000) in response.json()["detail"]

    response = test_client.get("/coinflip?num=1")
    assert response.status_code == 200
    assert response.json()["task"] == "coinflip x 1"
    assert len(response.json()["result"]) == 1
    for result in response.json()["result"]:
        assert type(result) == str
        assert result in ["Heads", "Tails"]

    response = test_client.get("/coinflip?num=10000")
    assert response.status_code == 200
    assert response.json()["task"] == "coinflip x 10000"
    assert len(response.json()["result"]) == 10000
    for result in response.json()["result"]:
        assert type(result) == str
        assert result in ["Heads", "Tails"]

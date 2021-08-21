from src.routes.quotes import quotes


def test_all_quotes(test_client):
    response = test_client.get("/quotes/all")
    assert response.status_code == 200

    # Check if this returns all quotes
    assert len(response.json()["quotes"]) == len(quotes)

    # Check if the first test quote is valid
    assert response.json()["quotes"][0] == {
        "id": 0,
        "quote": "Quotes are going through",
        "author": "potato"
    }


def test_quotes_by_id(test_client):
    response = test_client.get("/quotes/0")
    assert response.status_code == 200

    # Check if the test quote is valid
    assert response.json() == {
        "id": 0,
        "quote": "Quotes are going through",
        "author": "potato"
    }

    # Check if non-number IDs get flagged
    response = test_client.get("/quotes/abcd")
    assert response.status_code == 422

    not_valid_integer_error = {
        "loc": ["path", "quote_id"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }

    assert not_valid_integer_error in response.json()["detail"]

    # Check if numbers out of bounds get flagged
    # Lower Limit Check
    response = test_client.get("/quotes/-1")

    lower_limit_error = {
        "loc": ["path", "quote_id"],
        "msg": "ensure this value is greater than or equal to 0",
        "type": "value_error.number.not_ge",
        "ctx": {"limit_value": 0},
    }

    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    # Upper Limit Check
    response = test_client.get(f"/quotes/{len(quotes)}")

    upper_limit_error = {
        "loc": ["path", "quote_id"],
        "msg": f"ensure this value is less than {len(quotes)}",
        "type": "value_error.number.not_lt",
        "ctx": {"limit_value": len(quotes)},
    }

    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]


def test_get_quotes(test_client):
    response = test_client.get("/quotes")

    assert response.status_code == 200

    # Check if non numerical values of num get flagged
    not_valid_integer_error = {
        "loc": ["query", "num"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }
    response = test_client.get("/quotes?num=abcd")
    assert response.status_code == 422
    assert not_valid_integer_error in response.json()["detail"]

    # Check if numbers out of bounds get flagged
    # Lower Limit Check
    lower_limit_error = {
        "loc": ["query", "num"],
        "msg": "ensure this value is greater than or equal to 1",
        "type": "value_error.number.not_ge",
        "ctx": {"limit_value": 1},
    }
    response = test_client.get("/quotes?num=-1")
    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    response = test_client.get("/quotes?num=0")
    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    # Upper Limit Check
    upper_limit_error = {
        "loc": ["query", "num"],
        "msg": f"ensure this value is less than {len(quotes)}",
        "type": "value_error.number.not_lt",
        "ctx": {"limit_value": len(quotes)},
    }
    response = test_client.get(f"/quotes?num={len(quotes) + 1}")
    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]

    response = test_client.get(f"/quotes?num={len(quotes)}")
    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]

    # Check if it works
    response = test_client.get(f"/quotes?num={len(quotes) - 1}")
    assert response.status_code == 200
    assert len(response.json()["quotes"]) == len(quotes) - 1

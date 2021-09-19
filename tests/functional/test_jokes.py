import random

from src.routes.jokes import jokes


def test_all_jokes(test_client):
    response = test_client.get("/jokes/all")
    assert response.status_code == 200

    # Check if this returns all jokes
    assert len(response.json()["jokes"]) == len(jokes)

    # Check if the first test joke is valid
    assert response.json()["jokes"][0] == {
        "id": 0,
        "joke": jokes[0],
    }

    # Check if a random quote is valid
    random_index = random.randint(0, len(jokes) - 1)
    assert response.json()["jokes"][random_index] == {
        "id": random_index,
        "joke": jokes[random_index],
    }


def test_jokes_by_id(test_client):
    response = test_client.get("/jokes/0")
    assert response.status_code == 200

    # Check if the test joke is valid
    assert response.json() == {"id": 0, "joke": jokes[0]}

    # Check if non-number IDs get flagged
    response = test_client.get("/jokes/abcd")
    assert response.status_code == 422

    not_valid_integer_error = {
        "loc": ["path", "joke_id"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }

    assert not_valid_integer_error in response.json()["detail"]

    # Check if numbers out of bounds get flagged
    # Lower Limit Check
    response = test_client.get("/jokes/-1")

    lower_limit_error = {
        "loc": ["path", "joke_id"],
        "msg": "ensure this value is greater than or equal to 0",
        "type": "value_error.number.not_ge",
        "ctx": {"limit_value": 0},
    }

    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    # Upper Limit Check
    response = test_client.get(f"/jokes/{len(jokes)}")

    upper_limit_error = {
        "loc": ["path", "joke_id"],
        "msg": f"ensure this value is less than {len(jokes)}",
        "type": "value_error.number.not_lt",
        "ctx": {"limit_value": len(jokes)},
    }

    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]


def test_get_jokes(test_client):
    response = test_client.get("/jokes")

    assert response.status_code == 200

    # Check if non numerical values of num get flagged
    not_valid_integer_error = {
        "loc": ["query", "num"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }
    response = test_client.get("/jokes?num=abcd")
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
    response = test_client.get("/jokes?num=-1")
    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    response = test_client.get("/jokes?num=0")
    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    # Upper Limit Check
    upper_limit_error = {
        "loc": ["query", "num"],
        "msg": f"ensure this value is less than {len(jokes)}",
        "type": "value_error.number.not_lt",
        "ctx": {"limit_value": len(jokes)},
    }
    response = test_client.get(f"/jokes?num={len(jokes) + 1}")
    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]

    response = test_client.get(f"/jokes?num={len(jokes)}")
    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]

    # Check if it works
    response = test_client.get(f"/jokes?num={len(jokes) - 1}")
    assert response.status_code == 200
    assert len(response.json()["jokes"]) == len(jokes) - 1

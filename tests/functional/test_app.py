from fastapi.testclient import TestClient

from src.main import app
from src.routes.jokes import jokes

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>The Heptagram API</h1>"


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200


def test_all_jokes():
    response = client.get("/jokes/all")
    assert response.status_code == 200

    # Check if this returns all jokes
    assert len(response.json()["jokes"]) == len(jokes)

    # Check if the first test joke is valid
    assert response.json()["jokes"][0] == {
        "id": 0,
        "joke": "Jokes are going through",
    }


def test_jokes_by_id():
    response = client.get("/jokes/0")
    assert response.status_code == 200

    # Check if the test joke is valid
    assert response.json() == {"id": 0, "joke": "Jokes are going through"}

    # Check if non-number IDs get flagged
    response = client.get("/jokes/abcd")
    assert response.status_code == 422

    not_valid_integer_error = {
        "loc": ["path", "joke_id"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }

    assert not_valid_integer_error in response.json()["detail"]

    # Check if numbers out of bounds get flagged
    # Lower Limit Check
    response = client.get("/jokes/-1")

    lower_limit_error = {
        "loc": ["path", "joke_id"],
        "msg": "ensure this value is greater than or equal to 0",
        "type": "value_error.number.not_ge",
        "ctx": {"limit_value": 0},
    }

    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    # Upper Limit Check
    response = client.get(f"/jokes/{len(jokes)}")

    upper_limit_error = {
        "loc": ["path", "joke_id"],
        "msg": f"ensure this value is less than {len(jokes)}",
        "type": "value_error.number.not_lt",
        "ctx": {"limit_value": len(jokes)},
    }

    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]


def test_get_jokes():
    response = client.get("/jokes")

    assert response.status_code == 200

    # Check if non numerical values of num get flagged
    not_valid_integer_error = {
        "loc": ["query", "num"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }
    response = client.get("/jokes?num=abcd")
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
    response = client.get("/jokes?num=-1")
    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    response = client.get("/jokes?num=0")
    assert response.status_code == 422
    assert lower_limit_error in response.json()["detail"]

    # Upper Limit Check
    upper_limit_error = {
        "loc": ["query", "num"],
        "msg": "ensure this value is less than 3",
        "type": "value_error.number.not_lt",
        "ctx": {"limit_value": 3},
    }
    response = client.get(f"/jokes?num={len(jokes) + 1}")
    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]

    response = client.get(f"/jokes?num={len(jokes)}")
    assert response.status_code == 422
    assert upper_limit_error in response.json()["detail"]

    # Check if it works
    response = client.get(f"/jokes?num={len(jokes) - 1}")
    assert response.status_code == 200
    assert len(response.json()["jokes"]) == len(jokes) - 1


def test_roll_dice():
    # Check if it works
    response = client.get("/diceroll")
    assert response.status_code == 200
    assert response.json()["task"] == "diceroll - d6 x 1"
    assert len(response.json()["result"]) == 1

    for result in response.json()["result"]:
        assert type(result) == int
        assert result > 0 and result < 7

    # Check if it works for custom sides and multiple rounds

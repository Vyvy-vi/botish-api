# Check index page exists
def test_index(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>The Heptagram API</h1>"


# Check if docs got served
def test_docs(test_client):
    response = test_client.get("/docs")
    assert response.status_code == 200

    response = test_client.get("/redoc")
    assert response.status_code == 200

def test_get_polluters(client):
    response = client.get("/polluter")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)   
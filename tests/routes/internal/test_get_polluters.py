def test_get_polluters(client):
    response = client.get("/polluter")
    
    assert response.status_code == 200
    resp = response.json()
    assert isinstance(resp['data'], dict)   
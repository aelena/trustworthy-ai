from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_readyz_loads_bok():
    r = client.get("/readyz")
    assert r.status_code == 200
    body = r.json()
    assert body["bok_files"] > 0
    assert body["bok_tokens_estimate"] > 1000

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_process_excel_data():
    response = client.post("/excel_process", json={
        "file_path": "randompath/file.xlsx",
        "campaign_name": "test_campaign",
        "call_date": "2024-05-01"
    })
    assert response.status_code == 200
    assert response.json() == {"detail": "Данные успешно вставлены в таблицу TABLE_NAME"}

def test_process_crm_data():
    response = client.post("/crm_process")
    assert response.status_code == 200
    assert response.json() == {"detail": "Данные успешно обработаны"}

def test_export_temp_data():
    response = client.post("/export_temp_data", json={
        "campaign_name": "test_campaign"
    })
    assert response.status_code == 200
    assert response.json()["status"] == True
    assert "result_file_path" in response.json()
    assert "input_file_path" in response.json()

def test_export_data_by_date():
    response = client.post("/export_data_by_date", json={
        "campaign_name": "test_campaign",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    })
    assert response.status_code == 200
    assert response.json()["status"] == True
    assert "result_file_path" in response.json()
    assert "input_file_path" in response.json()

def test_process_collection():
    response = client.post("/collection_process", json={
        "file_path": "randompath/excel/file.xlsx",
        "campaign_name": "test_campaign"
    })
    assert response.status_code == 200
    assert response.json() == {"detail": "Данные успешно загружены в таблицу COLLECTION"}

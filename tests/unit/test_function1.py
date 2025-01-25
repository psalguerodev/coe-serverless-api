import pytest
import json
import os
from functions.function1.app import lambda_handler  # Importación directa

@pytest.fixture()
def api_event():
    return {
        'httpMethod': 'GET',
        'body': ''
    }

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('SECRET_NAME', 'test-secret')
    monkeypatch.setenv('AWS_SAM_LOCAL', 'true')
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'testing')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'testing')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-east-1')

def test_lambda_handler_success(api_event, mocker, mock_env):
    # Mock para secrets manager
    mock_client = mocker.patch('boto3.client')
    mock_client.return_value.get_secret_value.return_value = {
        'SecretString': json.dumps({'username': 'test_user', 'password': 'test_pass'})
    }
    
    response = lambda_handler(api_event, None)
    
    # Verificar la respuesta
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['secret_processed'] is True
    assert 'secret_value' in body

def test_lambda_handler_error(api_event, mocker, mock_env):
    # Mock para simular un error
    mock_client = mocker.patch('boto3.client')
    mock_client.return_value.get_secret_value.side_effect = Exception('Test error')
    
    response = lambda_handler(api_event, None)
    
    # Verificar la respuesta de error
    assert response['statusCode'] == 500
    assert 'error' in json.loads(response['body']) 
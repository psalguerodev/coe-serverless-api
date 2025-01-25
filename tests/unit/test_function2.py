import pytest
import json
import os
from functions.function2.app import lambda_handler

@pytest.fixture()
def api_event():
    return {
        'httpMethod': 'POST',
        'body': json.dumps({
            'mensaje': 'Hola Mundo'
        })
    }

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('CUSTOM_VAR', 'test-value')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

def test_lambda_handler_success(api_event, mock_env):
    # Ejecutar la función
    response = lambda_handler(api_event, None)
    
    # Verificar la respuesta
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Mensaje procesado: Hola Mundo'
    assert body['environment']['variable'] == 'test-value'

def test_lambda_handler_without_message(mock_env):
    # Evento sin mensaje
    event = {
        'httpMethod': 'POST',
        'body': json.dumps({})
    }
    
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Mensaje procesado: No se proporcionó mensaje'

def test_lambda_handler_invalid_json(mock_env):
    # Evento con JSON inválido
    event = {
        'httpMethod': 'POST',
        'body': 'invalid json'
    }
    
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 500
    body = json.loads(response['body'])
    assert 'error' in body

def test_lambda_handler_without_body(mock_env):
    # Evento sin body
    event = {
        'httpMethod': 'POST'
    }
    
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Mensaje procesado: No se proporcionó mensaje' 
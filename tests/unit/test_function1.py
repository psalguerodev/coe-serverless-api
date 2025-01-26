import pytest
import json
import os
from functions.function1.app import lambda_handler

@pytest.fixture()
def api_event():
    return {
        'httpMethod': 'GET',
        'body': ''
    }

@pytest.fixture
def mock_secrets_response():
    return {
        'SecretString': json.dumps({
            'username': 'test_user',
            'password': 'test_pass'
        })
    }

def test_lambda_handler_success(api_event, mock_secrets_response, mocker, monkeypatch):
    # Configurar variables de ambiente
    monkeypatch.setenv('SECRET_NAME', 'test-secret')
    
    # Mock del cliente AWS
    mock_secrets = mocker.MagicMock()
    mock_secrets.get_secret_value.return_value = mock_secrets_response
    
    # Mock de la función get_aws_client
    mock_get_client = mocker.patch('functions.function1.app.get_aws_client')
    mock_get_client.return_value = mock_secrets
    
    # Ejecutar función
    response = lambda_handler(api_event, None)
    
    # Verificar que se llamó al mock correctamente
    mock_get_client.assert_called_once_with('secretsmanager')
    mock_secrets.get_secret_value.assert_called_once_with(SecretId='test-secret')
    
    # Verificar respuesta
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['secret_processed'] is True
    assert 'secret_value' in body
    assert body['environment'] == 'true'

def test_lambda_handler_error(api_event, mocker, monkeypatch):
    # Configurar variables de ambiente
    monkeypatch.setenv('SECRET_NAME', 'test-secret')
    
    # Mock que simula un error
    mock_get_client = mocker.patch('functions.function1.app.get_aws_client')
    mock_get_client.side_effect = Exception('Test error')
    
    # Ejecutar función
    response = lambda_handler(api_event, None)
    
    # Verificar respuesta de error
    assert response['statusCode'] == 500
    body = json.loads(response['body'])
    assert 'error' in body

def test_get_aws_client_local(mocker):
    from utils.aws_clients import get_aws_client
    
    # Mock de boto3.client
    mock_boto3_client = mocker.patch('boto3.client')
    
    # Llamar a la función
    get_aws_client('secretsmanager')
    
    # Verificar que se llamó con los parámetros correctos
    mock_boto3_client.assert_called_once()
    call_args = mock_boto3_client.call_args[1]
    assert call_args['endpoint_url'] == 'http://host.docker.internal:4566'
    assert call_args['aws_access_key_id'] == 'dummy' 
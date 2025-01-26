import json
import os
import boto3
from botocore.config import Config

# Importar desde el layer
try:
    from utils.logger import setup_logger  # Para producción (layer)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../layers/common/python'))
    from utils.logger import setup_logger  # Para desarrollo local

logger = setup_logger(__name__)

def get_secret():
    secret_name = os.environ['SECRET_NAME']
    
    try:
        # Configuración para ambiente local
        if os.environ.get('AWS_SAM_LOCAL'):
            # Usamos host.docker.internal para acceder al host desde dentro del contenedor
            endpoint_url = 'http://host.docker.internal:4566'
            secrets_client = boto3.client(
                'secretsmanager',
                endpoint_url=endpoint_url,
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy',
                region_name='us-east-1',
                config=Config(
                    connect_timeout=5,
                    read_timeout=5,
                    retries={'max_attempts': 2}
                )
            )
        else:
            secrets_client = boto3.client('secretsmanager')
            
        logger.info(f"Intentando obtener secreto desde: {endpoint_url if os.environ.get('AWS_SAM_LOCAL') else 'AWS'}")
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        logger.error(f"Error obteniendo el secreto: {str(e)}")
        raise

def lambda_handler(event, context):
    logger.info("Procesando evento en función 1")
    try:
        secret_value = get_secret()
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Función 1 ejecutada exitosamente',
                'secret_processed': True,
                'environment': os.environ.get('AWS_SAM_LOCAL', 'aws'),
                'secret_value': secret_value  # Solo para depuración local
            })
        }
    except Exception as e:
        logger.error(f"Error en lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno del servidor'
            })
        } 
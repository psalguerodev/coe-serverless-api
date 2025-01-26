import json
import os
from utils.logger import setup_logger
from utils.aws_clients import get_aws_client

logger = setup_logger(__name__)

def get_secret():
    secret_name = os.environ['SECRET_NAME']
    
    try:
        # Obtener cliente de Secrets Manager configurado automáticamente
        secrets_client = get_aws_client('secretsmanager')
        
        logger.info(f"Intentando obtener secreto: {secret_name}")
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
                'secret_value': secret_value,  # Solo para depuración local
                'new_secret_value': 'new_secret_value'  # Solo para depuración local
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
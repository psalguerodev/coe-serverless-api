import json
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)

def lambda_handler(event, context):
    logger.info("Procesando evento en función 2")
    try:
        # Obtener y validar el body
        body_str = event.get('body', '{}')
        try:
            body = json.loads(body_str)
        except json.JSONDecodeError as e:
            logger.error(f"Error decodificando JSON: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'JSON inválido en el body'
                })
            }
        
        # Obtener mensaje del body
        mensaje = body.get('mensaje', 'No se proporcionó mensaje')
        logger.info(f"Mensaje recibido: {mensaje}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Mensaje procesado: {mensaje}',
                'environment': {
                    'variable': os.environ.get('CUSTOM_VAR', 'no definida')
                }
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
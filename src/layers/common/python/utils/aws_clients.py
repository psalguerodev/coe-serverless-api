import os
import boto3
from botocore.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_aws_client(service_name, local_config=None):
    """
    Obtiene un cliente AWS configurado según el ambiente (local o producción)
    
    Args:
        service_name (str): Nombre del servicio AWS (e.g., 'secretsmanager')
        local_config (dict, optional): Configuración específica para ambiente local
            
    Returns:
        boto3.client: Cliente AWS configurado
    """
    try:
        if os.environ.get('AWS_SAM_LOCAL'):
            # Configuración por defecto para local
            default_config = {
                'endpoint_url': 'http://host.docker.internal:4566',
                'aws_access_key_id': 'dummy',
                'aws_secret_access_key': 'dummy',
                'region_name': 'us-east-1',
                'config': Config(
                    connect_timeout=5,
                    read_timeout=5,
                    retries={'max_attempts': 2}
                )
            }
            
            # Actualizar con configuración específica si se proporciona
            if local_config:
                default_config.update(local_config)
                
            logger.info(f"Creando cliente local para {service_name} en: {default_config['endpoint_url']}")
            return boto3.client(service_name, **default_config)
        else:
            logger.info(f"Creando cliente AWS para {service_name}")
            return boto3.client(service_name)
            
    except Exception as e:
        logger.error(f"Error creando cliente AWS para {service_name}: {str(e)}")
        raise 
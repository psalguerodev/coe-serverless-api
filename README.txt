PROYECTO SERVERLESS CON AWS SAM

Este proyecto contiene una aplicación serverless utilizando AWS SAM con dos funciones Lambda en Python, que incluyen manejo de secretos, variables de ambiente y capas compartidas.

REQUISITOS PREVIOS
- Python 3.12 o superior
- AWS CLI configurado
- AWS SAM CLI instalado
- Docker (para pruebas locales)

PASO A PASO PARA CONFIGURACIÓN

1. CREAR Y CONFIGURAR ENTORNO VIRTUAL
   a. Crear entorno virtual:
      python -m venv .venv

   b. Activar entorno virtual:
      - En Windows: .venv\Scripts\activate
      - En Linux/Mac: source .venv/bin/activate

   c. Instalar dependencias:
      pip install -r requirements-dev.txt

2. CONFIGURAR LOCALSTACK
   a. Iniciar LocalStack:
      docker-compose up -d

   b. Dar permisos al script de inicialización:
      chmod +x init-localstack.sh

   c. Ejecutar script de inicialización:
      ./init-localstack.sh

   d. Verificar que LocalStack está funcionando:
      curl http://localhost:4566/_localstack/health

   e. Verificar que el secreto se creó:
      aws --endpoint-url=http://localhost:4566 secretsmanager list-secrets --region us-east-1

3. PRUEBAS LOCALES
   a. Ejecutar pruebas unitarias:
      pytest tests/unit/

   b. Invocar funciones individualmente:
      - Función 1: sam local invoke Function1 -e tests/events/event1.json --env-vars env.json
      - Función 2: sam local invoke Function2 -e tests/events/event2.json --env-vars env.json

   c. Iniciar API local:
      sam local start-api --env-vars env.json

4. DESPLIEGUE
   a. Construir el proyecto:
      sam build

   b. Primer despliegue (configuración guiada):
      sam deploy --guided

   c. Despliegues subsecuentes:
      sam deploy

ESTRUCTURA DEL PROYECTO
mi-proyecto-serverless/
│
├── src/
│   ├── functions/          # Funciones Lambda
│   │   ├── function1/      # Función que usa Secrets Manager
│   │   └── function2/      # Función que procesa mensajes
│   └── layers/             # Capas compartidas
│       └── common/         # Utilidades comunes (logger)
├── tests/
│   ├── unit/              # Pruebas unitarias
│   └── events/            # Eventos de prueba
├── template.yaml          # Plantilla SAM
└── env.json              # Variables de ambiente locales

ENDPOINTS DISPONIBLES
1. GET /function1
   - Accede a un secreto y retorna una respuesta
   - Prueba local: curl http://localhost:3000/function1

2. POST /function2
   - Procesa un mensaje y retorna una respuesta
   - Prueba local: 
     curl -X POST http://localhost:3000/function2 \
     -H "Content-Type: application/json" \
     -d '{"mensaje": "Hola Mundo"}'

VARIABLES DE AMBIENTE
- Desarrollo Local: Configuradas en env.json
- Producción: Configuradas en template.yaml

SOLUCIÓN DE PROBLEMAS COMUNES

1. Error de conexión con LocalStack:
   - Verificar que LocalStack está corriendo: docker ps
   - Verificar la salud: curl http://localhost:4566/_localstack/health
   - Reiniciar LocalStack: docker-compose restart

2. Errores en las pruebas:
   - Verificar entorno virtual está activado
   - Reinstalar dependencias: pip install -r requirements-dev.txt
   - Limpiar caché de pytest: pytest --cache-clear

3. Errores de timeout:
   - Verificar el valor de Timeout en template.yaml
   - Verificar conexión con LocalStack
   - Revisar logs: sam logs -n Function1

LIMPIEZA
1. Detener LocalStack:
   docker-compose down

2. Eliminar recursos AWS:
   sam delete

3. Desactivar entorno virtual:
   deactivate

NOTAS IMPORTANTES
- Mantener actualizadas las dependencias
- Revisar los logs para diagnóstico
- Asegurar que Docker esté corriendo antes de las pruebas locales
- Verificar la configuración de AWS CLI antes del despliegue 

PRUEBAS DE FUNCIÓN 2

1. Invocar función con mensaje:
   sam local invoke Function2 -e tests/events/event2.json --env-vars env.json
   # Respuesta esperada: {"statusCode": 200, "body": {"message": "Mensaje procesado: Este es un mensaje de prueba"}}

2. Invocar función con mensaje vacío:
   sam local invoke Function2 -e tests/events/event2_empty.json --env-vars env.json
   # Respuesta esperada: {"statusCode": 200, "body": {"message": "Mensaje procesado: No se proporcionó mensaje"}}

3. Invocar función con JSON inválido:
   sam local invoke Function2 -e tests/events/event2_invalid.json --env-vars env.json
   # Respuesta esperada: {"statusCode": 500, "body": {"error": "JSON inválido en el body"}}

4. Probar vía API local:
   a. Iniciar API:
      sam local start-api --env-vars env.json
   
   b. Enviar solicitud:
      curl -X POST http://localhost:3000/function2 \
        -H "Content-Type: application/json" \
        -d '{"mensaje": "Este es un mensaje de prueba"}' 
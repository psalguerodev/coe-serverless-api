#!/bin/bash

# Esperar a que LocalStack esté listo
echo "Esperando que LocalStack esté listo..."
while ! curl -s http://localhost:4566/_localstack/health | grep -q '"secretsmanager": "available"'; do
    sleep 2
done

# Crear el secreto
echo "Creando secreto en LocalStack..."
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret \
    --name "dev/mi-secreto" \
    --description "Secreto de prueba" \
    --secret-string '{"username": "test_user", "password": "test_password"}' \
    --region us-east-1

echo "Configuración completada!" 
#!/bin/bash

# Variables
STACK_NAME="rag-movies-system-stack"
TEMPLATE_FILE="infra/template.yaml"
PROFILE="cf-deployment-user"
DB_USERNAME="xx"
DB_PASSWORD="xx"
ALLOWED_IP="xx"

# Validación del perfil configurado
aws sts get-caller-identity --profile $PROFILE > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "El perfil $PROFILE no está configurado correctamente o no tiene acceso."
  exit 1
fi

# Despliegue del stack de CloudFormation
echo "Iniciando el despliegue del stack: $STACK_NAME..."
aws cloudformation deploy \
  --template-file $TEMPLATE_FILE \
  --stack-name $STACK_NAME \
  --parameter-overrides DBUsername=$DB_USERNAME DBPassword=$DB_PASSWORD AllowedIP=$ALLOWED_IP \
  --capabilities CAPABILITY_NAMED_IAM \
  --profile $PROFILE

if [ $? -eq 0 ]; then
  echo "El despliegue del stack $STACK_NAME se completó con éxito."
else
  echo "El despliegue falló. Revisa los logs para más detalles."
  exit 1
fi

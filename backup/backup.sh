#!/bin/bash
mkdir -p /backups

echo "Iniciando servicio de backup automático..."

while true; do
   
    FILENAME=/backups/backup_$(date +%Y%m%d_%H%M%S).sql
    
    echo "Generando respaldo: $FILENAME"
    
  
    export PGPASSWORD=$DB_PASSWORD
    pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $FILENAME
    
    if [ $? -eq 0 ]; then
        echo "✅ Respaldo exitoso."
    else
        echo "❌ Error al generar respaldo."
    fi
    
    
    echo "Esperando 86400 segundos..."
    sleep 86400
done
## Configuración de la Base de Datos

Este proyecto utiliza **MariaDB**. Para configurarlo se crea un archivo llamado `.env` en la raíz del proyecto con las siguientes variables:

```env
DB_USERNAME="user"
DB_PASSWORD="password"
DB_SERVER="server"
DB_PORT=port
DB_NAME="database"
```

## Datos de prueba

El archivo **dump-fastapi_test_01.sql** contiene datos de prueba para importar en la base de datos.

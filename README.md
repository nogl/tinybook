# TinyBook

Repositorio con una aplicación Flask de ejemplo.

Crear entorno virtual  
```python -m venv venv```  

Activar el entorno virtual  
```source venv/bin/activate```

### App Initialization
Instalar las dependencias  
```pip install -r requirements.txt```

Uso de la cli de Flask (al llamarse la carpeta `app` y la aplicación se initializa con `create_app()` en el `app.__init__`, los módulos se cargan automáticamente.)

Mapeo app.endpoint | method | rule
```
$ [xxxx]@[/c/repos/tinybook]$>  flask routes
Endpoint           Methods  Rule                              
-----------------  -------  ----------------------------------
auth.login         GET      /auth/login                       
auth.register      GET      /auth/register                    
auth_api.login     POST     /api/v1/auth/login                
auth_api.me        GET      /api/v1/auth/me                   
auth_api.register  POST     /api/v1/auth/register             
get_cfg            GET      /cfg                              
index              GET      /index                            
index              GET      /                                 
openapi            GET      /openapi
static             GET      /static/<path:filename>
swagger_ui.show    GET      /openapi/docs/<path:path>
swagger_ui.show    GET      /openapi/docs/
swagger_ui.static  GET      /openapi/docs/dist/<path:filename>
```

```
flask cli # comandos basicos con la BBDD
flask database-schema # comandos relacionados con los schemas de la BBDD.
```
__
```
flask cli init_db # Inicializa la base de datos
```
Por defecto crea ``app/app.db``, un fichero SQLite util para desarrollo.

__
```
flask cli seed_db # Crea usuario: "admin" con password "1234"
```
__  
Correr el servidor de desarrollo especificando la configuración  
```flask -e settings.env run --debug --reload```  

Una vez iniciado, podemos ir a para disfrutar de nuestro swagger. 
http://127.0.0.1:5000/openapi/docs/

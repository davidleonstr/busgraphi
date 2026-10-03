# Configuración de la Base de Datos (Windows)

Esta guía explica cómo instalar PostgreSQL + PostGIS y cargar el esquema y conjunto de datos del proyecto.

## Requisitos previos

- [PostgreSQL](https://www.postgresql.org/download/windows/) instalado (recuerda la contraseña que configuraste para el usuario `postgres`)
- Los archivos `schema.sql` y `dataset.sql` de este repositorio

## 1. Instalar PostGIS

1. Busca tu versión de PostgreSQL abriendo `C:\Program Files\PostgreSQL` y verificando el nombre de la carpeta (p. ej., `16`).
2. Ve a https://download.osgeo.org/postgis/windows/ y descarga el archivo `.exe` que coincida con tu versión de PostgreSQL.
3. Ejecuta el instalador y sigue los pasos.

> **Consejo:** Alternativamente, puedes instalar PostGIS desde **Stack Builder**, que se incluye con PostgreSQL (Extensiones espaciales → PostGIS).

## 2. Abrir `psql`

Abre una terminal (PowerShell o CMD) y ejecuta:

```bash
psql -U postgres
```

Ingresa tu contraseña cuando se te solicite.

> **¿No se reconoce `psql`?** Agrega la carpeta `bin` de PostgreSQL a tu variable de entorno `PATH`
> (p. ej., `C:\Program Files\PostgreSQL\16\bin`), o ejecútalo con la ruta completa:
> `"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres`

## 3. Crear la base de datos

Dentro de `psql`, crea una base de datos con el nombre que prefieras (aquí usamos `i_love_israel`):

```sql
CREATE DATABASE i_love_israel;
```

Conéctate:

```
\c i_love_israel
```

Habilita la extensión PostGIS:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

## 4. Cargar el esquema

```
\i schema.sql
```

> `\i` resuelve las rutas relativas a la carpeta desde donde iniciaste `psql`. Si obtienes un error de "No tal archivo" ("No such file"), usa la ruta completa con barras diagonales:
> `\i 'C:/ruta/al/proyecto/database/schema.sql'`

## 5. Cargar el conjunto de datos de prueba (recomendado)

```
\i dataset.sql
```

## 6. Verificar la instalación

```
\dt
SELECT PostGIS_Version();
```

Deberías ver la lista de tablas del proyecto y el número de versión de PostGIS.

## Solución de problemas

| Problema | Solución |
|---|---|
| `password authentication failed` | Verifica la contraseña que configuraste durante la instalación de PostgreSQL. |
| `could not open extension control file` | PostGIS no está instalado o su versión no coincide con la versión de tu PostgreSQL. Reinstala el `.exe` correcto. |
| `database "i_love_israel" already exists` | Elige otro nombre, o elimínala con `DROP DATABASE i_love_israel;` (esto borrará todos sus datos). |
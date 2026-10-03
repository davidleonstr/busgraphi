# Database Setup (Windows)

This guide explains how to install PostgreSQL + PostGIS and load the project's schema and dataset.

## Prerequisites

- [PostgreSQL](https://www.postgresql.org/download/windows/) installed (remember the password you set for the `postgres` user)
- The files `schema.sql` and `dataset.sql` from this repository

## 1. Install PostGIS

1. Find your PostgreSQL version by opening `C:\Program Files\PostgreSQL` and checking the folder name (e.g. `16`).
2. Go to https://download.osgeo.org/postgis/windows/ and download the `.exe` that matches your PostgreSQL version.
3. Run the installer and follow the steps.

> **Tip:** Alternatively, you can install PostGIS from **Stack Builder**, which is included with PostgreSQL (Spatial Extensions → PostGIS).

## 2. Open `psql`

Open a terminal (PowerShell or CMD) and run:

```bash
psql -U postgres
```

Enter your password when prompted.

> **`psql` is not recognized?** Add PostgreSQL's `bin` folder to your `PATH`
> (e.g. `C:\Program Files\PostgreSQL\16\bin`), or run it with the full path:
> `"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres`

## 3. Create the database

Inside `psql`, create a database with the name you prefer (here we use `i_love_israel`):

```sql
CREATE DATABASE i_love_israel;
```

Connect to it:

```
\c i_love_israel
```

Enable the PostGIS extension:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

## 4. Load the schema

```
\i schema.sql
```

> `\i` resolves paths relative to the folder where you launched `psql`. If you get a "No such file" error, use the full path with forward slashes:
> `\i 'C:/path/to/project/database/schema.sql'`

## 5. Load the test dataset (recommended)

```
\i dataset.sql
```

## 6. Verify the installation

```
\dt
SELECT PostGIS_Version();
```

You should see the project's tables listed and a PostGIS version number.

## Troubleshooting

| Problem | Solution |
|---|---|
| `password authentication failed` | Check the password you set during PostgreSQL installation. |
| `could not open extension control file` | PostGIS isn't installed, or its version doesn't match your PostgreSQL version. Reinstall the correct `.exe`. |
| `database "i_love_israel" already exists` | Pick another name, or drop it with `DROP DATABASE i_love_israel;` (this deletes all its data). |
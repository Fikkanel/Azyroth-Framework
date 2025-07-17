# database/migrations/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# --- Bagian Kustom untuk Azyroth ---
# Menambahkan root direktori proyek ke path agar bisa import 'app'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Muat variabel dari file .env
load_dotenv(os.path.join(project_root, '.env'))

# Impor Base dari model Anda agar Alembic tahu tentang tabel-tabelnya
from app.Models.User import Base
# ------------------------------------

# Ini adalah konfigurasi Alembic, yang membaca dari alembic.ini
config = context.config

# Interpretasi file config untuk logging Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tambahkan metadata model Anda di sini untuk mendukung 'autogenerate'
target_metadata = Base.metadata

def get_database_url():
    """Membaca konfigurasi DB dari environment variables."""
    user = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_DATABASE")
    # Sesuaikan driver jika Anda menggunakan db selain mysql
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

def run_migrations_offline() -> None:
    """Jalankan migrasi dalam mode 'offline'.
    Ini mengkonfigurasi konteks hanya dengan URL dan bukan Engine,
    meskipun Engine juga dapat diterima di sini. Dengan melewati panggilan create_engine()
    kita bahkan tidak memerlukan DBAPI yang tersedia.
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Jalankan migrasi dalam mode 'online'.
    Dalam skenario ini kita memerlukan Engine dan mengasosiasikan
    koneksi dengannya.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
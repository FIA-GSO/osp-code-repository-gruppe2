import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from flask import current_app

# Alembic Config
config = context.config

# Logging nur konfigurieren, wenn ini vorhanden ist
if config.config_file_name:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")


def get_engine():
    """Kompatibel zu Flask-SQLAlchemy <3 und >=3"""
    migrate_ext = current_app.extensions["migrate"]
    db = migrate_ext.db
    # Flask-SQLAlchemy>=3
    if hasattr(db, "engine"):
        return db.engine
    # Flask-SQLAlchemy<3
    return db.get_engine()


def get_engine_url():
    """URL der aktuell konfigurierten Engine (als String)"""
    eng = get_engine()
    try:
        return eng.url.render_as_string(hide_password=False).replace("%", "%%")
    except Exception:
        return str(eng.url).replace("%", "%%")


def get_metadata():
    """SQLAlchemy MetaData für Autogenerate"""
    db = current_app.extensions["migrate"].db
    if hasattr(db, "metadatas"):
        return db.metadatas[None]
    return db.metadata


def run_migrations_offline():
    """Offline: keine DB-Verbindung nötig"""
    url = get_engine_url()
    config.set_main_option("sqlalchemy.url", url)

    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online: echte DB-Verbindung"""
    url = get_engine_url()
    config.set_main_option("sqlalchemy.url", url)

    # Callback: keine leere Migration generieren
    def process_revision_directives(ctx, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    conf_args = current_app.extensions["migrate"].configure_args
    conf_args.setdefault("process_revision_directives", process_revision_directives)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
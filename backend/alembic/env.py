from logging.config import fileConfig
from pkgutil import iter_modules
from sqlalchemy.orm import DeclarativeBase, class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
import importlib
from types import ModuleType
#from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config import settings
from app.core.database import Base
from app import models

# delete the "+psycopg" for forced psycog to classical mode synchrone
def getUrl():
    url = str(settings.SQLALCHEMY_DATABASE_URI)
    return url.replace("postgresql+psycopg://", "postgresql://")

# this function recursively make sure all models are imported
# so that Alembic can detect them for migrations.
# it is necessary to import all models before running migrations
# because Alembic needs to know about all models to generate migrations.
# this is a workaround to avoid having to import each model manually.
# it will import all models in the models package and its subpackages.
# it is not necessary to import models that are not used in the application,
# but it is a good practice to import all models to ensure that they are registered in the metadata.
# this is necessary for Alembic to detect changes in the models and generate migrations.
def recursive_import_models(package: ModuleType):
    for _, name, is_pkg in iter_modules(package.__path__, package.__name__ + "."):
        imported = importlib.import_module(name)
        if is_pkg:
            recursive_import_models(imported)

recursive_import_models(models)

# this function validates that all relationships are correctly defined
# it checks that each relationship has a corresponding back_populates in the target model.
# it will print an error message if a relationship is not correctly defined.
def validate_relationships(base_class: DeclarativeBase):
    for cls in base_class.registry.mappers:
        model_cls = cls.class_
        try:
            mapper = class_mapper(model_cls)
        except UnmappedClassError:
            continue
        for prop in mapper.relationships:
            if prop.back_populates:
                target_cls = prop.entity.class_
                target_mapper = class_mapper(target_cls)
                if prop.back_populates not in target_mapper.relationships:
                    print(
                        f"[ERREUR] Dans {model_cls.__name__}.{prop.key}, "
                        f"`back_populates='{prop.back_populates}'` introuvable dans {target_cls.__name__}"
                    )


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the sqlalchemy.url option in the Alembic config
# to the database URL from the settings.
if settings.SQLALCHEMY_DATABASE_URI:
    # Set the sqlalchemy.url option in the Alembic config
    # to the database URL from the settings.
    config.set_main_option("sqlalchemy.url", getUrl())
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
validate_relationships(Base)
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    
    context.configure(
        url=getUrl(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    """connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    """
    
    from sqlalchemy import create_engine
    connectable = create_engine(getUrl(), poolclass=pool.NullPool)
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

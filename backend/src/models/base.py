from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    A single Base class for all the SQLAlchemy models to inherit from.

    Each instance of a class that inherits from DeclarativeBase will create its own metadata. By having each model
    inherit from this Base class, we can ensure that all the metadata is shared across all the models.
    """
    pass

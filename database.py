# Importamos las dependencias necesarias de SQLAlchemy
from sqlalchemy import create_engine  # Para crear el motor de conexión con la base de datos
from sqlalchemy.ext.declarative import declarative_base  # Para crear la clase base de los modelos
from sqlalchemy.orm import sessionmaker  # Para crear la clase que gestiona las sesiones de la base de datos
from os import getenv  # Para obtener variables de entorno desde el sistema
from dotenv import load_dotenv  # Para cargar el archivo .env y acceder a sus variables

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Motor de la base de datos
# `create_engine` se usa para crear un motor de base de datos que SQLAlchemy utilizará para conectar con la base de datos.
# La URL de la base de datos se obtiene desde las variables de entorno usando `getenv("DATABASE_URL")`.
# `connect_args={"charset": "utf8mb4"}` es un argumento adicional para asegurarse de que la base de datos use el juego de caracteres utf8mb4.
engine = create_engine(getenv("DATABASE_URL"), connect_args={"charset": "utf8mb4"})

# Clase base para los modelos
# `declarative_base` es una función que proporciona la clase base de la que deben heredar todos los modelos (tablas) de SQLAlchemy.
# Esta clase base se usará para definir la estructura de nuestras tablas en la base de datos.
Base = declarative_base()

# Sesión local
# `sessionmaker` es una fábrica de clases que nos permite crear sesiones que se usan para interactuar con la base de datos.
# `autocommit=False` significa que las transacciones no se confirman automáticamente; `autoflush=False` significa que las consultas no se ejecutan de forma automática.
# `bind=engine` vincula la sesión al motor de base de datos que definimos previamente.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    # Abrir una nueva sesión de base de datos
    db = SessionLocal()
    try:
        yield db  # Retornar la sesión de base de datos
    finally:
        db.close()  # Cerrar la sesión de base de datos cuando termine

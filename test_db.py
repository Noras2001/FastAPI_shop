from app.models import Base, engine

# Crear las tablas
Base.metadata.create_all(bind=engine)
print("Tablas creadas con éxito.")

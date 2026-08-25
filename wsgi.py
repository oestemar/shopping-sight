print("WSGI: start import")

from app import create_app

print("WSGI: before create_app")

app = create_app()

print("WSGI: after create_app")

import app  # Import the 'app' module

# Create an instance of the WSGI application
application = app.app()  # Use a different variable name to avoid conflicts

if __name__ == "__main__":
    application.run()
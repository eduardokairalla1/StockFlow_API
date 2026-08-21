"""
Application entry point.

Initializes the Flask application using the factory and starts the development server
when this script is executed directly.
"""

from app import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)

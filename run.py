from app import create_app

app = create_app()  # This creates the app variable that Gunicorn will use

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

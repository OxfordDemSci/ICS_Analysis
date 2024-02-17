from app import create_app

app = create_app("development")

if __name__ == "__main__":
    app = create_app("local_development")
    app.run(debug=True, port=5001)

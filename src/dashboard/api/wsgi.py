from app import create_app

app = create_app("development")
print(app.config)
#app.run()

if __name__ == "__main__":
    app.run(debug=True)

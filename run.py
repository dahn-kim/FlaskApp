from app import create_app, db

app = create_app('dev')

if __name__ == "__main__":
    app.run()

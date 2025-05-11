from app import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run()
#with app.app_context(): create_all() # can be used for testing but not preferred
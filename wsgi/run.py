from fikrposdc import app
if __name__ == "__main__":
    from fikrposdc import app as application
    from fikrposdc import *
    db.create_all() #create db for each application startup
    app.run(debug=True)

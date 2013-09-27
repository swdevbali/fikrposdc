from main import app
if __name__ == "__main__":
    from main import app as application
    from main import *
    print "Create DB"
    db.create_all() #create db for each application startup
    app.run(debug=True)

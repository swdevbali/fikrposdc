from main import app
import md5

def hash_pass(password):
     """
     Return the md5 hash of the password+salt
     """
     salted_password = password + app.secret_key
     return md5.new(salted_password).hexdigest()
 

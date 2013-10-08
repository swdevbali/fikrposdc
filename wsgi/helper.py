from main import app
import md5

def hash_pass(password):
     """
     Return the md5 hash of the password+salt
     """
     salted_password = password + app.secret_key
     return md5.new(salted_password).hexdigest()
 
def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")

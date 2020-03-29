from flask import Flask, request
import psycopg2

app = Flask(__name__)
DATABASE_URL = "postgres://pqzjhlsufjnojc:92afeb211db8814c527737977cb8f4d6cf36a7449a018344744aa6174f41f125@ec2-34-200-101-236.compute-1.amazonaws.com:5432/d5asif8uu92am5"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/professions/add/', methods = ['POST'])
def add_new_professions():
    content = request.get_json()
    print(content)
    # title = request
    # description
    # ProfessionID
    # return

@app.route('/professions/all/', methods = ['GET'])
def get_all_professions():
    return "All professions"

@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)

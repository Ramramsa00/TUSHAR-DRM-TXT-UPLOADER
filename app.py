from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Ram Ram from ❣𓊈Ⅾ𝔯Ṃũ𝕤īcī𝗮𝚗𓊉❣(✿◠‿◠)'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

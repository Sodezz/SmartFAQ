from app.main import app

@app.get("/")
def main():
    print("Hello")
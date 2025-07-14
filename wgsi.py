# wsgi.py
from myclinic import create_app

app = create_app()      # ← builds and exports the Flask instance

# (Optional) Only runs locally if you call `python wsgi.py`
if __name__ == "__main__":
    app.run(debug=True)

from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Role, Review
import unittest

app = create_app("development")
migrate = Migrate(app, db)

@app.cli.command()
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Role': Role, 'Review': Review}

if __name__ == '__main__':
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    app.run(debug=True)

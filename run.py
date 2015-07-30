#/usr/bin/env python
from catalog_project import app, manager


if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0', port=5000, debug=True)

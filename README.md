# joblet.common
A simple app boilerplate, written in Python.


## Usage
First, add a `settings.py`, like this:

```python
# settings.py

REQUIRED_COMPONENTS = (
    'database',
)

DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'USER': 'some-user',
        'PASSWORD': 'some-password',
        'DBNAME': 'some-database'
    },
    'other': {
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'USER': 'some-user',
        'PASSWORD': 'some-password',
        'DBNAME': 'some-database'
    }
}
```

and put this to some directory, like `settings/`, then the settings module will be `settings.settings`.

Secondly, set environment variable `JOBLET_CONFIG`, for example:
```bash
export JOBLET_CONFIG=settings.settings
```

Finally, invoke resources initialized by joblet.common, for example:
```python
import sqlalchemy as sa
from common.holder import Holder

holder = Holder()  # Initialize global holder

db = holder.db  # Invoke managed database connection (SQLAlchemy Engine)
                # Select "default" database by default.

other_db = holder.db.other  # Invoke managed database named "other" in settings.DATABASES

# Write some model.
class SomeModel(db.Base):
    name = sa.Column(sa.String(), nullable=False, default='')


# Do query
db.session.query(SomeModel).filter(SomeModel.name == "some-value")

# Launch interactive shell
holder.shell()
```


## Supported components, and TODOs.
#### Supported
- SQLAlchemy supported databases.


#### TODOs

**Pluggable components**
- MongoDB
- Redis
- API Server (RESTful or/and RPC)


## License
BSD 3-Clause License

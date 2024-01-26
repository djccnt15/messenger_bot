# Simple Messenger Alarm Bot

Simple Alarm Bot for messengers

## Requires

- Python 3.11
- requirements.txt

## Alembic

how to revision with Alembic

### initialize

```
alembic init migrations
```

### Alembic setting

- set DB info to `alembic.ini`

```
sqlalchemy.url = mysql+pymysql://root:admin1015*@localhost:3306/mydb
```

- add table metadata to `migrations/env.py`

```python
from src.db.entity import *

target_metadata = BaseEntity.metadata
```

### create Alembic revision

```
alembic revision --autogenerate
```

### run Alembic revision to head

```
alembic upgrade head
```

## Messengers

API list done

- [x] Telegram
- [ ] Line
- [ ] KakaoTalk

### Messenger API Docs

- [Telegram Bot API](https://core.telegram.org/bots/api)
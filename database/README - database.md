# Database

The database is a SQLite file at `data/app.db` (repo root), managed with [yoyo-migrations](https://ollycope.com/software/yoyo/latest/).

## Setup
```bash
pip install -r database/requirements.txt
```

## Running migrations
All commands must be run from the `database/` directory, since `yoyo.ini` paths (`sources`, `database`) are relative to it.

```bash
cd database
```

**Apply all pending migrations:**
```bash
yoyo apply
```

**Rollback the most recent migration:**
```bash
yoyo rollback
```

**Check migration status:**
```bash
yoyo list
```

**Create a new migration file:**
```bash
yoyo new -m "add example table"
```

`batch_mode` is enabled in `yoyo.ini`, so these commands run without interactive confirmation prompts.

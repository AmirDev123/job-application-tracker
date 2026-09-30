# job-application-tracker

A command-line tool to track every job you apply to — status, notes, dates, and statistics.

## Features

- Add applications with company, role, URL, and notes
- Update status through the full hiring pipeline
- Filter by status (applied / phone_screen / interview / offer / rejected / withdrawn)
- Bar-chart summary of applications by stage
- All data stored locally in SQLite

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py add "Acme Corp" "Backend Developer" --url https://acme.com/jobs/1
python main.py add "Startup X" "Senior Python Dev" --notes "Referral from Alice"
python main.py list
python main.py list --status interview
python main.py status 1 interview
python main.py status 2 rejected
python main.py notes 1 "Second round scheduled for next week"
python main.py summary
python main.py delete 1
```

## Example output

```
$ python main.py summary

────────────────────────────────────────
  Total applications : 12
  Active             : 5

  By status:
    applied         6  ██████
    interview       2  ██
    offer           1  █
    rejected        3  ███
────────────────────────────────────────
```

## Running tests

```bash
pytest tests/
```

## Project structure

```
job-application-tracker/
├── tracker/
│   ├── models.py    # JobApplication dataclass
│   ├── storage.py   # SQLite CRUD operations
│   └── stats.py     # Summary and table output
├── tests/
│   └── test_tracker.py
├── main.py
└── requirements.txt
```

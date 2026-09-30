#!/usr/bin/env python3
"""
Job Application Tracker — keep track of every position you apply to.

Usage:
    python main.py add "Acme Corp" "Backend Developer" --url https://acme.com/jobs/1
    python main.py list
    python main.py status 1 interview
    python main.py notes 1 "Great team, re-interview scheduled"
    python main.py delete 1
    python main.py summary
"""
import argparse

from tracker.models import JobApplication
from tracker.stats import print_table, summary
from tracker.storage import add, delete, list_all, update_notes, update_status

VALID_STATUSES = ["applied", "phone_screen", "interview", "offer", "rejected", "withdrawn"]


def main():
    parser = argparse.ArgumentParser(description="Job Application Tracker")
    parser.add_argument("--db", default="jobs.db")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Track a new application")
    p_add.add_argument("company")
    p_add.add_argument("role")
    p_add.add_argument("--url", default="")
    p_add.add_argument("--notes", default="")
    p_add.add_argument("--date", dest="applied_date", default=None)

    p_list = sub.add_parser("list", help="List applications")
    p_list.add_argument("--status", choices=VALID_STATUSES, default=None)
    p_list.add_argument("--notes", action="store_true", help="Show notes column")

    p_status = sub.add_parser("status", help="Update application status")
    p_status.add_argument("id", type=int)
    p_status.add_argument("status", choices=VALID_STATUSES)

    p_notes = sub.add_parser("notes", help="Update notes for an application")
    p_notes.add_argument("id", type=int)
    p_notes.add_argument("text", nargs="+")

    p_del = sub.add_parser("delete", help="Delete an application")
    p_del.add_argument("id", type=int)

    sub.add_parser("summary", help="Show statistics")

    args = parser.parse_args()

    if args.cmd == "add":
        app = JobApplication(
            company=args.company,
            role=args.role,
            url=args.url,
            notes=args.notes,
        )
        if args.applied_date:
            app.applied_date = args.applied_date
        new_id = add(app, args.db)
        print(f"Added application #{new_id}: {args.role} @ {args.company}")

    elif args.cmd == "list":
        apps = list_all(args.status, args.db)
        print_table(apps, args.notes)

    elif args.cmd == "status":
        ok = update_status(args.id, args.status, args.db)
        if ok:
            print(f"Updated #{args.id} status → {args.status}")
        else:
            print(f"Application #{args.id} not found.")

    elif args.cmd == "notes":
        ok = update_notes(args.id, " ".join(args.text), args.db)
        if ok:
            print(f"Notes updated for #{args.id}")
        else:
            print(f"Application #{args.id} not found.")

    elif args.cmd == "delete":
        ok = delete(args.id, args.db)
        if ok:
            print(f"Deleted application #{args.id}")
        else:
            print(f"Application #{args.id} not found.")

    elif args.cmd == "summary":
        summary(args.db)


if __name__ == "__main__":
    main()

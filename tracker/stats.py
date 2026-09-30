"""Statistics and reporting for job applications."""
from collections import Counter

from .storage import list_all


def summary(db_path: str = "jobs.db") -> None:
    apps = list_all(db_path=db_path)
    if not apps:
        print("No applications tracked yet.")
        return

    counts = Counter(a.status for a in apps)
    active = sum(1 for a in apps if a.is_active())
    print(f"\n{'─'*40}")
    print(f"  Total applications : {len(apps)}")
    print(f"  Active             : {active}")
    print(f"\n  By status:")
    for status in ["applied", "phone_screen", "interview", "offer", "rejected", "withdrawn"]:
        n = counts.get(status, 0)
        if n:
            bar = "█" * n
            print(f"    {status:<15} {n:>3}  {bar}")
    print(f"{'─'*40}\n")


def print_table(apps, show_notes: bool = False) -> None:
    if not apps:
        print("No applications found.")
        return

    STATUS_COLORS = {
        "applied": "", "phone_screen": "", "interview": "",
        "offer": "", "rejected": "", "withdrawn": "",
    }

    print(f"\n{'ID':<5} {'Applied':<12} {'Company':<22} {'Role':<25} {'Status':<15}")
    print("─" * 82)
    for a in apps:
        print(f"{a.id:<5} {a.applied_date:<12} {a.company[:21]:<22} {a.role[:24]:<25} {a.status:<15}")
        if show_notes and a.notes:
            print(f"      Notes: {a.notes}")
    print()

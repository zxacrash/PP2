import csv
import json
import os
from datetime import datetime
import psycopg2
import psycopg2.extras
from connect import connect

def _conn(): return connect()
def _fmt_date(d): return d.isoformat() if d else ""
def _parse_date(s):
    try: return datetime.strptime((s or "").strip(), "%Y-%m-%d").date() if (s or "").strip() else None
    except ValueError: print(f"  ⚠  Invalid date '{s}'"); return None

def _print(rows):
    if not rows: print("  (no contacts found)"); return
    print("-" * 60)
    for r in rows: print(f"  [{r[0]:>4}]  {r[1]}  📞 {r[2]}")
    print("-" * 60)

# ── Schema ───────────────────────────────────────────────────

def init_schema():
    base = os.path.dirname(os.path.abspath(__file__))
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL
            );
        """)
        for fname in ("functions.sql", "procuders.sql"):
            fpath = os.path.join(base, fname)
            if os.path.exists(fpath):
                cur.execute(open(fpath, encoding="utf-8").read())
    conn.commit(); conn.close()
    print("✅  Schema applied.")

# ── CRUD ─────────────────────────────────────────────────────

def add_contact():
    name, phone = input("Name: ").strip(), input("Phone: ").strip()
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur: cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit(); conn.close()
    print(f"✅  Saved: {name}")

def delete_contact():
    term = input("Name or phone to delete: ").strip()
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur: cur.execute("CALL delete_contact(%s)", (term,))
    conn.commit(); conn.close()
    print("✅  Deleted.")

def bulk_insert():
    print("Enter 'name,phone' lines (empty line to finish):")
    names, phones = [], []
    while True:
        line = input("  > ").strip()
        if not line: break
        parts = line.split(",", 1)
        if len(parts) == 2: names.append(parts[0].strip()); phones.append(parts[1].strip())
        else: print("  ⚠  Format: name,phone")
    if not names: return
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (names, phones, []))
        errors = cur.fetchone()[0]
        if errors: print(f"  ⚠  Skipped: {errors}")
    conn.commit(); conn.close()
    print("✅  Bulk insert done.")

# ── Search & Browse ──────────────────────────────────────────

def search_contacts():
    query = input("Search query: ").strip()
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()
    conn.close(); _print(rows)

def show_all():
    order = {"1": "name", "2": "id"}.get(input("Sort: 1)Name 2)ID [1]: ").strip() or "1", "name")
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name, phone FROM contacts ORDER BY {order}")
        rows = cur.fetchall()
    conn.close(); _print(rows)

def paginated_browse():
    page_size, page = 5, 0
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM contacts"); total = cur.fetchone()[0]
    conn.close()
    total_pages = max(1, (total + page_size - 1) // page_size)
    while True:
        conn = _conn()
        if not conn: return
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, page * page_size))
            rows = cur.fetchall()
        conn.close()
        print(f"\n── Page {page+1}/{total_pages} ──"); _print(rows)
        cmd = input("[N]ext [P]rev [Q]uit: ").strip().lower()
        if   cmd == "n": page = min(page + 1, total_pages - 1)
        elif cmd == "p": page = max(page - 1, 0)
        elif cmd == "q": break

# ── Import / Export ───────────────────────────────────────────

def export_json():
    fp = input("File path [contacts_export.json]: ").strip() or "contacts_export.json"
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, phone FROM contacts ORDER BY name")
        rows = cur.fetchall()
    conn.close()
    json.dump([{"id":r[0],"name":r[1],"phone":r[2]} for r in rows], open(fp,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"✅  Exported {len(rows)} contacts to '{fp}'.")

def import_json():
    fp = input("File path [contacts_export.json]: ").strip() or "contacts_export.json"
    if not os.path.exists(fp): print(f"  ✗  Not found: {fp}"); return
    records = json.load(open(fp, encoding="utf-8"))
    conn = _conn()
    if not conn: return
    with conn.cursor() as cur:
        for r in records: cur.execute("CALL upsert_contact(%s, %s)", (r["name"], r["phone"]))
    conn.commit(); conn.close()
    print(f"✅  Imported {len(records)} contacts.")

def import_csv():
    fp = input("CSV file path [contacts.csv]: ").strip() or "contacts.csv"
    if not os.path.exists(fp): print(f"  ✗  Not found: {fp}"); return
    conn = _conn()
    if not conn: return
    count = 0
    with open(fp, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name  = (row.get("name") or f"{row.get('first_name','')} {row.get('last_name','')}").strip()
            phone = (row.get("phone") or "").strip()
            if name and phone:
                with conn.cursor() as cur: cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
                count += 1
    conn.commit(); conn.close()
    print(f"✅  CSV import done: {count} rows.")

# ── Menu ─────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════╗
║          PhoneBook  –  Lab8          ║
╠══════════════════════════════════════╣
║  0  Apply schema & procedures        ║
║  1  Add / Update contact             ║
║  2  Delete contact                   ║
║  3  Bulk insert                      ║
║  4  Search contacts                  ║
║  5  Show all (sorted)                ║
║  6  Browse (paginated)               ║
║  7  Export to JSON                   ║
║  8  Import from JSON                 ║
║  9  Import from CSV                  ║
║  Q  Quit                             ║
╚══════════════════════════════════════╝"""

HANDLERS = {"0":init_schema,"1":add_contact,"2":delete_contact,"3":bulk_insert,
            "4":search_contacts,"5":show_all,"6":paginated_browse,
            "7":export_json,"8":import_json,"9":import_csv}

def run_phonebook():
    while True:
        print(MENU)
        choice = input("Select option: ").strip().lower()
        if choice == "q": print("Goodbye!"); break
        handler = HANDLERS.get(choice)
        if handler:
            try: handler()
            except psycopg2.Error as e: print(f"  ✗  DB error: {e.pgerror or e}")
            except KeyboardInterrupt: print()
        else: print("  Invalid choice.")

if __name__ == "__main__":
    run_phonebook()

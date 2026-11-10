#!/usr/bin/env python3
"""Pre-configure a CommStat install for receive-only use with a WebSDR.

Run once by install.sh, after CommStat has been cloned. It:

  * creates traffic.db3 from CommStat's own shipped template if there isn't one
    (exactly what CommStat's launcher would do on first run),
  * stores the user's callsign / grid / state, so CommStat starts without
    asking,
  * adds ONE JS8 connector - the local WebSDR JS8Call - with auto-connect on
    and RF Ack OFF. RF Ack is what makes CommStat automatically transmit an
    acknowledgement over the air when it receives a STATREP; there is no
    radio here, and an acknowledgement must never be triggered by traffic
    heard through someone else's receiver.
  * adds the groups to follow (DEFAULT_GROUPS, or the COMMSTAT_GROUPS
    environment variable: names separated by spaces or commas; set it to an
    empty string to add none). Groups already in CommStat are left alone.

It never overwrites anything: an existing database keeps its data, an
existing connector with the same name is left exactly as it is, and only
missing groups are added (never removed).

Usage: seed_commstat.py COMMSTAT_DIR CALLSIGN GRID STATE RIG_NAME TCP_PORT
       seed_commstat.py --groups    (print the group list and exit)
"""
import datetime
import os
import re
import shutil
import sqlite3
import sys

DEFAULT_GROUPS = ["AMRRON", "COMMSTAT", "GHOSTNET", "MAGNET", "NOMADNET", "TTP"]
MAX_GROUP_NAME_LENGTH = 8   # CommStat's own limit (constants.py)


def wanted_groups():
    env = os.environ.get("COMMSTAT_GROUPS")
    names = DEFAULT_GROUPS if env is None else re.split(r"[\s,]+", env)
    out = []
    for n in names:
        n = n.strip().lstrip("@").upper()[:MAX_GROUP_NAME_LENGTH]
        if n and n not in out:
            out.append(n)
    return out


def add_groups(db_path):
    """Add missing groups the way CommStat's Manage Groups dialog does."""
    names = wanted_groups()
    if not names:
        print("No groups to add.")
        return
    today = datetime.date.today().strftime("%Y-%m-%d")
    added = []
    with sqlite3.connect(db_path, timeout=10) as conn:
        have = {r[0].upper() for r in conn.execute("SELECT name FROM groups") if r[0]}
        for n in names:
            if n not in have:
                conn.execute(
                    "INSERT INTO groups (name, comment, url1, url2, date_added) VALUES (?, '', '', '', ?)",
                    (n, today),
                )
                added.append(n)
        conn.commit()
    if added:
        print("Added CommStat groups: " + ", ".join(added))
    else:
        print("CommStat groups already present: " + ", ".join(names))


def main(argv):
    if argv[1:] == ["--groups"]:
        # For install.sh: the same list, for the JS8Call profile's My Groups.
        print(" ".join(wanted_groups()))
        return
    if len(argv) != 7:
        sys.exit(__doc__)
    commstat_dir, callsign, grid, state, rig_name, port = argv[1:]
    port = int(port)
    db_path = os.path.join(commstat_dir, "traffic.db3")
    template = os.path.join(commstat_dir, "traffic.db3.template")

    if not os.path.isdir(commstat_dir):
        sys.exit(f"CommStat not found at {commstat_dir}")

    if not os.path.exists(db_path):
        if not os.path.exists(template):
            sys.exit(f"Neither {db_path} nor {template} exists - is this a complete CommStat checkout?")
        shutil.copy(template, db_path)
        print(f"Created {db_path} from CommStat's template.")
    else:
        print(f"Keeping existing {db_path}.")

    # Callsign / grid / state: only fill in what's still blank, so re-running
    # the installer can't overwrite settings the user has since changed in CommStat.
    with sqlite3.connect(db_path, timeout=10) as conn:
        row = conn.execute("SELECT callsign, gridsquare, state FROM controls WHERE id = 1").fetchone()
        if row is None:
            sys.exit("CommStat's database has no 'controls' row - unexpected schema.")
        cur_call, cur_grid, cur_state = (row[0] or "", row[1] or "", row[2] or "")
        conn.execute(
            "UPDATE controls SET callsign = ?, gridsquare = ?, state = ? WHERE id = 1",
            (cur_call or callsign.upper(), cur_grid or grid, cur_state or state.upper()),
        )
        conn.commit()
    print("Callsign/grid/state set (existing values kept).")

    add_groups(db_path)

    # Use CommStat's own ConnectorManager so validation and defaults are exactly
    # what its JS8 Connectors dialog would produce.
    sys.path.insert(0, commstat_dir)
    os.chdir(commstat_dir)
    from connector_manager import ConnectorManager  # noqa: E402  (needs the path set above)

    mgr = ConnectorManager(db_path)
    existing = [c for c in mgr.get_all_connectors(enabled_only=False) if c.get("rig_name") == rig_name]
    if existing:
        print(f"Connector '{rig_name}' already present - left as it is.")
        return
    ok = mgr.add_connector(
        rig_name=rig_name,
        tcp_port=port,
        server="127.0.0.1",
        state="",
        comment="Receive-only JS8Call fed by a web SDR (no radio, no TX)",
        set_as_default=True,
        auto_connect=True,
        rf_ack=False,
    )
    if not ok:
        sys.exit("CommStat refused to add the connector.")
    print(f"Added connector '{rig_name}' -> 127.0.0.1:{port} (auto-connect on, RF Ack OFF).")


if __name__ == "__main__":
    main(sys.argv)

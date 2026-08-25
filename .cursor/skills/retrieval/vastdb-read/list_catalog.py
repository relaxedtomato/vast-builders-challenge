#!/usr/bin/env python3
"""List VastDB databases, schemas, and tables via the vastdb Python SDK only."""

from __future__ import annotations

import argparse
import os
import ssl
import sys
import urllib.error
import urllib.request
from collections import defaultdict

INTERNAL_TABLES = frozenset({"tabular_schema_table"})


def normalize_endpoint(url: str) -> str:
    return url if url.startswith(("http://", "https://")) else f"http://{url}"


def resolve_credentials() -> tuple[str, str, str]:
    """Read endpoint and keys from the pre-provisioned environment."""
    endpoint = os.environ.get("VDB_ENDPOINT") or os.environ.get("S3_ENDPOINT", "")
    access = os.environ.get("ACCESS_KEY", "")
    secret = os.environ.get("SECRET_KEY", "")

    missing = [
        name
        for name, value in (("VDB_ENDPOINT", endpoint), ("ACCESS_KEY", access), ("SECRET_KEY", secret))
        if not value
    ]
    if missing:
        print(
            f"Not set in the environment: {', '.join(missing)}.\n"
            "These are provisioned for you. If they are missing, tell an organizer.",
            file=sys.stderr,
        )
        sys.exit(1)
    return normalize_endpoint(endpoint), access, secret


def probe_endpoint(endpoint: str) -> None:
    """Fail fast with a clear message if the data endpoint is unreachable."""
    try:
        urllib.request.urlopen(endpoint, timeout=5)
    except urllib.error.HTTPError:
        return  # any HTTP response means we reached it
    except ssl.SSLError:
        return  # TLS handshake happened, so the host is up; the SDK skips verification
    except OSError:
        print(
            f"Cannot reach {endpoint}. The VastDB data endpoint should be reachable from\n"
            "your VM. Check VDB_ENDPOINT, then tell an organizer.",
            file=sys.stderr,
        )
        sys.exit(1)


def parse_path_parts(parent_path: str) -> list[str]:
    return [p for p in parent_path.strip("/").split("/") if p]


def catalog_tree(endpoint: str, access: str, secret: str) -> dict[str, dict[str, list[str]]]:
    """Build database → schema → [tables] from tx.catalog() SCHEMA/TABLE rows."""
    import vastdb

    tree: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    session = vastdb.connect(endpoint=endpoint, access=access, secret=secret, ssl_verify=False)
    with session.transaction() as tx:
        catalog = tx.catalog(fail_if_missing=False)
        if catalog is None:
            return {}

        df = catalog.select(columns=["element_type", "name", "parent_path"]).read_all().to_pandas()

    for _, row in df[df["element_type"] == "SCHEMA"].iterrows():
        parts = parse_path_parts(row["parent_path"])
        if len(parts) != 1:
            continue
        tree[parts[0]][row["name"]]  # ensure schema key exists

    for _, row in df[df["element_type"] == "TABLE"].iterrows():
        if row["name"] in INTERNAL_TABLES:
            continue
        parts = parse_path_parts(row["parent_path"])
        if len(parts) != 2:
            continue
        bucket, schema = parts
        tables = tree[bucket][schema]
        if row["name"] not in tables:
            tables.append(row["name"])

    return {db: {sch: sorted(tables) for sch, tables in sorted(schemas.items())} for db, schemas in sorted(tree.items())}


def live_bucket_tree(
    endpoint: str, access: str, secret: str, bucket: str
) -> dict[str, dict[str, list[str]]]:
    """Optional live drill-down via bucket.schemas() / schema.tables() (SDK only)."""
    import vastdb
    from vastdb.errors import Conflict

    tree: dict[str, dict[str, list[str]]] = {bucket: {}}
    session = vastdb.connect(endpoint=endpoint, access=access, secret=secret, ssl_verify=False)
    with session.transaction() as tx:
        try:
            schemas = list(tx.bucket(bucket).schemas())
        except Conflict:
            return {}

        for schema in schemas:
            tables = []
            for table in schema.tables():
                if table.name not in INTERNAL_TABLES:
                    tables.append(table.name)
            tree[bucket][schema.name] = sorted(tables)
    return tree


def print_tree(tree: dict[str, dict[str, list[str]]]) -> None:
    if not tree:
        print("No VastDB databases found in catalog.")
        return

    print(f"{'DATABASE (bucket)':<40} {'SCHEMA':<30} TABLES")
    print("-" * 100)
    for bucket, schemas in tree.items():
        if not schemas:
            print(f"{bucket:<40} (no schemas)")
            continue
        for i, (schema, tables) in enumerate(sorted(schemas.items())):
            table_str = ", ".join(tables) if tables else "(no tables)"
            if i == 0:
                print(f"{bucket:<40} {schema:<30} {table_str}")
            else:
                print(f"{'':<40} {schema:<30} {table_str}")


def main() -> None:
    parser = argparse.ArgumentParser(description="List VastDB catalog via vastdb SDK")
    parser.add_argument("--bucket", help="Also verify one bucket via bucket.schemas()")
    parser.add_argument("--live-only", action="store_true", help="Use bucket.schemas() only (requires --bucket)")
    args = parser.parse_args()

    endpoint, access, secret = resolve_credentials()
    probe_endpoint(endpoint)
    print(f"VastDB endpoint: {endpoint}\n")

    if args.live_only:
        if not args.bucket:
            print("--live-only requires --bucket", file=sys.stderr)
            sys.exit(1)
        print_tree(live_bucket_tree(endpoint, access, secret, args.bucket))
        return

    tree = catalog_tree(endpoint, access, secret)
    print_tree(tree)

    if args.bucket:
        print(f"\n--- live bucket.schemas() for {args.bucket} ---")
        print_tree(live_bucket_tree(endpoint, access, secret, args.bucket))


if __name__ == "__main__":
    main()

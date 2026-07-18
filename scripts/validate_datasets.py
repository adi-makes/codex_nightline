#!/usr/bin/env python3
"""Validate Ask Kochi's curated JSON corpus without external dependencies.

The repository's schema.json is a dataset registry, not a standalone JSON Schema for
the whole directory. This command validates that registry plus minimum data-integrity
rules and can emit a machine-readable report without writing generated files.
"""

from __future__ import annotations

import argparse
import collections
import datetime as datetime
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


EXCLUDED_FILES = {"schema.json", "stats.json"}
KOCHI_LATITUDE_RANGE = (9.3, 10.4)
KOCHI_LONGITUDE_RANGE = (76.0, 77.0)


@dataclass
class Finding:
    severity: str
    path: str
    rule: str
    message: str


@dataclass
class Report:
    dataset_files: int = 0
    records: int = 0
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, path: str, rule: str, message: str) -> None:
        self.findings.append(Finding(severity, path, rule, message))

    @property
    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "warning"]


def read_json(path: Path, report: Report) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        report.add("error", path.as_posix(), "utf8", f"not valid UTF-8: {exc}")
    except json.JSONDecodeError as exc:
        report.add("error", path.as_posix(), "json", f"invalid JSON: {exc}")
    return None


def definition_for(mapping: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any] | None:
    items = mapping.get("items")
    if not isinstance(items, dict):
        return None
    reference = items.get("$ref")
    if not isinstance(reference, str) or not reference.startswith("#/definitions/"):
        return None
    name = reference.rsplit("/", maxsplit=1)[-1]
    definition = schema.get("definitions", {}).get(name)
    return definition if isinstance(definition, dict) else None


def valid_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_record(
    record: Any,
    location: str,
    required: list[str],
    report: Report,
    ids: dict[str, list[str]],
    strict_provenance: bool,
) -> None:
    if not isinstance(record, dict):
        report.add("error", location, "item-object", "array item must be an object")
        return

    missing = [field for field in required if field not in record]
    if missing:
        report.add("error", location, "required-fields", f"missing: {', '.join(missing)}")

    stable_id = record.get("id") or record.get("station_id")
    if stable_id is not None:
        if not isinstance(stable_id, str) or not stable_id.strip():
            report.add("error", location, "stable-id", "id/station_id must be a non-empty string")
        else:
            ids[stable_id].append(location)

    latitude = record.get("latitude")
    longitude = record.get("longitude")
    if (latitude is None) != (longitude is None):
        report.add("error", location, "coordinates-paired", "latitude and longitude must appear together")
    elif latitude is not None:
        coordinates_are_numbers = (
            isinstance(latitude, (int, float))
            and not isinstance(latitude, bool)
            and isinstance(longitude, (int, float))
            and not isinstance(longitude, bool)
        )
        if not coordinates_are_numbers:
            report.add("error", location, "coordinates-type", "latitude and longitude must be numbers")
        elif not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            report.add("error", location, "coordinates-range", "coordinate outside WGS84 range")
        elif not (
            KOCHI_LATITUDE_RANGE[0] <= latitude <= KOCHI_LATITUDE_RANGE[1]
            and KOCHI_LONGITUDE_RANGE[0] <= longitude <= KOCHI_LONGITUDE_RANGE[1]
        ):
            report.add(
                "warning",
                location,
                "kochi-area-sanity",
                f"coordinate {latitude}, {longitude} is outside the broad Kochi-area window",
            )

    if "estimated" in record and not isinstance(record["estimated"], bool):
        report.add("error", location, "estimated-type", "estimated must be boolean")
    if "last_verified" in record and not valid_iso_date(record["last_verified"]):
        report.add("error", location, "last-verified-date", "last_verified must be ISO YYYY-MM-DD")

    has_source = isinstance(record.get("source"), str) and bool(record["source"].strip())
    has_verified_date = "last_verified" in record and valid_iso_date(record["last_verified"])
    if strict_provenance and not has_source:
        report.add("error", location, "provenance-source", "source is required in strict provenance mode")
    if strict_provenance and not has_verified_date:
        report.add(
            "error",
            location,
            "provenance-last-verified",
            "last_verified is required in strict provenance mode",
        )


def validate(root: Path, strict_provenance: bool) -> Report:
    report = Report()
    schema_path = root / "schema.json"
    stats_path = root / "stats.json"
    schema = read_json(schema_path, report)
    stats = read_json(stats_path, report)
    if not isinstance(schema, dict) or not isinstance(stats, dict):
        return report

    dataset_mappings = schema.get("datasets")
    definitions = schema.get("definitions")
    if not isinstance(dataset_mappings, dict):
        report.add("error", schema_path.as_posix(), "dataset-registry", "datasets must be an object")
        return report
    if not isinstance(definitions, dict):
        report.add("error", schema_path.as_posix(), "definitions", "definitions must be an object")
        return report

    for name, definition in definitions.items():
        if not isinstance(definition, dict):
            report.add("error", schema_path.as_posix(), "definition-object", f"{name} must be an object")
            continue
        if not isinstance(definition.get("required"), list):
            report.add("error", schema_path.as_posix(), "definition-required", f"{name} has no required array")
        if not isinstance(definition.get("properties"), dict):
            report.add(
                "warning",
                schema_path.as_posix(),
                "definition-properties",
                f"{name} has no properties/type constraints; required fields alone cannot validate shape",
            )

    arrays: dict[str, int] = {}
    identifiers: dict[str, list[str]] = collections.defaultdict(list)
    for path in sorted(root.rglob("*.json")):
        if path.name in EXCLUDED_FILES:
            continue
        relative = path.relative_to(root).as_posix()
        value = read_json(path, report)
        if not isinstance(value, list):
            report.add("error", relative, "top-level-array", "dataset must be a JSON array")
            continue
        report.dataset_files += 1
        arrays[relative] = len(value)
        mapping = dataset_mappings.get(relative)
        if not isinstance(mapping, dict):
            report.add("error", relative, "schema-coverage", "dataset has no schema registry entry")
            continue
        definition = definition_for(mapping, schema)
        if definition is None:
            report.add(
                "error",
                relative,
                "item-contract",
                "schema registry declares only an array; define an item contract before this data is trusted",
            )
            required: list[str] = []
        else:
            required = definition.get("required", [])
            if not isinstance(required, list) or not all(isinstance(field, str) for field in required):
                report.add("error", relative, "required-fields", "schema definition has invalid required fields")
                required = []
        for index, record in enumerate(value):
            report.records += 1
            validate_record(record, f"{relative}[{index}]", required, report, identifiers, strict_provenance)

    for relative in dataset_mappings:
        if relative not in arrays:
            report.add("error", relative, "schema-file", "schema registry references a missing/non-array dataset")

    for stable_id, locations in sorted(identifiers.items()):
        if len(locations) > 1:
            report.add("error", stable_id, "duplicate-stable-id", "; ".join(locations))

    declared_counts = stats.get("datasets")
    if not isinstance(declared_counts, dict):
        report.add("error", stats_path.as_posix(), "dataset-counts", "datasets must be an object")
    else:
        for relative, count in arrays.items():
            if declared_counts.get(relative) != count:
                report.add(
                    "error",
                    stats_path.as_posix(),
                    "dataset-count",
                    f"{relative}: expected {count}, found {declared_counts.get(relative)!r}",
                )
        for relative in declared_counts:
            if relative not in arrays:
                report.add("error", stats_path.as_posix(), "orphan-count", f"{relative} has no dataset file")
    return report


def emit_text(report: Report) -> None:
    print(f"Dataset files: {report.dataset_files}")
    print(f"Records: {report.records}")
    print(f"Errors: {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")
    for finding in report.findings:
        print(f"{finding.severity.upper()} {finding.path} [{finding.rule}]: {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("datasets"), help="dataset directory")
    parser.add_argument(
        "--strict-provenance",
        action="store_true",
        help="require source and last_verified on every record",
    )
    parser.add_argument("--json", action="store_true", help="emit a JSON report to stdout")
    args = parser.parse_args()

    report = validate(args.root, args.strict_provenance)
    if args.json:
        print(
            json.dumps(
                {
                    "dataset_files": report.dataset_files,
                    "records": report.records,
                    "errors": len(report.errors),
                    "warnings": len(report.warnings),
                    "findings": [asdict(finding) for finding in report.findings],
                },
                indent=2,
            )
        )
    else:
        emit_text(report)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

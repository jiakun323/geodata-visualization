#!/usr/bin/env python3
"""Validate the GeoJSON and its repository-relative media references."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

NUMERIC_FIELDS = {
    "heart_rate", "rr", "temperature", "attention", "relaxation",
    "sync_rate", "mental_effort", "familiarity", "pitch", "yaw", "roll",
    "delta", "theta", "low_alpha", "high_alpha", "alpha", "low_beta",
    "high_beta", "beta", "low_gamma", "mid_gamma", "gamma"
}

REQUIRED_FIELDS = NUMERIC_FIELDS | {
    "record_id", "timestamp", "image", "spectrogram",
    "audio", "event_mark", "interpolated_fields"
}


def is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "geojson",
        nargs="?",
        default="data/biometric_multi_metric_with_spectrogram.geojson",
    )
    parser.add_argument(
        "--strict-assets",
        action="store_true",
        help="Fail when a referenced image, spectrogram, or audio file is missing.",
    )
    args = parser.parse_args()

    geojson_path = Path(args.geojson).resolve()
    repository_root = geojson_path.parent.parent

    errors: list[str] = []
    missing_assets: list[str] = []

    try:
        data = json.loads(geojson_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read GeoJSON: {exc}")
        return 1

    if data.get("type") != "FeatureCollection":
        errors.append("Root type must be FeatureCollection.")

    features = data.get("features")
    if not isinstance(features, list) or not features:
        errors.append("features must be a non-empty list.")
        features = []

    seen_ids: set[str] = set()

    for index, feature in enumerate(features):
        label = f"feature[{index}]"
        geometry = feature.get("geometry") or {}
        properties = feature.get("properties") or {}

        if geometry.get("type") != "Point":
            errors.append(f"{label}: geometry must be Point.")

        coordinates = geometry.get("coordinates")
        if (
            not isinstance(coordinates, list)
            or len(coordinates) < 2
            or not all(is_finite_number(value) for value in coordinates[:2])
        ):
            errors.append(f"{label}: invalid coordinates.")
        else:
            longitude, latitude = coordinates[:2]
            if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
                errors.append(f"{label}: coordinates are outside valid ranges.")

        missing_fields = sorted(REQUIRED_FIELDS - properties.keys())
        if missing_fields:
            errors.append(
                f"{label}: missing properties: {', '.join(missing_fields)}"
            )

        record_id = str(properties.get("record_id") or "").strip()
        if not record_id:
            errors.append(f"{label}: record_id is empty.")
        elif record_id in seen_ids:
            errors.append(f"{label}: duplicate record_id {record_id}.")
        seen_ids.add(record_id)

        for field in NUMERIC_FIELDS:
            if field in properties and not is_finite_number(properties[field]):
                errors.append(f"{label}: {field} must be a finite number.")

        for field in ("image", "spectrogram", "audio"):
            asset_path = str(properties.get(field) or "").strip()
            if asset_path and not (repository_root / asset_path).is_file():
                missing_assets.append(asset_path)

    metadata_count = (data.get("metadata") or {}).get("point_count")
    if metadata_count is not None and metadata_count != len(features):
        errors.append(
            f"metadata.point_count is {metadata_count}, "
            f"but features contains {len(features)} records."
        )

    print(f"Validated records: {len(features)}")

    if missing_assets:
        unique_assets = sorted(set(missing_assets))
        preview = ", ".join(unique_assets[:5])
        remainder = len(unique_assets) - min(5, len(unique_assets))
        suffix = f", … and {remainder} more" if remainder else ""
        print(
            f"WARNING: {len(unique_assets)} referenced media file(s) are missing: "
            f"{preview}{suffix}"
        )
        if args.strict_assets:
            errors.append(
                "Media validation failed because --strict-assets was supplied."
            )

    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("Validation failed.")
        return 1

    print("GeoJSON structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

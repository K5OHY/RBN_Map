#!/usr/bin/env python3
import csv
import maidenhead as mh

RAW_FILE = "spotters_raw.txt"
OUT_FILE = "spotter_coords.csv"


def grid_to_latlon(grid: str):
    """
    Convert Maidenhead grid (4 or 6 chars) -> (lat, lon)
    Matches the common conversion used in ham tools.
    """
    grid = (grid or "").strip()
    if len(grid) < 4:
        raise ValueError("Grid too short")
    lat, lon = mh.to_location(grid, center=True)
    return round(lat, 3), round(lon, 3)


def main():
    rows_out = []
    seen = set()

    with open(RAW_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Skip header line
            if line.lower().startswith("callsign"):
                continue

            # Your data is TAB-separated
            parts = line.split("\t")

            # If someone pasted with spaces instead of tabs, try a fallback:
            # We only trust it if we can still find a plausible grid in column 3.
            if len(parts) < 3:
                # fallback: split on whitespace, but this is less reliable
                parts = line.split()

            if len(parts) < 3:
                continue

            callsign = (parts[0] or "").strip()
            grid = (parts[2] or "").strip()

            if not callsign or not grid:
                continue

            # Normalize callsign spacing
            callsign = " ".join(callsign.split())

            try:
                lat, lon = grid_to_latlon(grid)
            except Exception:
                # Bad/odd grid -> skip
                continue

            key = callsign.upper()
            if key in seen:
                continue
            seen.add(key)

            rows_out.append({"callsign": callsign, "latitude": lat, "longitude": lon})

    with open(OUT_FILE, "w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, fieldnames=["callsign", "latitude", "longitude"])
        w.writeheader()
        w.writerows(rows_out)

    print(f"✅ Wrote {len(rows_out)} rows to {OUT_FILE}")


if __name__ == "__main__":
    main()

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import os
import csv

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _read_csv(filename: str) -> List[dict]:
    """Read a CSV file from the data/ directory."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ──────────────────────────────────────────────
# OVERVIEW
# ──────────────────────────────────────────────

@router.get("/overview", summary="Dataset overview and high-level stats")
def get_overview():
    """Returns high-level statistics about the F1 dataset."""
    results = _read_csv("results.csv")
    drivers = _read_csv("drivers.csv")
    circuits = _read_csv("circuits.csv")
    races = _read_csv("races.csv")

    years = sorted(set(r["year"] for r in races if r.get("year"))) if races else []

    return {
        "total_race_results": len(results),
        "total_drivers": len(drivers),
        "total_circuits": len(circuits),
        "total_races": len(races),
        "years_covered": {
            "from": years[0] if years else "N/A",
            "to": years[-1] if years else "N/A",
            "count": len(years),
        },
        "data_available": {
            "results": len(results) > 0,
            "drivers": len(drivers) > 0,
            "circuits": len(circuits) > 0,
            "races": len(races) > 0,
        },
        "note": "Place your CSV files in the data/ folder at the project root to populate live stats.",
    }


# ──────────────────────────────────────────────
# DRIVERS
# ──────────────────────────────────────────────

@router.get("/drivers", summary="Top drivers by wins")
def get_drivers(limit: int = Query(10, ge=1, le=50)):
    """Returns top drivers ranked by total wins."""
    results = _read_csv("results.csv")
    drivers = _read_csv("drivers.csv")

    driver_map = {d["driverId"]: f"{d.get('forename', '')} {d.get('surname', '')}".strip() for d in drivers}
    wins = {}
    races = {}
    total_pos = {}

    for r in results:
        did = r.get("driverId", "")
        pos = r.get("positionOrder", r.get("position", ""))
        try:
            pos_int = int(pos)
        except (ValueError, TypeError):
            continue

        races[did] = races.get(did, 0) + 1
        total_pos[did] = total_pos.get(did, 0) + pos_int
        if pos_int == 1:
            wins[did] = wins.get(did, 0) + 1

    sorted_drivers = sorted(wins.keys(), key=lambda d: wins[d], reverse=True)[:limit]

    return {
        "drivers": [
            {
                "driver_id": did,
                "name": driver_map.get(did, f"Driver #{did}"),
                "wins": wins.get(did, 0),
                "races": races.get(did, 0),
                "avg_finish": round(total_pos.get(did, 0) / max(races.get(did, 1), 1), 2),
            }
            for did in sorted_drivers
        ]
    }


# ──────────────────────────────────────────────
# CONSTRUCTORS
# ──────────────────────────────────────────────

@router.get("/constructors", summary="Constructor performance stats")
def get_constructors(limit: int = Query(10, ge=1, le=50)):
    """Returns top constructors by wins."""
    results = _read_csv("results.csv")
    constructors = _read_csv("constructors.csv")

    con_map = {c["constructorId"]: c.get("name", f"Team #{c['constructorId']}") for c in constructors}
    wins = {}
    races = {}

    for r in results:
        cid = r.get("constructorId", "")
        pos = r.get("positionOrder", r.get("position", ""))
        try:
            pos_int = int(pos)
        except (ValueError, TypeError):
            continue

        races[cid] = races.get(cid, 0) + 1
        if pos_int == 1:
            wins[cid] = wins.get(cid, 0) + 1

    sorted_cons = sorted(races.keys(), key=lambda c: wins.get(c, 0), reverse=True)[:limit]

    return {
        "constructors": [
            {
                "constructor_id": cid,
                "name": con_map.get(cid, f"Team #{cid}"),
                "wins": wins.get(cid, 0),
                "race_entries": races.get(cid, 0),
            }
            for cid in sorted_cons
        ]
    }


# ──────────────────────────────────────────────
# CIRCUITS
# ──────────────────────────────────────────────

@router.get("/circuits", summary="Circuit list with details")
def get_circuits(country: Optional[str] = None):
    """Returns all circuits, optionally filtered by country."""
    circuits = _read_csv("circuits.csv")
    if country:
        circuits = [c for c in circuits if c.get("country", "").lower() == country.lower()]

    return {
        "total": len(circuits),
        "circuits": [
            {
                "circuit_id": c.get("circuitId"),
                "name": c.get("name"),
                "country": c.get("country"),
                "location": c.get("location"),
                "lat": c.get("lat"),
                "lng": c.get("lng"),
            }
            for c in circuits
        ],
    }


# ──────────────────────────────────────────────
# GRID VS FINISH ANALYSIS
# ──────────────────────────────────────────────

@router.get("/grid-analysis", summary="Grid position vs finishing position correlation")
def grid_vs_finish():
    """
    Returns aggregated data showing how often each grid position
    translates into specific finishing positions (1, podium, top10).
    """
    results = _read_csv("results.csv")
    grid_stats = {}

    for r in results:
        grid = r.get("grid", "")
        pos = r.get("positionOrder", r.get("position", ""))
        try:
            g, p = int(grid), int(pos)
        except (ValueError, TypeError):
            continue
        if not (1 <= g <= 20 and 1 <= p <= 20):
            continue

        if g not in grid_stats:
            grid_stats[g] = {"grid": g, "total": 0, "wins": 0, "podiums": 0, "top10": 0, "avg_finish": 0, "_sum": 0}

        grid_stats[g]["total"] += 1
        grid_stats[g]["_sum"] += p
        if p == 1:
            grid_stats[g]["wins"] += 1
        if p <= 3:
            grid_stats[g]["podiums"] += 1
        if p <= 10:
            grid_stats[g]["top10"] += 1

    output = []
    for g in sorted(grid_stats.keys()):
        s = grid_stats[g]
        total = s["total"] or 1
        output.append({
            "grid_position": g,
            "total_races": s["total"],
            "win_rate_pct": round(s["wins"] / total * 100, 1),
            "podium_rate_pct": round(s["podiums"] / total * 100, 1),
            "top10_rate_pct": round(s["top10"] / total * 100, 1),
            "avg_finish_position": round(s["_sum"] / total, 2),
        })

    return {"grid_analysis": output}


# ──────────────────────────────────────────────
# SEASON SUMMARY
# ──────────────────────────────────────────────

@router.get("/seasons/{year}", summary="Season summary for a given year")
def get_season(year: int):
    """Returns race results summary for a specific season."""
    races = _read_csv("races.csv")
    results = _read_csv("results.csv")
    drivers = _read_csv("drivers.csv")

    season_races = {r["raceId"]: r for r in races if r.get("year") == str(year)}
    if not season_races:
        raise HTTPException(status_code=404, detail=f"No data found for year {year}")

    driver_map = {d["driverId"]: f"{d.get('forename', '')} {d.get('surname', '')}".strip() for d in drivers}
    wins = {}

    for res in results:
        if res.get("raceId") in season_races:
            pos = res.get("positionOrder", res.get("position", ""))
            try:
                if int(pos) == 1:
                    did = res["driverId"]
                    wins[did] = wins.get(did, 0) + 1
            except (ValueError, TypeError):
                continue

    champion = max(wins, key=wins.get) if wins else None

    return {
        "year": year,
        "total_races": len(season_races),
        "unique_race_winners": len(wins),
        "champion_driver_id": champion,
        "champion_name": driver_map.get(champion, "Unknown") if champion else None,
        "champion_wins": wins.get(champion, 0) if champion else 0,
        "all_winners": [
            {"driver_id": d, "name": driver_map.get(d, f"Driver #{d}"), "wins": w}
            for d, w in sorted(wins.items(), key=lambda x: -x[1])
        ],
    }
import urllib.request
import urllib.parse
import json
import csv
import sys

API_KEY = "5511ada7264b813c62e3cf2fa95e3e1c"
BASE_URL = "https://oec.world/api/olap-proxy/data.jsonrecords"

headers = {
    "x-oec-token": API_KEY,
    "Content-Type": "application/json",
}

# Step 1: Discover available cubes to find the right one for Ukraine monthly data
print("Step 1: Discovering available cubes...")
cubes_url = "https://oec.world/api/olap-proxy/cubes"
req = urllib.request.Request(cubes_url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        cubes_data = json.loads(resp.read().decode())
        cubes = cubes_data.get("cubes", cubes_data) if isinstance(cubes_data, dict) else cubes_data

        print(f"Found {len(cubes) if isinstance(cubes, list) else 'unknown'} cubes")

        # Look for Ukraine-specific or monthly cubes
        ukraine_cubes = []
        monthly_cubes = []
        if isinstance(cubes, list):
            for cube in cubes:
                name = cube.get("name", "") if isinstance(cube, dict) else str(cube)
                if "ukr" in name.lower():
                    ukraine_cubes.append(name)
                if "_m_" in name.lower() or "month" in name.lower():
                    monthly_cubes.append(name)

            print(f"\nUkraine-specific cubes: {ukraine_cubes if ukraine_cubes else 'None found'}")
            print(f"Monthly cubes: {monthly_cubes if monthly_cubes else 'None found'}")

            # Print all cube names for reference
            print("\nAll cube names:")
            for cube in cubes:
                name = cube.get("name", "") if isinstance(cube, dict) else str(cube)
                print(f"  - {name}")
        else:
            print("Unexpected cubes format, dumping raw:")
            print(json.dumps(cubes_data, indent=2)[:3000])
except Exception as e:
    print(f"Error fetching cubes: {e}")

# Step 2: Try querying bilateral trade data for Ukraine 2025
# Try common cube names for sub-annual data
cube_candidates = [
    "trade_s_ukr_m_hs",
    "trade_s_ukr_port_m_hs",
    "trade_s_ukr_m_hs6",
    "trade_i_comtrade_m_hs",
    "trade_i_baci_a_92",
]

print("\n\nStep 2: Attempting to fetch Ukraine bilateral trade data for 2025...")

for cube_name in cube_candidates:
    params = {
        "cube": cube_name,
        "drilldowns": "Month,Exporter Country,Importer Country,HS4",
        "measures": "Trade Value",
        "Exporter Country": "euukr",
        "Year": "2025",
        "parents": "false",
        "sparse": "false",
    }

    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            if isinstance(data, dict) and "data" in data:
                records = data["data"]
            elif isinstance(data, list):
                records = data
            else:
                records = []

            if records:
                print(f"\nSUCCESS with cube '{cube_name}': {len(records)} records found")
                print(f"Sample record: {json.dumps(records[0], indent=2)}")

                # Write to CSV
                output_file = "/home/user/hello-world/ukraine_bilateral_trade_2025.csv"
                if records:
                    fieldnames = list(records[0].keys())
                    with open(output_file, "w", newline="") as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(records)
                    print(f"\nWrote {len(records)} records to {output_file}")
                break
            else:
                print(f"No data from cube '{cube_name}'")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} from cube '{cube_name}': {e.reason}")
    except Exception as e:
        print(f"Error with cube '{cube_name}': {e}")

# Step 3: If no specific Ukraine cube, try the general bilateral cube with Ukraine filter
print("\n\nStep 3: Trying alternative drilldown configurations...")

alt_queries = [
    {
        "cube": "trade_i_baci_a_92",
        "drilldowns": "Year,Exporter Country,Importer Country,HS4",
        "measures": "Trade Value",
        "Exporter Country": "euukr",
        "Year": "2025",
    },
    {
        "cube": "trade_i_baci_a_92",
        "drilldowns": "Year,Exporter Country,Importer Country,HS4",
        "measures": "Trade Value",
        "Importer Country": "euukr",
        "Year": "2025",
    },
    {
        "cube": "trade_i_comtrade_m_hs",
        "drilldowns": "Time,Reporter Country,Partner Country,HS4",
        "measures": "Trade Value",
        "Reporter Country": "euukr",
        "Time": "202501,202502,202503,202504,202505,202506,202507,202508,202509",
    },
]

for i, params in enumerate(alt_queries):
    params["parents"] = "false"
    params["sparse"] = "false"

    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            if isinstance(data, dict) and "data" in data:
                records = data["data"]
            elif isinstance(data, list):
                records = data
            else:
                records = []

            if records:
                print(f"\nSUCCESS with alt query {i+1}: {len(records)} records")
                print(f"Sample: {json.dumps(records[0], indent=2)}")

                output_file = f"/home/user/hello-world/ukraine_bilateral_trade_2025_alt{i+1}.csv"
                fieldnames = list(records[0].keys())
                with open(output_file, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(records)
                print(f"Wrote {len(records)} records to {output_file}")
            else:
                print(f"No data from alt query {i+1}")
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code} from alt query {i+1}: {e.reason} - {body[:500]}")
    except Exception as e:
        print(f"Error with alt query {i+1}: {e}")

print("\nDone.")

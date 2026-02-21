import re

with open('/Users/jeremy/devroot/P2C-Stack/P2CScripts/scripts/ETL/backfill_geocoding.py', 'r') as f:
    content = f.read()

# I want to find the while True: loop and indent everything under it properly.
# The simplest way is to manually replace the unindented portion.

# We will just rewrite the `geocode_and_update` function entirely.
new_func = """def geocode_and_update(table, id_col, address_col, time_col, target_ids=None):
    \"\"\"Reads rows with null lat/lon, geocodes, and updates them via API.\"\"\"
    api = shared_utils.APIClient()
    total_processed = 0
    chunks = [target_ids[i:i + 500] for i in range(0, len(target_ids), 500)] if target_ids else [None]

    for chunk in chunks:
        while True:
            candidates = []
            try:
                if target_ids:
                    candidates = api.post("tools/geocode/fetch-addresses", {"ids": [str(x) for x in chunk], "table": table})
                else:
                    candidates = api.get(f"tools/geocode/candidates?table={table}&count=50")
            except Exception as e:
                print(f"API Fetch Error: {e}")
                raise e
                
            if not candidates:
                break
                
            updates = []
            for row in candidates:
                record_id = row.get('id') or row.get('Id')
                raw_address = row.get('address') or row.get('Address')
                
                if not raw_address:
                    continue

                lat, lon = extract_coordinates(raw_address)
                
                if not lat:
                    address = clean_address(raw_address)
                    
                    if "PBX" in address or "UNKNOWN" in address:
                        print(f"Skipping known bad: {address}")
                        updates.append({"Id": str(record_id), "Lat": 0.0, "Lon": 0.0, "Table": table})
                        continue

                    def fetch_coords(query):
                        for attempt in range(2):
                            try:
                                r = requests.get(PROXY_GEOCODE_URL, params={'q': query}, timeout=3)
                                if r.status_code == 200:
                                    d = r.json()
                                    if d and 'lat' in d and 'lon' in d:
                                        return float(d['lat']), float(d['lon'])
                            except Exception:
                                time.sleep(0.1)
                            time.sleep(0.1)
                        return None, None

                    lat, lon = fetch_coords(address)

                    if (lat is None) and " & " in address:
                        parts = address.split(" & ")
                        city_suffix = ", DUBUQUE, IA"
                        if "," in parts[-1]:
                            city_suffix = parts[-1][parts[-1].find(","):]
                        valid_coords = []
                        for part in parts:
                            part = part.strip()
                            if not part: continue
                            query = part if "," in part else part + city_suffix
                            plat, plon = fetch_coords(query)
                            if plat: valid_coords.append((plat, plon))
                        if valid_coords:
                            lat = sum(c[0] for c in valid_coords) / len(valid_coords)
                            lon = sum(c[1] for c in valid_coords) / len(valid_coords)
                            print(f"  -> Resolved intersection: {lat}, {lon}")

                    if (lat is None) and address[0].isdigit():
                        parts = address.split(" ", 1)
                        if len(parts) > 1:
                            street_with_city = parts[1]
                            lat, lon = fetch_coords(street_with_city)
                    
                    if (lat is None):
                        bare_addr = address.split(',')[0].strip()
                        if bare_addr[0].isdigit() and " " in bare_addr:
                             bare_addr = bare_addr.split(" ", 1)[1]
                        lat, lon = fetch_coords(bare_addr)
                        if not lat and "NORTHWEST ARTERIAL" in address:
                             lat, lon = fetch_coords("NW ARTERIAL")

                    if (lat is None) and "DUBUQUE" in address:
                        county_addr = address.replace("DUBUQUE", "DUBUQUE COUNTY")
                        lat, lon = fetch_coords(county_addr)

                if lat is not None and lon is not None:
                    updates.append({"Id": str(record_id), "Lat": lat, "Lon": lon, "Table": table})
                    print(f"Geocoded {record_id}: {lat}, {lon}")
                else:
                    print(f"Failed Geocode {record_id} ({raw_address}) -> Cleaned: {address}")
                    updates.append({"Id": str(record_id), "Lat": 0.0, "Lon": 0.0, "Table": table})
                
                total_processed += 1
                time.sleep(0.05)
                
            if updates:
                try:
                    api.post("tools/geocode/update", updates)
                except Exception as e:
                    print(f"Update Batch Error: {e}")
                    raise e
            
            if target_ids:
               break
               
    print(f"Processed {total_processed} records.")
"""

# Replace in content using regex from def geocode_and_update to def main():
content = re.sub(r'def geocode_and_update.*?def main', new_func + '\n\ndef main', content, flags=re.DOTALL)

with open('/Users/jeremy/devroot/P2C-Stack/P2CScripts/scripts/ETL/backfill_geocoding.py', 'w') as f:
    f.write(content)

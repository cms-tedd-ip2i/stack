import json
import urllib.request
import os
import base64

# Configuration
GRAFANA_URL = "http://localhost:3001"
AUTH = "admin:daqtedd"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "dashboards")

def get_request(url):
    req = urllib.request.Request(url)
    # Preemptively set the Authorization header to handle Grafana API requests
    auth_bytes = base64.b64encode(AUTH.encode()).decode()
    req.add_header("Authorization", f"Basic {auth_bytes}")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def export_dashboards():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Search for all dashboards
    search_url = f"{GRAFANA_URL}/api/search?type=dash-db"
    dashboards = get_request(search_url)

    for dash in dashboards:
        uid = dash['uid']
        title = dash['title'].replace(' ', '_').lower()
        print(f"Exporting {dash['title']} ({uid})...")

        # 2. Get full dashboard JSON
        dash_url = f"{GRAFANA_URL}/api/dashboards/uid/{uid}"
        full_data = get_request(dash_url)
        
        # 3. Extract the actual dashboard object
        actual_dashboard = full_data['dashboard']
        
        # 4. Clean up for provisioning
        # Setting id to null allows Grafana to import it as a new object
        actual_dashboard['id'] = None
        
        # 5. Save to file
        file_path = os.path.join(OUTPUT_DIR, f"{title}.json")
        with open(file_path, 'w') as f:
            json.dump(actual_dashboard, f, indent=2)
        print(f" Saved to {file_path}")

if __name__ == "__main__":
    export_dashboards()

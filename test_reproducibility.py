import os
import glob
import pytest

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def test_nodered_flows_exist():
    """Verify Node-RED flows are exported."""
    flow_file = os.path.join(BASE_PATH, "node-red/data/flows.json")
    assert os.path.exists(flow_file), "Node-RED flows.json is missing."

def test_grafana_dashboards_exist():
    """Verify at least one Grafana dashboard is exported and provisioned."""
    dashboard_dir = os.path.join(BASE_PATH, "grafana/dashboards")
    provisioning_file = os.path.join(BASE_PATH, "grafana/provisioning/dashboards/dashboard.yaml")
    json_files = glob.glob(os.path.join(dashboard_dir, "*.json"))
    
    assert len(json_files) > 0, "No Grafana dashboard JSON files found."
    assert os.path.exists(provisioning_file), "Grafana provisioning file is missing."

def test_ph2_acf_xmls_exist():
    """Verify Ph2_ACF XML configurations are present."""
    settings_dir = os.path.join(BASE_PATH, "ph2_acf/settings")
    xml_files = glob.glob(os.path.join(settings_dir, "**/*.xml"), recursive=True)
    assert len(xml_files) > 0, "No Ph2_ACF XML configuration files found in settings/."

def test_influxdb_provisioning_exists():
    """Verify InfluxDB environment file exists."""
    env_file = os.path.join(BASE_PATH, "my.env")
    assert os.path.exists(env_file), "my.env file is missing for setup."

def test_simulators_exist():
    """Verify that development simulators exist for offline work."""
    assert os.path.exists(os.path.join(BASE_PATH, "dummy/caen_sim.py")), "CAEN simulator missing."
    assert os.path.exists(os.path.join(BASE_PATH, "dummy/ph2_acf_sim.py")), "Ph2_ACF simulator missing."
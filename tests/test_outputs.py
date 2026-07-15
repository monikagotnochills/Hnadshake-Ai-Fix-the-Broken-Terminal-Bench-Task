import json
from pathlib import Path
from collections import Counter

REPORTING_PATH = Path("/app/report.json")
LOGGING_PATH = Path("/app/access.log")


def compute_expected_values():
    total_requests = 0
    unique_ips = set()
    paths = Counter()

    assert LOGGING_PATH.exists(), "access.log not found"
    
    with LOGGING_PATH.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            total_requests += 1

            parts = line.split()

            ip = parts[0]
            unique_ips.add(ip)
            try:
                first_quote = line.index('"')
                second_quote = line.index('"', first_quote + 1)

                request = line[first_quote + 1 : second_quote]
                request_parts = request.split()
                if len(request_parts) >= 2:
                    path = request_parts[1]
                    paths[path] += 1

            except ValueError:
                
                continue

    top_path = paths.most_common(1)[0][0] if paths else None

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": top_path,
    }


def load_report():
    # To ensure report.json file exists before reading it
    assert REPORTING_PATH.exists(), "report.json not found"
   # Open the JSON report in read mode and parse its contents
    with REPORTING_PATH.open("r") as f:
        return json.load(f)

#Verify that the report.json file was generated
def test_report_exists():
    assert REPORTING_PATH.exists(), "report.json not found"

# This ensures the file contains some output instead of being blank
def test_report_nonempty():
    """report.json is not empty."""
    assert REPORTING_PATH.stat().st_size > 0, "report.json is empty"

# Verify that report.json contains valif JSON , If parsing Fails the test reports the parsing error 
def test_valid_json():
    try:
        load_report()
    except Exception as e:
        assert False, f"Invalid report.json: {e}"

# report.json contains all required fields
def test_required_fields():
    report = load_report()

    required_fields = {
        "total_requests",
        "unique_ips",
        "top_path",
    }
    assert isinstance(report["total_requests"], int)
    assert isinstance(report["unique_ips"], int)
    assert isinstance(report["top_path"], str)

    missing = required_fields - report.keys()
    
    assert not missing, f"Missing fields: {missing}"

#The total request count
def test_total_requests():
    report = load_report()
    expected = compute_expected_values()

    assert (
        report["total_requests"] == expected["total_requests"]
    ), (
        f"Expected total_requests={expected['total_requests']}, "
        f"got {report['total_requests']}"
    )

#vVerifying the unique IP count
def test_unique_ips():
    report = load_report()
    expected = compute_expected_values()

    assert (
        report["unique_ips"] == expected["unique_ips"]
    ), (
        f"Expected unique_ips={expected['unique_ips']}, "
        f"got {report['unique_ips']}"
    )

#Verifinng the  most requested endpoint
def test_top_path():
    report = load_report()
    expected = compute_expected_values()
    assert (
        report["top_path"] == expected["top_path"]
    ), (
        f"Expected top_path='{expected['top_path']}', "
        f"got '{report['top_path']}'"
    )
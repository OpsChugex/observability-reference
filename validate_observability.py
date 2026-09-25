import json
from pathlib import Path

import yaml

policy = json.loads(Path("slo-policy.json").read_text(encoding="utf-8"))
rules = yaml.safe_load(Path("prometheus-rules.yml").read_text(encoding="utf-8"))

assert policy["evidence_id"] == "OCX-OBS-001"
assert 99 < policy["availability_target_percent"] < 100
assert policy["window_days"] == 30
assert policy["latency_p95_target_ms"] > 0
expected_error_rate = 100 - policy["availability_target_percent"]
assert abs(policy["error_rate_target_percent"] - expected_error_rate) < 0.000001

fast = policy["burn_rate_alerts"]["fast"]
slow = policy["burn_rate_alerts"]["slow"]
assert fast["burn_rate"] > slow["burn_rate"] > 1
assert fast["window"] == "5m"
assert slow["window"] == "1h"

rule_names = set()
alert_names = set()
for group in rules["groups"]:
    for item in group["rules"]:
        if "record" in item:
            rule_names.add(item["record"])
        if "alert" in item:
            alert_names.add(item["alert"])

assert "ocx:http_request_success_ratio:5m" in rule_names
assert "ocx:http_request_success_ratio:1h" in rule_names
assert "ocx:http_request_latency_p95_seconds:5m" in rule_names
assert "HighErrorBudgetBurnFast" in alert_names
assert "HighErrorBudgetBurnSlow" in alert_names
assert "HighLatencyP95" in alert_names

minutes = policy["window_days"] * 24 * 60
allowed_downtime = minutes * (1 - policy["availability_target_percent"] / 100)

print("OBSERVABILITY_REFERENCE=PASS")
print(f"SLO_WINDOW_DAYS={policy['window_days']}")
print(f"AVAILABILITY_TARGET_PERCENT={policy['availability_target_percent']}")
print(f"ALLOWED_DOWNTIME_MINUTES={allowed_downtime:.2f}")
print(f"LATENCY_P95_TARGET_MS={policy['latency_p95_target_ms']}")

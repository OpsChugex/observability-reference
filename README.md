# OCX-OBS-001: Observability Reference

[![Validate observability reference](https://github.com/OpsChugex/observability-reference/actions/workflows/validate.yml/badge.svg)](https://github.com/OpsChugex/observability-reference/actions/workflows/validate.yml)

**Classification:** Demonstration design with executable validation

This repository defines a reviewable observability contract for a reference API.

## Reference signals

- availability / request success ratio
- P95 request latency
- error-budget burn
- alert severity and timing
- 30-day SLO window

The policy defines a 99.9% availability target over 30 days and a 300 ms P95 latency target. The validator calculates the corresponding 30-day availability budget and verifies that the Prometheus recording and alert rules match the documented contract.

## Files

- `slo-policy.json` contains the machine-readable SLO policy.
- `prometheus-rules.yml` contains reference recording and alert rules.
- `validate_observability.py` checks the SLO and rule contract.
- `.github/workflows/validate.yml` repeats the validation in GitHub Actions.

## Run locally

```bash
python -m pip install PyYAML==6.0.3
python validate_observability.py
```

## Evidence interpretation

A passing workflow proves that the reference SLO policy and alert rules are internally consistent for that commit.

This repository does not claim that these rules are attached to a customer system, that the displayed targets are customer SLAs, or that production availability has been measured.

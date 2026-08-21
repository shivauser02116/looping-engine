# Hardware Tamper Case Study

## Scenario

An Internet of Things water quality station reports normal readings while the field unit has been physically moved, power-cycled, or exposed to probe tampering.

## Risk

Bad field data can look valid if the software only checks whether sensor values are inside normal chemical ranges. A useful loop must also evaluate metadata and operational signals.

## Signals to Check

- Sudden sensor flatlines after a reboot.
- Repeated values with impossible precision.
- Battery voltage drops followed by clean-looking readings.
- Location drift from the assigned installation zone.
- Missing calibration events after probe replacement.
- Turbidity, pH, and total dissolved solids changing in physically inconsistent ways.

## Looping Engine Evaluation

1. Run the data quality command against the latest device payload.
2. Check for expected exit code, warning text, and generated anomaly report files.
3. If the check fails, apply one targeted fix to parsing, thresholds, or metadata handling.
4. Rerun until the tamper case is detected or the maximum attempt limit is reached.

## Pass Criteria

- The tamper condition is flagged.
- The report names the violated signal.
- Normal-range chemical readings alone are not enough to pass the case.
- Remaining assumptions are written down before deployment.

## Deployment Note

This case study is not a replacement for field testing. It is a software-side guardrail for projects such as water quality monitoring systems where physical device behavior can invalidate clean-looking data.

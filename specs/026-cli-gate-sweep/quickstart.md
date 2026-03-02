# Quickstart: CLI Gate Sweep Verification

## Scenario 1: CLI Listing Without Routes

```bash
# Method listing should show names and params only, no route paths
ab payments

# Expected: clean listing like:
#   payments — N methods
#
#   API Methods:
#   ──────────────────────────────────────────
#   get                            job_display_id -> PaymentInfo
#   get_sources                    job_display_id -> PaymentSources
```

## Scenario 2: Route Visible in Help

```bash
# Individual method help SHOULD show the route
ab payments get --help

# Expected: includes "Route   GET /job/{jobDisplayId}/payment"
```

## Scenario 3: Tracking Example Auto-Resolves Constants

```bash
# Should run without passing any arguments — uses TEST_JOB_DISPLAY_ID
ex jobs get_tracking

# Expected: 200 response, fixture captured to TrackingInfo.json
```

## Scenario 4: Tracking V3 with historyAmount

```bash
# Should use TEST_HISTORY_AMOUNT (3) automatically
ex jobs get_tracking_v3

# Expected: 200 response, fixture captured to TrackingInfoV3.json
```

## Scenario 5: Chain Discovery for RFQ

```bash
# rfqId not in constants — should list RFQs for TEST_JOB_DISPLAY_ID first
ex jobs get_rfq

# Expected: discovers rfqId from listing, then calls GET /rfq/{rfqId}
```

## Scenario 6: Progress Report Improvement

```bash
python scripts/generate_progress.py

# Expected: gate pass counts increase from baseline
# Baseline: G1=2, G2=2, G3=6, G5=216
# Target: measurable improvement in G1, G2, G3
```

## Scenario 7: Constants Follow Naming Convention

```bash
# All constants should follow TEST_SCREAMING_SNAKE pattern
python -c "
from tests.constants import *
import tests.constants as c
for name in sorted(dir(c)):
    if name.startswith('TEST_'):
        print(f'{name} = {getattr(c, name)!r}')
"

# Expected: all constants are TEST_ prefixed, values are sensible staging defaults
```

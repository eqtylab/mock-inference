# Simple EQTY SDK sample

The [Python script](eqty_responses_sample.py) records seven example items:

1. CPU workloads from `responseapi/` (mock API, safety service, and configuration).
2. Model files from `mock-model/`, with EQTY model signing enabled.
3. Prompt text.
4. Inference output text.
5. Mock Azure regions for CPU workloads and inference.
6. Mock session metadata.
7. Mock guardrail results.

EQTY handles all content hashing. There are no manually calculated SHA hashes.
The workload and model directories are each registered as one asset.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python eqty_responses_sample.py
```

Output: `mock-session.manifest.json`. Local keys and SDK storage are kept in
`.eqty-sample/`. Python 3.10+ and EQTY SDK 2.5.0 are required.

Every asset explicitly sets the SDK's blob-storage option, named `_store`:

- `_store=True` for prompt, inference output, regions, session, and guardrail results.
- `_store=False` for `responseapi/` and `mock-model/`; their contents remain in
  those directories, with content-addressed references recorded in the manifest.

Directory indexes, asset metadata, and signatures are still retained. `_store=False`
does not erase any content already present in an existing SDK store.

Model signing is enabled with `_enable_model_signing_signature=True` on
`Model.from_path(...)`. The SDK creates Model Signing evidence using the active
P-256 (`SECP256R1`) signer. The separate `mock-sample-p256` key name avoids reusing
an older demo key with an incompatible algorithm. This signs the mock model
locally; it does not verify an external publisher's signature.

All workload/model files and session data are mock examples. The weight shards
are placeholders, not a loadable model. The script makes no API calls and executes
no guardrails. Equal mock region values do not establish real colocation.

Checked with EQTY SDK 2.5.0. Successful export alone does not establish independent
signature verifiability.

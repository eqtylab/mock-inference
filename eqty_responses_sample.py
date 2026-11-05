"""Simple EQTY example: seven mock objects, one signed lineage manifest.

All service, model, region, and guardrail evidence below is simulated.
No Azure requests are performed. EQTY model signing is enabled for mock files.
"""
from pathlib import Path

import eqty_sdk as sdk


# 1. CPU workloads: EQTY hashes the mock API and safety service directory.
mock_cpu_directory = Path(__file__).resolve().parent / "responseapi"

# 2. Model identity: hash the entire mock model directory as one asset.
# EQTY generates the model signature using the active local signer below.
mock_model_directory = Path(__file__).resolve().parent / "mock-model"
mock_model_identity = {
    "name": "mock-model",
    "version": "1.0",
}

# 3. Prompt: EQTY handles hashing when the asset is registered.
mock_prompt = {
    "text": "What is the capital of France?",
}

# 4. Inference output: EQTY handles hashing when the asset is registered.
mock_inference = {
    "text": "The capital of France is Paris.",
}

# 5. Azure regions: separate fields even when the mock values are equal.
mock_azure_regions = {
    "responses_api_cpu": "eastus2",
    "safety_service_cpu": "eastus2",
    "inference_server": "eastus2",
    "evidence": "mock values; actual colocation is not established",
}

# 6. Additional session metadata.
mock_session = {
    "session_id": "mock-session-001",
    "request_id": "mock-request-001",
    "timestamp": "2026-11-06T00:00:00Z",
    "input_tokens": 8,
    "output_tokens": 7,
    "latency_ms": 120,
    "evidence_type": "simulated example",
}

# 7. Guardrails and results: illustrative records, not actual safety checks.
mock_guardrails = {
    "input": [{"name": "prompt_safety", "version": "mock-1", "result": "pass"}],
    "output": [{"name": "response_safety", "version": "mock-1", "result": "pass"}],
    "execution_status": "simulated; no guardrails were executed",
}


def main():
    # Initialize EQTY.
    context = sdk.Context.new("Mock Responses API session")
    config = sdk.init(default_context=context, custom_dir=Path(".eqty-sample"))
    config.set_store_all_blobs(False)

    # Select a local signing key. Model signing requires a P-256 key.
    signer = sdk.Signer.load_or_create(
        name="mock-sample-p256", algorithm=sdk.SIGNER_ALGORITHMS.SECP256R1,
    )
    sdk.set_active_signer(signer)

    # Register each mock object. EQTY hashes the objects and signs the records.
    # The SDK names its store_blob option `_store`.
    cpu = sdk.Code.from_path(
        mock_cpu_directory, name="Mock responseapi CPU workload", _store=False,
        storage="by-reference", storage_reason="workload files kept in responseapi/",
    )
    model = sdk.Model.from_path(
        mock_model_directory, **mock_model_identity, _store=False,
        _enable_model_signing_signature=True,
        storage="by-reference", storage_reason="model files kept in mock-model/",
    )
    prompt = sdk.Prompt.from_object(mock_prompt, name="Mock prompt", _store=True)
    inference = sdk.Document.from_object(mock_inference, name="Mock inference output", _store=True)
    regions = sdk.Configuration.from_object(mock_azure_regions, name="Mock Azure regions", _store=True)
    session = sdk.Configuration.from_object(mock_session, name="Mock session metadata", _store=True)
    guardrails = sdk.Guardrail.from_object(mock_guardrails, name="Mock guardrail results", _store=True)

    # Connect the inputs and output in the lineage graph.
    # This declares a simulated relationship; it does not execute inference.
    run = sdk.Computation.new(name="Mock inference", evidence_type="simulated")
    for asset in [cpu, model, prompt, regions, session]:
        run.add_input_cid(asset.cid)
    for asset in [inference, guardrails]:
        run.add_output_cid(asset.cid)
    run.finalize()

    context.export(Path("mock-session.manifest.json"))
    print(f"Mock model directory CID: {model.cid}")
    print("Wrote mock-session.manifest.json")


if __name__ == "__main__":
    main()

from vpn_leaks.models import NormalizedRun


def test_normalized_json_roundtrip():
    n = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
    )
    s = n.model_dump_json()
    assert "example" in s
    assert n.schema_version == "1.4"

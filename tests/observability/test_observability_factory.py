from app.observability.factory import build_telemetry_sink
from app.observability.sink import TelemetrySink


def test_build_telemetry_sink_returns_telemetry_sink():
    sink = build_telemetry_sink()

    assert isinstance(sink, TelemetrySink)

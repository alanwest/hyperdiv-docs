from importlib.metadata import version
import hyperdiv as hd
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from .router import router
from .menu import menu
from .app_template_demo import main as demo_main

resource = Resource(attributes={
    SERVICE_NAME: "HyperdivDocs"
})

# metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter()
    # OTLPMetricExporter(endpoint="<traces-endpoint>/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

metrics.set_meter_provider(meter_provider)

def render_title(slot=None):
    with hd.hbox(gap=0.5, font_size=1, align="center", slot=slot):
        hd.text("Hyperdiv", font_weight="bold")
        hd.text("Docs")
        hd.badge(
            f'v{version("hyperdiv")}',
            background_color="neutral-200",
            font_color="neutral-700",
            font_size=0.7,
        )


def main():
    loc = hd.location()
    if loc.path.startswith("/app-template-demo"):
        demo_main()
        return

    t = hd.theme()
    app = hd.template(
        logo=f'/assets/hd-logo-{"black" if t.is_light else "white"}.svg',
    )
    app.add_sidebar_menu(menu)
    with app.app_title:
        render_title()
    with app.drawer_title:
        render_title()
    app.body.padding = 0
    with app.body:
        router.run()

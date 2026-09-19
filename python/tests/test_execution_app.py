import importlib

import httpx
import pytest

from vidap_execution.app import create_app


@pytest.mark.unit
def test_foundation_ownership_packages_are_importable() -> None:
    package_names = (
        "vidap_execution",
        "vidap_experiments",
        "vidap_export",
        "vidap_workflow",
    )

    imported_packages = {
        importlib.import_module(name).__name__ for name in package_names
    }

    assert imported_packages == set(package_names)


@pytest.mark.integration
@pytest.mark.anyio
async def test_unrouted_app_returns_framework_unknown_route_response() -> None:
    transport = httpx.ASGITransport(app=create_app())

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/not-a-product-route")

    assert response.status_code == 404

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


@pytest.mark.integration
@pytest.mark.anyio
async def test_foundation_status_is_the_static_phase_zero_response() -> None:
    transport = httpx.ASGITransport(app=create_app())

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/api/status")

    assert response.status_code == 200
    assert response.json() == {
        "application": "ViDAP",
        "scope": "phase-0-foundation",
        "status": "ready",
    }


@pytest.mark.integration
@pytest.mark.anyio
async def test_automatic_api_documentation_endpoints_remain_disabled() -> None:
    transport = httpx.ASGITransport(app=create_app())

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/docs")

    assert response.status_code == 404

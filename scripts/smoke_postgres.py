"""Read/write smoke test against the configured PostgreSQL database."""

from __future__ import annotations

import asyncio
from uuid import uuid4

from httpx import ASGITransport, AsyncClient

from app.main import app


async def main() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        collections = (
            "product-groups",
            "preparation-methods",
            "ingredients",
            "suppliers",
            "authors",
            "products",
            "recipes",
            "invoices",
        )
        responses = {}
        for collection in collections:
            response = await client.get(f"/api/v1/{collection}/")
            response.raise_for_status()
            responses[collection] = response.json()

        groups = responses["product-groups"]
        if not groups:
            raise RuntimeError("Seed data is missing: no product groups")
        suppliers = responses["suppliers"]
        if not suppliers:
            raise RuntimeError("Seed data is missing: no suppliers")
        if responses["recipes"]:
            assert responses["recipes"][0]["author"] is not None
        if responses["invoices"]:
            assert responses["invoices"][0]["supplier"] is not None
            if responses["invoices"][0]["items"]:
                assert responses["invoices"][0]["items"][0]["ingredient"] is not None

        marker = uuid4().hex
        created = await client.post(
            "/api/v1/products/",
            json={"name": f"smoke-{marker}", "group_id": groups[0]["id"]},
        )
        created.raise_for_status()
        product_id = created.json()["id"]

        product_list = await client.get("/api/v1/products/")
        product_list.raise_for_status()
        listed_product = next(
            item for item in product_list.json() if item["id"] == product_id
        )
        assert listed_product["group"]["id"] == groups[0]["id"]

        fetched = await client.get(f"/api/v1/products/{product_id}")
        fetched.raise_for_status()
        assert fetched.json()["name"] == f"smoke-{marker}"

        updated = await client.put(
            f"/api/v1/products/{product_id}",
            json={"name": f"smoke-updated-{marker}"},
        )
        updated.raise_for_status()
        assert updated.json()["name"] == f"smoke-updated-{marker}"

        deleted = await client.delete(f"/api/v1/products/{product_id}")
        deleted.raise_for_status()

        report_urls = [
            "/api/v1/reports/min-calorie-products",
            "/api/v1/reports/products-with-recipes",
        ]
        supplier = next(
            (item for item in suppliers if item["code"] == "SUP-001"), suppliers[0]
        )
        report_urls.append(
            "/api/v1/reports/supplier-price-list"
            f"?supplier_id={supplier['id']}&price_date=2026-01-15"
        )
        for url in report_urls:
            response = await client.get(url)
            response.raise_for_status()

    print("PostgreSQL API smoke test passed")


if __name__ == "__main__":
    asyncio.run(main())

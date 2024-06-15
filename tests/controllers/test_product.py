import pytest
from tests.schemas.factories import product_data
from fastapi import status
from fastapi_pagination import LimitOffsetPage



async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()

    del content["id"]
    del content["create_at"]
    del content["update_at"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8.500", "status": True}


async def test_controller_get_should_return_success(client, products_url, product_inserted):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["create_at"]
    del content["update_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {"id": str(product_inserted.id), "name": "Iphone 14 Pro Max", "quantity": 10, "price": "8.500", "status": True}


async def test_controller_get_should_not_found(client, products_url):
    response = await client.get(f"{products_url}1e4f214e-85f7-461a-89d0-a751a32e3bb9")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detai": "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"}


@pytest.mark.usefixtures("products_inserted")
async def test_controller_get_all_should_return_success(client, products_url):
    response = await client.get_all(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), LimitOffsetPage)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(client, products_url, product_inserted):
    response = await client.patch(f"{products_url}{product_inserted.id}", json={"price": "6.666"})

    content = response.json()

    del content["create_at"]
    del content["update_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {"id": str(product_inserted.id), "name": "Iphone 14 Pro Max", "quantity": 10, "price": "6.666", "status": True}


async def test_controller_delete_should_return_no_content(client, products_url, product_inserted):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_not_found(client, products_url):
    response = await client.delete(f"{products_url}1e4f214e-85f7-461a-89d0-a751a32e3bb9")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detai": "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"}

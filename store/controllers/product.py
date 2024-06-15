from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdateIn
from store.usecases.product import ProductUsecase
from fastapi_pagination import LimitOffsetPage, paginate


router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def get_all(usecase: ProductUsecase = Depends()) -> LimitOffsetPage[ProductOut]:
    return paginate(await usecase.get_all())


@router.patch(path="/", status_code=status.HTTP_200_OK)
async def post(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdateIn = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

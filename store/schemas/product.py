from decimal import Decimal
from typing import Annotated
from bson import Decimal128
from pydantic import AfterValidator, BaseModel, Field
from store.schemas.base import BaseSchemaMixin, OutSchema


class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutSchema):
    ...


def convert_decimal_128(value):
    return Decimal128(str(value))


DECIMAL = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdateIn(BaseSchemaMixin):
    quantity: int | None = Field(None, description="Product quantity")
    price: DECIMAL | None = Field(None, description="Product price")
    status: bool | None = Field(None, description="Product status")


class ProductUpdateOut(ProductOut):
    ...

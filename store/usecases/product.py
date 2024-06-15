from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product_model import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdateIn, ProductUpdateOut
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient = db_client.get()
        self._database: AsyncIOMotorDatabase = self._client.get_database()
        self._collection = self._database.get_collection("products")
    
    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self._collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())
    
    async def get(self, id: UUID) -> ProductOut:
        result = await self._collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)
    
    async def get_all(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self._collection.find()]
    
    async def update(self, id: UUID, body: ProductUpdateIn) -> ProductUpdateOut:
        result = await self._collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self._collection.find_one({"id": id})

        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        
        result = await self._collection.delete_one({"id": id})
        
        return True if result.deleted_count > 0 else False

product_usecase = ProductUsecase()

from inventory_system.constants import ProductCategory
from inventory_system.models.product import ClothingProduct, ElectronicsProduct, FoodProduct, Product


class ProductFactory:
    def create_product(self, sku: str, name: str, price: float, qty: int, product_category: ProductCategory, threshold: int) -> Product:
        
        if product_category == ProductCategory.ELECTRONICS:
            return ElectronicsProduct(sku, name, price, qty, threshold, 0)
        elif product_category == ProductCategory.CLOTHING:
            return ClothingProduct(sku, name, price, qty, threshold, "")
        elif product_category == ProductCategory.FOOD:
            return FoodProduct(sku, name, price, qty, threshold, "")
        else:
            raise ValueError("Invalid product type")
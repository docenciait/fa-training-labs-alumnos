# Concepto: Modelo de Producto con Validaciones
from pydantic import BaseModel, Field, HttpUrl, ValidationError, FtpUrl
from typing import List, Optional

class Product(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50,
        description="Nombre del producto", examples=["Mi Super Producto"]
    )
    price: float = Field(..., gt=0, description="Precio > 0")
    tags: List[str] = Field(default=[], description="Etiquetas")
    image_url: Optional[HttpUrl] = Field(default=None, description="URL válida")
    
# 1. Ejemplo de producto válido

valid_product_data = {
    "name": "Teclado Mecánico RGB",
    "price": 79.99,
    "tags": ["gaming", "periférico", "rgb"],
    "image_url": "https://example.com/images/teclado.jpg"
}

# try:
#     product1 = Product(**valid_product_data)
#     print("Producto 1 válido:")
#     print(product1.model_dump_json(indent=2))
# except ValidationError as e:
#     print("Error en Producto 1:")
#     print(e.errors())
    
# 2. Ejemplo de producto válido (campos opcionales omitidos)

# valid_product_data_minimal = {
#     "name": "Ratón Óptico",
#     "price": 25.50
# }

# try:
#     product2 = Product(**valid_product_data_minimal)
#     print("\n Producto 2 válido (mínimo):")
#     print(product2.model_dump_json(indent=2))
#     # product2.tags será []
#     # product2.image_url será None
# except ValidationError as e:
#     print("\n Error en Producto 2:")
#     print(e.errors())

# 3. Ejemplo de producto con datos inválidos

invalid_product_data = {
    "name": "X",  # Demasiado corto
    "price": -10, # No es mayor que 0
    "tags": ["tech", 123], # 123 no es un string
    "image_url": "esto-no-es-una-url"
}

# print("\nIntentando crear Producto 3 con datos inválidos:")

# try:
#     product3 = Product(**invalid_product_data)
#     print(product3.model_dump_json(indent=2))
# except ValidationError as e:
#     print("Error de validación en Producto 3:")
#     # Pydantic agrupa todos los errores de validación
#     for error in e.errors():
#         print(error) #print(f"  - Campo: {error['loc'][0]}, Mensaje: {error['msg']}")

#4. Ejemplo con URL inválida pero el resto bien

invalid_url_data = {
    "name": "Monitor Curvo",
    "price": 299.00,
    "image_url": "ftp://example.com/image.png" # HttpUrl espera http o https
}

print("\nIntentando crear Producto 4 con URL inválida:")

try:
    product4 = Product(**invalid_url_data)
    print(product4.model_dump_json(indent=2))
except ValidationError as e:
    print("Error de validación en Producto 4:")
    for error in e.errors():
        print(f"  - Campo: {error['loc'][0]}, Mensaje: {error['msg']}")
"""
Simple product database for barcode-to-name lookup.
In a real production environment, this could be an API call or a database query.
"""

PRODUCT_DB = {
    "12345678": "Libreta Profesional",
    "87654321": "Crema de Manos Hidratante",
    "4005900114008": "Nivea Soft Cream",
    "7501055301323": "Coca Cola 600ml",
    "7501030400034": "Papas Sabritas Original",
    "8426307429887": "Libreta Azul",
    "8411047104118": "Crema de manos",
    "8431775035614": "Caja de camara",
    "3574660085587": "lapiz labial",
    "UNKNOWN": "Producto no asignado"
}

def get_product_name(barcode: str) -> str:
    """Returns the product name associated with the barcode."""
    return PRODUCT_DB.get(barcode, "Producto no asignado")

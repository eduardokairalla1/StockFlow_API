"""
Product controllers module.

Defines CRUD controller functions for product resources, handling HTTP requests,
validating input, invoking service layer operations, and formatting responses.
"""

from flask import request, jsonify
from marshmallow import ValidationError
from app.schemas.product_schema import ProductSchema
from app.utils.formatters import format_product, format_product_list
from app.services.product_service import (
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product
)


def create_product_controller(data):
    """
    Handle HTTP request to create a new product.

    Args:
        data (dict): Payload containing product attributes to be created.

    Returns:
        Response: JSON-formatted created product with HTTP 201 on success,
                  or validation/error messages on failure.
    """
    try:
        # Validate and deserialize input data using ProductSchema
        data = ProductSchema().load(data)

        # Create product via service layer
        product = create_product(data)

        # Format the created product and return with 201 status
        return jsonify(format_product(product)), 201

    except ValidationError as ve:
        # Return detailed validation errors with 400 status
        return jsonify({"errors": ve.messages}), 400

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": str(e)}), 500
    

def list_products_controller():
    """
    Handle HTTP request to list products with optional filtering.

    Returns:
        Response: JSON-formatted list of products with HTTP 200 on success,
                  or error message with HTTP 500 on failure.
    """
    try:
        # Extract optional query parameters for filtering
        name = request.args.get("name")
        code = request.args.get("code")

        # Retrieve filtered or all products via service layer
        products = get_all_products(name=name, code=code)

        # Format product list and return with 200 status
        return jsonify(format_product_list(products)), 200

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": str(e)}), 500
    

def get_product_controller(id):
    """
    Handle HTTP request to retrieve a single product by ID.

    Args:
        id (int): Identifier of the product to retrieve.

    Returns:
        Response: JSON-formatted product with HTTP 200 if found,
                  or error message with HTTP 404/500.
    """
    try:
        # Fetch product by ID via service layer
        product = get_product_by_id(id)

        # If no product found, return 404 not found
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Format and return the found product with 200 status
        return jsonify(format_product(product)), 200

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": str(e)}), 500


def update_product_controller(id):
    """
    Handle HTTP request to update an existing product partially or fully.

    Args:
        id (int): Identifier of the product to update.

    Returns:
        Response: JSON-formatted updated product with HTTP 200 if successful,
                  or error messages with HTTP 400/404/500.
    """
    try:
        # Allow partial updates by setting partial=True on schema
        schema = ProductSchema(partial=True)
        # Validate and deserialize JSON body of request
        data = schema.load(request.json)

        # Update product via service layer
        product = update_product(id, data)

        # If product does not exist, return 404 not found
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Format and return the updated product with 200 status
        return jsonify(format_product(product)), 200

    except ValidationError as ve:
        # Validation errors return 400 status
        return jsonify({"errors": ve.messages}), 400

    except ValueError as ve:
        # Service layer may raise ValueError for domain errors
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": str(e)}), 500


def delete_product_controller(id):
    """
    Handle HTTP request to delete a product by ID.

    Args:
        id (int): Identifier of the product to delete.

    Returns:
        Response: JSON message with HTTP 200 on success,
                  or error message with HTTP 404/500.
    """
    try:
        # Delete the product via service layer
        delete_product(id)
        # Return success message with 200 status
        return jsonify({"message": f"Product {id} successfully deleted."}), 200

    except ValueError as ve:
        # Service layer raises ValueError if product not found
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": str(e)}), 500

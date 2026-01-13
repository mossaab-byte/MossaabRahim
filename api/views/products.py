from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_products(request):
    """List all products or create a new product"""
    if request.method == 'GET':
        query = """
        MATCH (p:Product)
        OPTIONAL MATCH (p)-[:PART_OF]->(c:Category)
        OPTIONAL MATCH (s:Supplier)-[:SUPPLIES]->(p)
        RETURN p.productID AS id, 
               p.productName AS name,
               p.unitPrice AS unitPrice,
               p.unitsInStock AS unitsInStock,
               p.unitsOnOrder AS unitsOnOrder,
               p.discontinued AS discontinued,
               c.categoryName AS category,
               s.companyName AS supplier
        ORDER BY p.productName
        LIMIT 100
        """
        data = Neo4jService.run(query)
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('productName'):
            return Response(
                {"error": "productName is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get next product ID
        id_query = "MATCH (p:Product) RETURN max(p.productID) AS maxId"
        max_id_result = Neo4jService.run(id_query)
        next_id = (max_id_result[0]['maxId'] or 0) + 1
        
        query = """
        CREATE (p:Product {
            productID: $productID,
            productName: $productName,
            unitPrice: $unitPrice,
            unitsInStock: $unitsInStock,
            unitsOnOrder: $unitsOnOrder,
            quantityPerUnit: $quantityPerUnit,
            discontinued: $discontinued,
            reorderLevel: $reorderLevel
        })
        RETURN p.productID AS id, p.productName AS name
        """
        result = Neo4jService.run(query, {
            "productID": next_id,
            "productName": data.get('productName'),
            "unitPrice": float(data.get('unitPrice', 0)),
            "unitsInStock": int(data.get('unitsInStock', 0)),
            "unitsOnOrder": int(data.get('unitsOnOrder', 0)),
            "quantityPerUnit": data.get('quantityPerUnit', ''),
            "discontinued": data.get('discontinued', False),
            "reorderLevel": int(data.get('reorderLevel', 0))
        })
        
        # Link to category if provided
        if data.get('categoryId'):
            cat_query = """
            MATCH (p:Product {productID: $productID})
            MATCH (c:Category {categoryID: $categoryID})
            CREATE (p)-[:PART_OF]->(c)
            """
            Neo4jService.run(cat_query, {
                "productID": next_id,
                "categoryID": int(data.get('categoryId'))
            })
        
        # Link to supplier if provided
        if data.get('supplierId'):
            sup_query = """
            MATCH (p:Product {productID: $productID})
            MATCH (s:Supplier {supplierID: $supplierID})
            CREATE (s)-[:SUPPLIES]->(p)
            """
            Neo4jService.run(sup_query, {
                "productID": next_id,
                "supplierID": int(data.get('supplierId'))
            })
        
        return Response(result[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_product(request, product_id):
    """Get, update or delete a product"""
    if request.method == 'GET':
        query = """
        MATCH (p:Product {productID: $id})
        OPTIONAL MATCH (p)-[:PART_OF]->(c:Category)
        OPTIONAL MATCH (s:Supplier)-[:SUPPLIES]->(p)
        RETURN p.productID AS id,
               p.productName AS name,
               p.unitPrice AS unitPrice,
               p.unitsInStock AS unitsInStock,
               p.unitsOnOrder AS unitsOnOrder,
               p.quantityPerUnit AS quantityPerUnit,
               p.discontinued AS discontinued,
               c.categoryName AS category,
               c.categoryID AS categoryId,
               s.companyName AS supplier,
               s.supplierID AS supplierId
        """
        data = Neo4jService.run(query, {"id": int(product_id)})
        if not data:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (p:Product {productID: $id})
        SET p.productName = $productName,
            p.unitPrice = $unitPrice,
            p.unitsInStock = $unitsInStock,
            p.unitsOnOrder = $unitsOnOrder,
            p.quantityPerUnit = $quantityPerUnit,
            p.discontinued = $discontinued,
            p.reorderLevel = $reorderLevel
        RETURN p.productID AS id, p.productName AS name
        """
        result = Neo4jService.run(query, {
            "id": int(product_id),
            "productName": data.get('productName', ''),
            "unitPrice": float(data.get('unitPrice', 0)),
            "unitsInStock": int(data.get('unitsInStock', 0)),
            "unitsOnOrder": int(data.get('unitsOnOrder', 0)),
            "quantityPerUnit": data.get('quantityPerUnit', ''),
            "discontinued": data.get('discontinued', False),
            "reorderLevel": int(data.get('reorderLevel', 0))
        })
        if not result:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update category relationship if provided
        if data.get('categoryId'):
            Neo4jService.run(
                "MATCH (p:Product {productID: $id})-[r:PART_OF]->() DELETE r",
                {"id": int(product_id)}
            )
            Neo4jService.run("""
                MATCH (p:Product {productID: $productID})
                MATCH (c:Category {categoryID: $categoryID})
                CREATE (p)-[:PART_OF]->(c)
            """, {"productID": int(product_id), "categoryID": int(data.get('categoryId'))})
        
        # Update supplier relationship if provided
        if data.get('supplierId'):
            Neo4jService.run(
                "MATCH ()-[r:SUPPLIES]->(p:Product {productID: $id}) DELETE r",
                {"id": int(product_id)}
            )
            Neo4jService.run("""
                MATCH (p:Product {productID: $productID})
                MATCH (s:Supplier {supplierID: $supplierID})
                CREATE (s)-[:SUPPLIES]->(p)
            """, {"productID": int(product_id), "supplierID": int(data.get('supplierId'))})
        
        return Response(result[0])
    
    elif request.method == 'DELETE':
        check_query = "MATCH (p:Product {productID: $id}) RETURN p"
        exists = Neo4jService.run(check_query, {"id": int(product_id)})
        if not exists:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        query = """
        MATCH (p:Product {productID: $id})
        DETACH DELETE p
        """
        Neo4jService.run(query, {"id": int(product_id)})
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_orders(request, product_id):
    """Get all orders containing this product"""
    query = """
    MATCH (o:Order)-[:ORDERS]->(p:Product {productID: $id})
    MATCH (c:Customer)-[:PURCHASED]->(o)
    RETURN o.orderID AS orderId,
           o.orderDate AS orderDate,
           c.companyName AS customer,
           c.customerID AS customerId
    ORDER BY o.orderDate DESC
    LIMIT 50
    """
    data = Neo4jService.run(query, {"id": int(product_id)})
    return Response(data)


@api_view(['GET'])
def products_by_category(request, category_id):
    """Get all products in a category"""
    query = """
    MATCH (p:Product)-[:PART_OF]->(c:Category {categoryID: $id})
    RETURN p.productID AS id,
           p.productName AS name,
           p.unitPrice AS unitPrice,
           p.unitsInStock AS unitsInStock
    ORDER BY p.productName
    """
    data = Neo4jService.run(query, {"id": int(category_id)})
    return Response(data)


@api_view(['GET'])
def products_by_supplier(request, supplier_id):
    """Get all products from a supplier"""
    query = """
    MATCH (s:Supplier {supplierID: $id})-[:SUPPLIES]->(p:Product)
    OPTIONAL MATCH (p)-[:PART_OF]->(c:Category)
    RETURN p.productID AS id,
           p.productName AS name,
           p.unitPrice AS unitPrice,
           p.unitsInStock AS unitsInStock,
           c.categoryName AS category
    ORDER BY p.productName
    """
    data = Neo4jService.run(query, {"id": int(supplier_id)})
    return Response(data)

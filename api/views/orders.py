from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_orders(request):
    """List all orders or create a new order"""
    if request.method == 'GET':
        query = """
        MATCH (c:Customer)-[:PURCHASED]->(o:Order)
        OPTIONAL MATCH (sh:Shipper)-[:SHIPS]->(o)
        OPTIONAL MATCH (e:Employee)-[:SOLD]->(o)
        RETURN o.orderID AS id,
               o.orderDate AS orderDate,
               o.requiredDate AS requiredDate,
               o.shippedDate AS shippedDate,
               o.freight AS freight,
               o.shipCity AS shipCity,
               o.shipCountry AS shipCountry,
               c.companyName AS customer,
               c.customerID AS customerId,
               sh.companyName AS shipper,
               e.firstName + ' ' + e.lastName AS employee
        ORDER BY o.orderDate DESC
        LIMIT 100
        """
        data = Neo4jService.run(query)
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('customerId'):
            return Response(
                {"error": "customerId is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get next order ID
        id_query = "MATCH (o:Order) RETURN max(o.orderID) AS maxId"
        max_id_result = Neo4jService.run(id_query)
        next_id = (max_id_result[0]['maxId'] or 0) + 1
        
        # Create order
        query = """
        CREATE (o:Order {
            orderID: $orderID,
            orderDate: $orderDate,
            requiredDate: $requiredDate,
            shippedDate: $shippedDate,
            freight: $freight,
            shipName: $shipName,
            shipAddress: $shipAddress,
            shipCity: $shipCity,
            shipRegion: $shipRegion,
            shipPostalCode: $shipPostalCode,
            shipCountry: $shipCountry
        })
        RETURN o.orderID AS id
        """
        result = Neo4jService.run(query, {
            "orderID": next_id,
            "orderDate": data.get('orderDate', ''),
            "requiredDate": data.get('requiredDate', ''),
            "shippedDate": data.get('shippedDate', ''),
            "freight": float(data.get('freight', 0)),
            "shipName": data.get('shipName', ''),
            "shipAddress": data.get('shipAddress', ''),
            "shipCity": data.get('shipCity', ''),
            "shipRegion": data.get('shipRegion', ''),
            "shipPostalCode": data.get('shipPostalCode', ''),
            "shipCountry": data.get('shipCountry', '')
        })
        
        # Link to customer
        Neo4jService.run("""
            MATCH (c:Customer {customerID: $customerId})
            MATCH (o:Order {orderID: $orderID})
            CREATE (c)-[:PURCHASED]->(o)
        """, {"customerId": data.get('customerId'), "orderID": next_id})
        
        # Link to employee if provided
        if data.get('employeeId'):
            Neo4jService.run("""
                MATCH (e:Employee {employeeID: $employeeId})
                MATCH (o:Order {orderID: $orderID})
                CREATE (e)-[:SOLD]->(o)
            """, {"employeeId": int(data.get('employeeId')), "orderID": next_id})
        
        # Link to shipper if provided
        if data.get('shipperId'):
            Neo4jService.run("""
                MATCH (s:Shipper {shipperID: $shipperId})
                MATCH (o:Order {orderID: $orderID})
                CREATE (s)-[:SHIPS]->(o)
            """, {"shipperId": int(data.get('shipperId')), "orderID": next_id})
        
        return Response({"id": next_id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_order(request, order_id):
    """Get, update or delete an order"""
    if request.method == 'GET':
        query = """
        MATCH (c:Customer)-[:PURCHASED]->(o:Order {orderID: $id})
        OPTIONAL MATCH (sh:Shipper)-[:SHIPS]->(o)
        OPTIONAL MATCH (e:Employee)-[:SOLD]->(o)
        RETURN o.orderID AS id,
               o.orderDate AS orderDate,
               o.requiredDate AS requiredDate,
               o.shippedDate AS shippedDate,
               o.freight AS freight,
               o.shipName AS shipName,
               o.shipAddress AS shipAddress,
               o.shipCity AS shipCity,
               o.shipRegion AS shipRegion,
               o.shipPostalCode AS shipPostalCode,
               o.shipCountry AS shipCountry,
               c.companyName AS customer,
               c.customerID AS customerId,
               sh.companyName AS shipper,
               sh.shipperID AS shipperId,
               e.firstName + ' ' + e.lastName AS employee,
               e.employeeID AS employeeId
        """
        data = Neo4jService.run(query, {"id": int(order_id)})
        if not data:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (o:Order {orderID: $id})
        SET o.orderDate = $orderDate,
            o.requiredDate = $requiredDate,
            o.shippedDate = $shippedDate,
            o.freight = $freight,
            o.shipName = $shipName,
            o.shipAddress = $shipAddress,
            o.shipCity = $shipCity,
            o.shipRegion = $shipRegion,
            o.shipPostalCode = $shipPostalCode,
            o.shipCountry = $shipCountry
        RETURN o.orderID AS id
        """
        result = Neo4jService.run(query, {
            "id": int(order_id),
            "orderDate": data.get('orderDate', ''),
            "requiredDate": data.get('requiredDate', ''),
            "shippedDate": data.get('shippedDate', ''),
            "freight": float(data.get('freight', 0)),
            "shipName": data.get('shipName', ''),
            "shipAddress": data.get('shipAddress', ''),
            "shipCity": data.get('shipCity', ''),
            "shipRegion": data.get('shipRegion', ''),
            "shipPostalCode": data.get('shipPostalCode', ''),
            "shipCountry": data.get('shipCountry', '')
        })
        if not result:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result[0])
    
    elif request.method == 'DELETE':
        check_query = "MATCH (o:Order {orderID: $id}) RETURN o"
        exists = Neo4jService.run(check_query, {"id": int(order_id)})
        if not exists:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        query = """
        MATCH (o:Order {orderID: $id})
        DETACH DELETE o
        """
        Neo4jService.run(query, {"id": int(order_id)})
        return Response({"message": "Order deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def order_details(request, order_id):
    """Get order line items or add a product to order"""
    if request.method == 'GET':
        query = """
        MATCH (o:Order {orderID: $id})-[r:ORDERS]->(p:Product)
        RETURN p.productID AS productId,
               p.productName AS productName,
               r.unitPrice AS unitPrice,
               r.quantity AS quantity,
               r.discount AS discount,
               (r.unitPrice * r.quantity * (1 - r.discount)) AS lineTotal
        ORDER BY p.productName
        """
        data = Neo4jService.run(query, {"id": int(order_id)})
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('productId') or not data.get('quantity'):
            return Response(
                {"error": "productId and quantity are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get product price if not provided
        unit_price = data.get('unitPrice')
        if not unit_price:
            price_query = "MATCH (p:Product {productID: $id}) RETURN p.unitPrice AS price"
            price_result = Neo4jService.run(price_query, {"id": int(data.get('productId'))})
            if price_result:
                unit_price = price_result[0]['price']
            else:
                unit_price = 0
        
        query = """
        MATCH (o:Order {orderID: $orderID})
        MATCH (p:Product {productID: $productID})
        CREATE (o)-[r:ORDERS {
            unitPrice: $unitPrice,
            quantity: $quantity,
            discount: $discount
        }]->(p)
        RETURN p.productID AS productId, r.quantity AS quantity
        """
        result = Neo4jService.run(query, {
            "orderID": int(order_id),
            "productID": int(data.get('productId')),
            "unitPrice": float(unit_price),
            "quantity": int(data.get('quantity')),
            "discount": float(data.get('discount', 0))
        })
        return Response(result[0], status=status.HTTP_201_CREATED)

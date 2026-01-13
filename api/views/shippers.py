from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_shippers(request):
    """List all shippers or create a new shipper"""
    if request.method == 'GET':
        query = """
        MATCH (s:Shipper)
        OPTIONAL MATCH (s)-[:SHIPS]->(o:Order)
        RETURN s.shipperID AS id,
               s.companyName AS name,
               s.phone AS phone,
               count(o) AS orderCount
        ORDER BY s.companyName
        """
        data = Neo4jService.run(query)
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('companyName'):
            return Response(
                {"error": "companyName is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get next shipper ID
        id_query = "MATCH (s:Shipper) RETURN max(s.shipperID) AS maxId"
        max_id_result = Neo4jService.run(id_query)
        next_id = (max_id_result[0]['maxId'] or 0) + 1
        
        query = """
        CREATE (s:Shipper {
            shipperID: $shipperID,
            companyName: $companyName,
            phone: $phone
        })
        RETURN s.shipperID AS id, s.companyName AS name
        """
        result = Neo4jService.run(query, {
            "shipperID": next_id,
            "companyName": data.get('companyName'),
            "phone": data.get('phone', '')
        })
        return Response(result[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_shipper(request, shipper_id):
    """Get, update or delete a shipper"""
    if request.method == 'GET':
        query = """
        MATCH (s:Shipper {shipperID: $id})
        RETURN s.shipperID AS id,
               s.companyName AS name,
               s.phone AS phone
        """
        data = Neo4jService.run(query, {"id": int(shipper_id)})
        if not data:
            return Response({"error": "Shipper not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (s:Shipper {shipperID: $id})
        SET s.companyName = $companyName,
            s.phone = $phone
        RETURN s.shipperID AS id, s.companyName AS name
        """
        result = Neo4jService.run(query, {
            "id": int(shipper_id),
            "companyName": data.get('companyName', ''),
            "phone": data.get('phone', '')
        })
        if not result:
            return Response({"error": "Shipper not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result[0])
    
    elif request.method == 'DELETE':
        check_query = "MATCH (s:Shipper {shipperID: $id}) RETURN s"
        exists = Neo4jService.run(check_query, {"id": int(shipper_id)})
        if not exists:
            return Response({"error": "Shipper not found"}, status=status.HTTP_404_NOT_FOUND)
        
        query = """
        MATCH (s:Shipper {shipperID: $id})
        DETACH DELETE s
        """
        Neo4jService.run(query, {"id": int(shipper_id)})
        return Response({"message": "Shipper deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def shipper_orders(request, shipper_id):
    """Get all orders shipped by this shipper"""
    query = """
    MATCH (s:Shipper {shipperID: $id})-[:SHIPS]->(o:Order)
    MATCH (c:Customer)-[:PURCHASED]->(o)
    RETURN o.orderID AS orderId,
           o.orderDate AS orderDate,
           o.shippedDate AS shippedDate,
           o.shipCity AS shipCity,
           o.shipCountry AS shipCountry,
           c.companyName AS customer
    ORDER BY o.shippedDate DESC
    LIMIT 50
    """
    data = Neo4jService.run(query, {"id": int(shipper_id)})
    return Response(data)

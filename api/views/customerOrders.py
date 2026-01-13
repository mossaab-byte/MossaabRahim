from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services.neo4j import Neo4jService


@api_view(['GET'])
def customer_orders(request, customer_id):
    query = """
    MATCH (c:Customer {customerID:$id})-[:PURCHASED]->(o:Order)
    RETURN o.orderID AS id, o.orderDate AS date
    ORDER BY o.orderDate DESC
    LIMIT 20
    """
    data = Neo4jService.run(query, {"id": customer_id})
    return Response(data)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services.neo4j import Neo4jService


@api_view(['GET'])
def order_products(request, order_id):
    query = """
    MATCH (o:Order {orderID:$id})-[:ORDERS]->(p:Product)
    RETURN p.productName AS name, p.quantity AS quantity
    """
    data = Neo4jService.run(query, {"id": int(order_id)})
    return Response(data)
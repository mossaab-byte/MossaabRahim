from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_customers(request):
    """List all customers or create a new customer"""
    if request.method == 'GET':
        query = """
        MATCH (c:Customer)
        OPTIONAL MATCH (c)-[:PURCHASED]->(o:Order)
        RETURN c.customerID AS id,
               c.companyName AS name,
               c.contactName AS contactName,
               c.city AS city,
               c.country AS country,
               count(o) AS orderCount
        ORDER BY c.companyName
        LIMIT 100
        """
        data = Neo4jService.run(query)
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('customerID') or not data.get('companyName'):
            return Response(
                {"error": "customerID and companyName are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        query = """
        CREATE (c:Customer {
            customerID: $customerID,
            companyName: $companyName,
            contactName: $contactName,
            contactTitle: $contactTitle,
            address: $address,
            city: $city,
            region: $region,
            postalCode: $postalCode,
            country: $country,
            phone: $phone,
            fax: $fax
        })
        RETURN c.customerID AS id, c.companyName AS name
        """
        result = Neo4jService.run(query, {
            "customerID": data.get('customerID'),
            "companyName": data.get('companyName'),
            "contactName": data.get('contactName', ''),
            "contactTitle": data.get('contactTitle', ''),
            "address": data.get('address', ''),
            "city": data.get('city', ''),
            "region": data.get('region', ''),
            "postalCode": data.get('postalCode', ''),
            "country": data.get('country', ''),
            "phone": data.get('phone', ''),
            "fax": data.get('fax', '')
        })
        return Response(result[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_customer(request, customer_id):
    """Get, update or delete a customer"""
    if request.method == 'GET':
        query = """
        MATCH (c:Customer {customerID: $id})
        RETURN c.customerID AS id,
               c.companyName AS name,
               c.contactName AS contactName,
               c.contactTitle AS contactTitle,
               c.address AS address,
               c.city AS city,
               c.region AS region,
               c.postalCode AS postalCode,
               c.country AS country,
               c.phone AS phone,
               c.fax AS fax
        """
        data = Neo4jService.run(query, {"id": customer_id})
        if not data:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (c:Customer {customerID: $id})
        SET c.companyName = $companyName,
            c.contactName = $contactName,
            c.contactTitle = $contactTitle,
            c.address = $address,
            c.city = $city,
            c.region = $region,
            c.postalCode = $postalCode,
            c.country = $country,
            c.phone = $phone,
            c.fax = $fax
        RETURN c.customerID AS id, c.companyName AS name
        """
        result = Neo4jService.run(query, {
            "id": customer_id,
            "companyName": data.get('companyName', ''),
            "contactName": data.get('contactName', ''),
            "contactTitle": data.get('contactTitle', ''),
            "address": data.get('address', ''),
            "city": data.get('city', ''),
            "region": data.get('region', ''),
            "postalCode": data.get('postalCode', ''),
            "country": data.get('country', ''),
            "phone": data.get('phone', ''),
            "fax": data.get('fax', '')
        })
        if not result:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result[0])
    
    elif request.method == 'DELETE':
        # First check if customer exists
        check_query = "MATCH (c:Customer {customerID: $id}) RETURN c"
        exists = Neo4jService.run(check_query, {"id": customer_id})
        if not exists:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete customer and their relationships
        query = """
        MATCH (c:Customer {customerID: $id})
        DETACH DELETE c
        """
        Neo4jService.run(query, {"id": customer_id})
        return Response({"message": "Customer deleted"}, status=status.HTTP_204_NO_CONTENT)





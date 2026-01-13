from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_suppliers(request):
    """List all suppliers or create a new supplier"""
    if request.method == 'GET':
        query = """
        MATCH (s:Supplier)
        OPTIONAL MATCH (s)-[:SUPPLIES]->(p:Product)
        RETURN s.supplierID AS id,
               s.companyName AS name,
               s.contactName AS contactName,
               s.contactTitle AS contactTitle,
               s.city AS city,
               s.country AS country,
               s.phone AS phone,
               count(p) AS productCount
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
        
        # Get next supplier ID
        id_query = "MATCH (s:Supplier) RETURN max(s.supplierID) AS maxId"
        max_id_result = Neo4jService.run(id_query)
        next_id = (max_id_result[0]['maxId'] or 0) + 1
        
        query = """
        CREATE (s:Supplier {
            supplierID: $supplierID,
            companyName: $companyName,
            contactName: $contactName,
            contactTitle: $contactTitle,
            address: $address,
            city: $city,
            region: $region,
            postalCode: $postalCode,
            country: $country,
            phone: $phone,
            fax: $fax,
            homePage: $homePage
        })
        RETURN s.supplierID AS id, s.companyName AS name
        """
        result = Neo4jService.run(query, {
            "supplierID": next_id,
            "companyName": data.get('companyName'),
            "contactName": data.get('contactName', ''),
            "contactTitle": data.get('contactTitle', ''),
            "address": data.get('address', ''),
            "city": data.get('city', ''),
            "region": data.get('region', ''),
            "postalCode": data.get('postalCode', ''),
            "country": data.get('country', ''),
            "phone": data.get('phone', ''),
            "fax": data.get('fax', ''),
            "homePage": data.get('homePage', '')
        })
        return Response(result[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_supplier(request, supplier_id):
    """Get, update or delete a supplier"""
    if request.method == 'GET':
        query = """
        MATCH (s:Supplier {supplierID: $id})
        RETURN s.supplierID AS id,
               s.companyName AS name,
               s.contactName AS contactName,
               s.contactTitle AS contactTitle,
               s.address AS address,
               s.city AS city,
               s.region AS region,
               s.postalCode AS postalCode,
               s.country AS country,
               s.phone AS phone,
               s.fax AS fax,
               s.homePage AS homePage
        """
        data = Neo4jService.run(query, {"id": int(supplier_id)})
        if not data:
            return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (s:Supplier {supplierID: $id})
        SET s.companyName = $companyName,
            s.contactName = $contactName,
            s.contactTitle = $contactTitle,
            s.address = $address,
            s.city = $city,
            s.region = $region,
            s.postalCode = $postalCode,
            s.country = $country,
            s.phone = $phone,
            s.fax = $fax,
            s.homePage = $homePage
        RETURN s.supplierID AS id, s.companyName AS name
        """
        result = Neo4jService.run(query, {
            "id": int(supplier_id),
            "companyName": data.get('companyName', ''),
            "contactName": data.get('contactName', ''),
            "contactTitle": data.get('contactTitle', ''),
            "address": data.get('address', ''),
            "city": data.get('city', ''),
            "region": data.get('region', ''),
            "postalCode": data.get('postalCode', ''),
            "country": data.get('country', ''),
            "phone": data.get('phone', ''),
            "fax": data.get('fax', ''),
            "homePage": data.get('homePage', '')
        })
        if not result:
            return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result[0])
    
    elif request.method == 'DELETE':
        check_query = "MATCH (s:Supplier {supplierID: $id}) RETURN s"
        exists = Neo4jService.run(check_query, {"id": int(supplier_id)})
        if not exists:
            return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
        
        query = """
        MATCH (s:Supplier {supplierID: $id})
        DETACH DELETE s
        """
        Neo4jService.run(query, {"id": int(supplier_id)})
        return Response({"message": "Supplier deleted"}, status=status.HTTP_204_NO_CONTENT)

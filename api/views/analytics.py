from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services.neo4j import Neo4jService


@api_view(['GET'])
def top_products(request):
    """Get top 10 products by number of orders"""
    limit = request.query_params.get('limit', 10)
    query = """
    MATCH (:Order)-[r:ORDERS]->(p:Product)
    RETURN p.productID AS id,
           p.productName AS name,
           count(*) AS orderCount,
           sum(r.quantity) AS totalQuantity,
           sum(r.unitPrice * r.quantity) AS totalRevenue
    ORDER BY totalRevenue DESC
    LIMIT $limit
    """
    data = Neo4jService.run(query, {"limit": int(limit)})
    return Response(data)


@api_view(['GET'])
def top_customers(request):
    """Get top customers by number of orders"""
    limit = request.query_params.get('limit', 10)
    query = """
    MATCH (c:Customer)-[:PURCHASED]->(o:Order)
    OPTIONAL MATCH (o)-[r:ORDERS]->(p:Product)
    RETURN c.customerID AS id,
           c.companyName AS name,
           c.country AS country,
           count(DISTINCT o) AS orderCount,
           sum(r.unitPrice * r.quantity) AS totalSpent
    ORDER BY totalSpent DESC
    LIMIT $limit
    """
    data = Neo4jService.run(query, {"limit": int(limit)})
    return Response(data)


@api_view(['GET'])
def top_employees(request):
    """Get top employees by sales"""
    limit = request.query_params.get('limit', 10)
    query = """
    MATCH (e:Employee)-[:SOLD]->(o:Order)
    OPTIONAL MATCH (o)-[r:ORDERS]->(p:Product)
    RETURN e.employeeID AS id,
           e.firstName + ' ' + e.lastName AS name,
           e.title AS title,
           count(DISTINCT o) AS orderCount,
           sum(r.unitPrice * r.quantity) AS totalSales
    ORDER BY totalSales DESC
    LIMIT $limit
    """
    data = Neo4jService.run(query, {"limit": int(limit)})
    return Response(data)


@api_view(['GET'])
def sales_by_category(request):
    """Get sales breakdown by category"""
    query = """
    MATCH (o:Order)-[r:ORDERS]->(p:Product)-[:PART_OF]->(c:Category)
    RETURN c.categoryID AS id,
           c.categoryName AS category,
           count(DISTINCT o) AS orderCount,
           sum(r.quantity) AS totalQuantity,
           sum(r.unitPrice * r.quantity) AS totalRevenue
    ORDER BY totalRevenue DESC
    """
    data = Neo4jService.run(query)
    return Response(data)


@api_view(['GET'])
def sales_by_country(request):
    """Get sales breakdown by customer country"""
    query = """
    MATCH (c:Customer)-[:PURCHASED]->(o:Order)-[r:ORDERS]->(p:Product)
    RETURN c.country AS country,
           count(DISTINCT c) AS customerCount,
           count(DISTINCT o) AS orderCount,
           sum(r.unitPrice * r.quantity) AS totalRevenue
    ORDER BY totalRevenue DESC
    """
    data = Neo4jService.run(query)
    return Response(data)


@api_view(['GET'])
def sales_by_supplier(request):
    """Get sales breakdown by supplier"""
    query = """
    MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)<-[r:ORDERS]-(o:Order)
    RETURN s.supplierID AS id,
           s.companyName AS supplier,
           s.country AS country,
           count(DISTINCT p) AS productCount,
           sum(r.quantity) AS totalQuantity,
           sum(r.unitPrice * r.quantity) AS totalRevenue
    ORDER BY totalRevenue DESC
    """
    data = Neo4jService.run(query)
    return Response(data)


@api_view(['GET'])
def shipping_stats(request):
    """Get shipping statistics by shipper"""
    query = """
    MATCH (sh:Shipper)-[:SHIPS]->(o:Order)
    RETURN sh.shipperID AS id,
           sh.companyName AS shipper,
           count(o) AS orderCount,
           avg(o.freight) AS avgFreight,
           sum(o.freight) AS totalFreight
    ORDER BY orderCount DESC
    """
    data = Neo4jService.run(query)
    return Response(data)


@api_view(['GET'])
def monthly_sales(request):
    """Get monthly sales summary"""
    year = request.query_params.get('year', None)
    query = """
    MATCH (o:Order)-[r:ORDERS]->(p:Product)
    WHERE $year IS NULL OR o.orderDate STARTS WITH $year
    RETURN substring(o.orderDate, 0, 7) AS month,
           count(DISTINCT o) AS orderCount,
           sum(r.unitPrice * r.quantity) AS revenue
    ORDER BY month
    """
    data = Neo4jService.run(query, {"year": year})
    return Response(data)


@api_view(['GET'])
def dashboard_summary(request):
    """Get dashboard summary statistics"""
    query = """
    MATCH (c:Customer) WITH count(c) AS customerCount
    MATCH (p:Product) WITH customerCount, count(p) AS productCount
    MATCH (o:Order) WITH customerCount, productCount, count(o) AS orderCount
    MATCH (s:Supplier) WITH customerCount, productCount, orderCount, count(s) AS supplierCount
    MATCH (e:Employee) WITH customerCount, productCount, orderCount, supplierCount, count(e) AS employeeCount
    MATCH (:Order)-[r:ORDERS]->(:Product)
    RETURN customerCount,
           productCount,
           orderCount,
           supplierCount,
           employeeCount,
           sum(r.unitPrice * r.quantity) AS totalRevenue
    """
    data = Neo4jService.run(query)
    return Response(data[0] if data else {})

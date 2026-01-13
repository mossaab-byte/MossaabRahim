from django.urls import path

# Customers
from api.views.customers import list_customers, get_customer
from api.views.customerOrders import customer_orders

# Products
from api.views.products import (
    list_products, get_product, product_orders,
    products_by_category, products_by_supplier
)

# Orders
from api.views.orders import list_orders, get_order, order_details
from api.views.orderProducts import order_products

# Suppliers
from api.views.suppliers import list_suppliers, get_supplier

# Categories
from api.views.categories import list_categories, get_category

# Employees
from api.views.employees import (
    list_employees, get_employee, employee_orders,
    employee_territories, employee_subordinates
)

# Shippers
from api.views.shippers import list_shippers, get_shipper, shipper_orders

# Regions & Territories
from api.views.regions import (
    list_regions, get_region, region_territories,
    list_territories, get_territory, territory_employees
)

# Analytics
from api.views.analytics import (
    top_products, top_customers, top_employees,
    sales_by_category, sales_by_country, sales_by_supplier,
    shipping_stats, monthly_sales, dashboard_summary
)

urlpatterns = [
    # Customers
    path("customers/", list_customers),
    path("customers/<str:customer_id>/", get_customer),
    path("customers/<str:customer_id>/orders/", customer_orders),

    # Products
    path("products/", list_products),
    path("products/<int:product_id>/", get_product),
    path("products/<int:product_id>/orders/", product_orders),

    # Orders
    path("orders/", list_orders),
    path("orders/<int:order_id>/", get_order),
    path("orders/<int:order_id>/details/", order_details),
    path("orders/<int:order_id>/products/", order_products),

    # Suppliers
    path("suppliers/", list_suppliers),
    path("suppliers/<int:supplier_id>/", get_supplier),
    path("suppliers/<int:supplier_id>/products/", products_by_supplier),

    # Categories
    path("categories/", list_categories),
    path("categories/<int:category_id>/", get_category),
    path("categories/<int:category_id>/products/", products_by_category),

    # Employees
    path("employees/", list_employees),
    path("employees/<int:employee_id>/", get_employee),
    path("employees/<int:employee_id>/orders/", employee_orders),
    path("employees/<int:employee_id>/territories/", employee_territories),
    path("employees/<int:employee_id>/subordinates/", employee_subordinates),

    # Shippers
    path("shippers/", list_shippers),
    path("shippers/<int:shipper_id>/", get_shipper),
    path("shippers/<int:shipper_id>/orders/", shipper_orders),

    # Regions
    path("regions/", list_regions),
    path("regions/<int:region_id>/", get_region),
    path("regions/<int:region_id>/territories/", region_territories),

    # Territories
    path("territories/", list_territories),
    path("territories/<str:territory_id>/", get_territory),
    path("territories/<str:territory_id>/employees/", territory_employees),

    # Analytics
    path("analytics/dashboard/", dashboard_summary),
    path("analytics/top-products/", top_products),
    path("analytics/top-customers/", top_customers),
    path("analytics/top-employees/", top_employees),
    path("analytics/sales-by-category/", sales_by_category),
    path("analytics/sales-by-country/", sales_by_country),
    path("analytics/sales-by-supplier/", sales_by_supplier),
    path("analytics/shipping-stats/", shipping_stats),
    path("analytics/monthly-sales/", monthly_sales),
]
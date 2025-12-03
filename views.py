from flask import Blueprint, render_template, request, redirect, url_for
from models import (
    db, Product, GarmentBatch, Customer, Orders, Service,
    OrderDetail, MaterialUsed, Supplier, Materials
)

views = Blueprint("views", __name__)


# =====================================
#               HOME
# =====================================
@views.route("/")
def home():
    return render_template("index.html")



@views.route("/view/suppliers")
def view_suppliers():
    suppliers = Supplier.query.all()
    return render_template("suppliers.html", suppliers=suppliers)

@views.route("/view/materials")
def view_materials():
    materials = Materials.query.all()
    return render_template("materials.html", materials=materials)

@views.route("/view/customers")
def view_customers():
    customers = Customer.query.all()
    return render_template("customers.html", customers=customers)

@views.route("/view/products")
def view_products():
    products = Product.query.all()
    return render_template("products.html", products=products)

@views.route("/view/orders")
def view_orders():
    orders = Orders.query.all()
    return render_template("orders.html", orders=orders)

@views.route("/view/services")
def view_services():
    services = Service.query.all()
    return render_template("services.html", services=services)

@views.route("/view/batches")
def view_batches():
    batches = GarmentBatch.query.all()
    return render_template("batches.html", batches=batches)

@views.route("/view/order_details")
def view_order_details():
    details = OrderDetail.query.all()
    return render_template("order_details.html", details=details)

@views.route("/view/material_used")
def view_material_used():
    used = MaterialUsed.query.all()
    return render_template("material_used.html", used=used)

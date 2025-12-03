from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

from flask import render_template


# IMPORTA tus modelos reales
from models import db,Product, GarmentBatch, Customer, Orders, Service, OrderDetail, MaterialUsed, Supplier, Materials


app = Flask(__name__, template_folder="templates", static_folder="static")


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

from views import views
app.register_blueprint(views)

@app.route("/suppliers", methods=["POST"])
def create_supplier():
    data = request.json if request.is_json else request.form
    supplier = Supplier(
        Supplier_ID=data["Supplier_ID"],
        Supplier_Name=data["Supplier_Name"],
        Phone_number=data["Phone_number"],
        Email=data["Email"]
    )
    supplier.create()
    return jsonify({"message": "Supplier created"}), 201


@app.route("/suppliers", methods=["GET"])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([
        {
            "Supplier_ID": s.Supplier_ID,
            "Supplier_Name": s.Supplier_Name,
            "Phone_number": s.Phone_number,
            "Email": s.Email
        }
        for s in suppliers
    ])

# Obtener un supplier por ID
@app.route("/suppliers/<id>", methods=["GET"])
def get_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    return jsonify({
        "Supplier_ID": supplier.Supplier_ID,
        "Supplier_Name": supplier.Supplier_Name,
        "Phone_number": supplier.Phone_number,
        "Email": supplier.Email
    })



@app.route("/suppliers/<id>", methods=["PUT"])
def update_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    data = request.json if request.is_json else request.form
    supplier.Supplier_Name = data.get("Supplier_Name", supplier.Supplier_Name)
    supplier.Phone_number = data.get("Phone_number", supplier.Phone_number)
    supplier.Email = data.get("Email", supplier.Email)
    db.session.commit()

    return jsonify({"message": "Supplier updated"})


@app.route("/suppliers/<id>", methods=["DELETE"])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    db.session.delete(supplier)
    db.session.commit()

    return jsonify({"message": "Supplier deleted"})



# MATERIALS CRUD
# ───────────────────────────────

@app.route("/materials", methods=["POST"])
def create_material():
    data = request.json if request.is_json else request.form
    
    material = Materials(
        Material_ID=data["Material_ID"],
        Supplier_ID=data["Supplier_ID"],
        Stock=data["Stock"],
        Name=data["Name"]
    )
    material.create()
    return jsonify({"message": "Material created"}), 201


@app.route("/materials", methods=["GET"])
def get_materials():
    materials = Materials.query.all()
    return jsonify([
        {
            "Material_ID": m.Material_ID,
            "Supplier_ID": m.Supplier_ID,
            "Stock": m.Stock,
            "Name": m.Name
        }
        for m in materials
    ])


@app.route("/materials/<id>", methods=["GET"])
def get_material(id):
    material = Materials.query.get(id)
    if not material:
        return jsonify({"error": "Material not found"}), 404
    return jsonify({
        "Material_ID": material.Material_ID,
        "Supplier_ID": material.Supplier_ID,
        "Stock": material.Stock,
        "Name": material.Name
    })


@app.route("/materials/<id>", methods=["PUT"])
def update_material(id):
    material = Materials.query.get(id)
    if not material:
        return jsonify({"error": "Material not found"}), 404

    data = request.json if request.is_json else request.form
    
    material.Stock = data.get("Stock", material.Stock)
    material.Name = data.get("Name", material.Name)
    db.session.commit()

    return jsonify({"message": "Material updated"})


@app.route("/materials/<id>", methods=["DELETE"])
def delete_material(id):
    material = Materials.query.get(id)
    if not material:
        return jsonify({"error": "Material not found"}), 404

    db.session.delete(material)
    db.session.commit()

    return jsonify({"message": "Material deleted"})
#------------------------------------------------------------------------------------------
# CRUD CUSTOMER

#------------------------------------------------------------------------------------------
# CRUD CUSTOMER
# ───────────────────────────────────────

@app.route("/customers", methods=["POST"])
def create_customer():
    data = request.json if request.is_json else request.form

    customer = Customer(
        Customer_ID=data["Customer_ID"],
        First_Name=data["First_Name"],
        Last_name=data["Last_name"],
        Phone_number=data["Phone_number"],
        Address=data["Address"],
        Email=data["Email"]
    )

    customer.create()
    return jsonify({"message": "Customer created"}), 201


@app.route("/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([
        {
            "Customer_ID": c.Customer_ID,
            "First_Name": c.First_Name,
            "Last_name": c.Last_name,
            "Phone_number": c.Phone_number,
            "Address": c.Address,
            "Email": c.Email
        }
        for c in customers
    ])

@app.route("/customers/<id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({
        "Customer_ID": customer.Customer_ID,
        "First_Name": customer.First_Name,
        "Last_name": customer.Last_name,
        "Phone_number": customer.Phone_number,
        "Address": customer.Address,
        "Email": customer.Email
    })


@app.route("/customers/<id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.json if request.is_json else request.form
    
    customer.First_Name = data.get("First_Name", customer.First_Name)
    customer.Last_name = data.get("Last_name", customer.Last_name)
    customer.Phone_number = data.get("Phone_number", customer.Phone_number)
    customer.Address = data.get("Address", customer.Address)
    customer.Email = data.get("Email", customer.Email)

    db.session.commit()
    return jsonify({"message": "Customer updated"})


@app.route("/customers/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"})


#------------------------------------------------------------------------------------------
# CRUD ORDER DETAIL
# ───────────────────────────────────────

@app.route("/order_details", methods=["POST"])
def create_order_detail():
    data = request.json if request.is_json else request.form
    
    detail = OrderDetail(
        Detail_ID=data["Detail_ID"],
        Order_ID=data["Order_ID"],
        Service_ID=data["Service_ID"],
        Product_ID=data["Product_ID"],
        Subtotal=data["Subtotal"]
    )

    detail.create()
    return jsonify({"message": "Order detail created"}), 201


@app.route("/order_details", methods=["GET"])
def get_order_details():
    details = OrderDetail.query.all()
    return jsonify([
        {
            "Detail_ID": d.Detail_ID,
            "Order_ID": d.Order_ID,
            "Service_ID": d.Service_ID,
            "Product_ID": d.Product_ID,
            "Subtotal": d.Subtotal
        }
        for d in details
    ])

@app.route("/order_details/<id>", methods=["GET"])
def get_order_detail(id):
    detail = OrderDetail.query.get(id)
    if not detail:
        return jsonify({"error": "Order detail not found"}), 404
    return jsonify({
        "Detail_ID": detail.Detail_ID,
        "Order_ID": detail.Order_ID,
        "Service_ID": detail.Service_ID,
        "Product_ID": detail.Product_ID,
        "Subtotal": detail.Subtotal
    })


@app.route("/order_details/<id>", methods=["PUT"])
def update_order_detail(id):
    detail = OrderDetail.query.get(id)
    if not detail:
        return jsonify({"error": "Order detail not found"}), 404

    data = request.json if request.is_json else request.form
    
    detail.Order_ID = data.get("Order_ID", detail.Order_ID)
    detail.Service_ID = data.get("Service_ID", detail.Service_ID)
    detail.Product_ID = data.get("Product_ID", detail.Product_ID)
    detail.Subtotal = data.get("Subtotal", detail.Subtotal)

    db.session.commit()
    return jsonify({"message": "Order detail updated"})


@app.route("/order_details/<id>", methods=["DELETE"])
def delete_order_detail(id):
    detail = OrderDetail.query.get(id)
    if not detail:
        return jsonify({"error": "Order detail not found"}), 404

    db.session.delete(detail)
    db.session.commit()
    return jsonify({"message": "Order detail deleted"})



#------------------------------------------------------------------------------------------
# CRUD PRODUCT
# ───────────────────────────────────────

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json if request.is_json else request.form
    
    product = Product(
        Product_ID=data["Product_ID"],
        Product_Name=data["Product_Name"],
        Description=data["Description"],
        Price=data["Price"],
        Stock=data["Stock"]
    )
    product.create()
    return jsonify({"message": "Product created"}), 201


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "Product_ID": p.Product_ID,
            "Product_Name": p.Product_Name,
            "Description": p.Description,
            "Price": str(p.Price),
            "Stock": p.Stock
        }
        for p in products
    ])

@app.route("/products/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "Product_ID": product.Product_ID,
        "Product_Name": product.Product_Name,
        "Description": product.Description,
        "Price": str(product.Price),
        "Stock": product.Stock
    })


@app.route("/products/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.json if request.is_json else request.form
    
    product.Product_Name = data.get("Product_Name", product.Product_Name)
    product.Description = data.get("Description", product.Description)
    product.Price = data.get("Price", product.Price)
    product.Stock = data.get("Stock", product.Stock)

    db.session.commit()
    return jsonify({"message": "Product updated"})


@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


#------------------------------------------------------------------------------------------
# CRUD GARMENT BATCH
# ───────────────────────────────────────

@app.route("/batches", methods=["POST"])
def create_batch():
    data = request.json if request.is_json else request.form

    batch = GarmentBatch(
        Garment_batch_ID=data["Garment_batch_ID"],
        Product_ID=data["Product_ID"],
        Start_date=data["Start_date"],
        Finish_date=data["Finish_date"],
        Quantity_produced=data["Quantity_produced"]
    )

    batch.create()
    return jsonify({"message": "Garment batch created"}), 201


@app.route("/batches", methods=["GET"])
def get_batches():
    batches = GarmentBatch.query.all()
    return jsonify([
        {
            "Garment_batch_ID": b.Garment_batch_ID,
            "Product_ID": b.Product_ID,
            "Start_date": str(b.Start_date),
            "Finish_date": str(b.Finish_date),
            "Quantity_produced": b.Quantity_produced
        }
        for b in batches
    ])

@app.route("/batches/<id>", methods=["GET"])
def get_batch(id):
    batch = GarmentBatch.query.get(id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404
    return jsonify({
        "Garment_batch_ID": batch.Garment_batch_ID,
        "Product_ID": batch.Product_ID,
        "Start_date": str(batch.Start_date),
        "Finish_date": str(batch.Finish_date),
        "Quantity_produced": batch.Quantity_produced
    })


@app.route("/batches/<id>", methods=["PUT"])
def update_batch(id):
    batch = GarmentBatch.query.get(id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404

    data = request.json if request.is_json else request.form
    
    batch.Product_ID = data.get("Product_ID", batch.Product_ID)
    batch.Start_date = data.get("Start_date", batch.Start_date)
    batch.Finish_date = data.get("Finish_date", batch.Finish_date)
    batch.Quantity_produced = data.get("Quantity_produced", batch.Quantity_produced)

    db.session.commit()
    return jsonify({"message": "Batch updated"})


@app.route("/batches/<id>", methods=["DELETE"])
def delete_batch(id):
    batch = GarmentBatch.query.get(id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404

    db.session.delete(batch)
    db.session.commit()
    return jsonify({"message": "Batch deleted"})



#------------------------------------------------------------------------------------------
# CRUD ORDERS
# ───────────────────────────────────────

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json if request.is_json else request.form

    order = Orders(
        Order_ID=data["Order_ID"],
        Customer_ID=data["Customer_ID"],
        Date=data["Date"],
        State=data["State"]
    )

    order.create()
    return jsonify({"message": "Order created"}), 201


@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Orders.query.all()
    return jsonify([
        {
            "Order_ID": o.Order_ID,
            "Customer_ID": o.Customer_ID,
            "Date": str(o.Date),
            "State": o.State
        }
        for o in orders
    ])

@app.route("/orders/<id>", methods=["GET"])
def get_order(id):
    order = Orders.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({
        "Order_ID": order.Order_ID,
        "Customer_ID": order.Customer_ID,
        "Date": str(order.Date),
        "State": order.State
    })


@app.route("/orders/<id>", methods=["PUT"])
def update_order(id):
    order = Orders.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.json if request.is_json else request.form
    
    order.Customer_ID = data.get("Customer_ID", order.Customer_ID)
    order.Date = data.get("Date", order.Date)
    order.State = data.get("State", order.State)

    db.session.commit()
    return jsonify({"message": "Order updated"})


@app.route("/orders/<id>", methods=["DELETE"])
def delete_order(id):
    order = Orders.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"})



#------------------------------------------------------------------------------------------
# CRUD SERVICE
# ───────────────────────────────────────

@app.route("/services", methods=["POST"])
def create_service():
    data = request.json if request.is_json else request.form

    service = Service(
        Service_ID=data["Service_ID"],
        Description=data["Description"],
        Price=data["Price"]
    )

    service.create()
    return jsonify({"message": "Service created"}), 201


@app.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([
        {
            "Service_ID": s.Service_ID,
            "Description": s.Description,
            "Price": str(s.Price)
        }
        for s in services
    ])

@app.route("/services/<id>", methods=["GET"])
def get_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    return jsonify({
        "Service_ID": service.Service_ID,
        "Description": service.Description,
        "Price": str(service.Price)
    })


@app.route("/services/<id>", methods=["PUT"])
def update_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    data = request.json if request.is_json else request.form
    
    service.Description = data.get("Description", service.Description)
    service.Price = data.get("Price", service.Price)

    db.session.commit()
    return jsonify({"message": "Service updated"})


@app.route("/services/<id>", methods=["DELETE"])
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted"})


#------------------------------------------------------------------------------------------
# CRUD MATERIAL USED
# ───────────────────────────────────────

@app.route("/material_used", methods=["POST"])
def create_material_used():
    data = request.json if request.is_json else request.form
    

    mu = MaterialUsed(
        Material_ID=data["Material_ID"],
        Garment_batch_ID=data["Garment_batch_ID"],
        Quantity_used=data["Quantity_used"]
    )

    mu.create()
    return jsonify({"message": "Material used added"}), 201


@app.route("/material_used", methods=["GET"])
def get_material_used():
    relations = MaterialUsed.query.all()
    return jsonify([
        {
            "Material_ID": r.Material_ID,
            "Garment_batch_ID": r.Garment_batch_ID,
            "Quantity_used": r.Quantity_used
        }
        for r in relations
    ])

@app.route("/material_used/<mat>/<batch>", methods=["GET"])
def get_material_used1(mat, batch):
    mu = MaterialUsed.query.filter_by(Material_ID=mat, Garment_batch_ID=batch).first()
    if not mu:
        return jsonify({"error": "Relation not found"}), 404
    return jsonify({
        "Material_ID": mu.Material_ID,
        "Garment_batch_ID": mu.Garment_batch_ID,
        "Quantity_used": mu.Quantity_used
    })


@app.route("/material_used/<mat>/<batch>", methods=["PUT"])
def update_material_used(mat, batch):
    mu = MaterialUsed.query.filter_by(Material_ID=mat, Garment_batch_ID=batch).first()

    if not mu:
        return jsonify({"error": "Relation not found"}), 404

    data = request.json if request.is_json else request.form
    
    mu.Quantity_used = data.get("Quantity_used", mu.Quantity_used)

    db.session.commit()
    return jsonify({"message": "Material used updated"})


@app.route("/material_used/<mat>/<batch>", methods=["DELETE"])
def delete_material_used(mat, batch):
    mu = MaterialUsed.query.filter_by(Material_ID=mat, Garment_batch_ID=batch).first()

    if not mu:
        return jsonify({"error": "Relation not found"}), 404

    db.session.delete(mu)
    db.session.commit()
    return jsonify({"message": "Material used deleted"})









if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DECIMAL, Date, Integer
from sqlalchemy.orm import relationship, backref
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = "Product"
    Product_ID = db.Column(db.String(15), primary_key=True)
    Product_Name = db.Column(db.String(30), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    Price = db.Column(DECIMAL, nullable=False) 
    Stock = db.Column(db.String(50), nullable=False)

    batches = db.relationship("GarmentBatch", backref="product", cascade="all, delete-orphan")
    details = db.relationship("OrderDetail", backref="product", cascade="all, delete-orphan")

    def __init__(self, Product_ID, Product_Name, Description, Price, Stock):
        self.Product_ID = Product_ID
        self.Product_Name = Product_Name
        self.Description = Description
        self.Price = Price
        self.Stock = Stock

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __repr__(self):
        return f"<Product {self.Product_ID}: {self.Product_Name}>"


class GarmentBatch(db.Model):
    __tablename__ = "Garment_batch"
    Garment_batch_ID = db.Column(db.String(15), primary_key=True)
    Product_ID = db.Column(db.String(15), ForeignKey('Product.Product_ID'), nullable=False)
    Start_date = db.Column(Date, nullable=False)
    Finish_date = db.Column(Date, nullable=False)
    Quantity_produced = db.Column(Integer, nullable=False)


    materials_used = db.relationship("MaterialUsed", backref="garment_batch", cascade="all, delete-orphan")

    def __init__(self, Garment_batch_ID, Product_ID, Start_date, Finish_date, Quantity_produced):
        self.Garment_batch_ID = Garment_batch_ID
        self.Product_ID = Product_ID
        self.Start_date = Start_date
        self.Finish_date = Finish_date
        self.Quantity_produced = Quantity_produced

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Batch {self.Garment_batch_ID} for P:{self.Product_ID}>"



class Customer(db.Model):
    __tablename__ = "Customer"
    Customer_ID = db.Column(db.String(15), primary_key=True)
    First_Name = db.Column(db.String(30), nullable=False)
    Last_name = db.Column(db.String(30), nullable=False)
    Phone_number = db.Column(db.String(10), nullable=False)
    Address = db.Column(db.String(30), nullable=False)
    Email = db.Column(db.String(100), nullable=False)

    orders = db.relationship("Orders", backref="customer", cascade="all, delete-orphan")

    def __init__(self, Customer_ID, First_Name, Last_name, Phone_number, Address, Email):
        self.Customer_ID = Customer_ID
        self.First_Name = First_Name
        self.Last_name = Last_name
        self.Phone_number = Phone_number
        self.Address = Address
        self.Email = Email

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Customer {self.Customer_ID}: {self.First_Name} {self.Last_name}>"


class Orders(db.Model):
    __tablename__ = "Orders"
    Order_ID = db.Column(db.String(15), primary_key=True)
    Customer_ID = db.Column(db.String(15), ForeignKey('Customer.Customer_ID'), nullable=False)
    Date = db.Column(Date, nullable=False)
    State = db.Column(db.String(50), nullable=False)

    details = db.relationship("OrderDetail", backref="order", cascade="all, delete-orphan")

    def __init__(self, Order_ID, Customer_ID, Date, State):
        self.Order_ID = Order_ID
        self.Customer_ID = Customer_ID
        self.Date = Date
        self.State = State

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Order {self.Order_ID} by C:{self.Customer_ID}>"


class Service(db.Model):
    __tablename__ = "Service"
    Service_ID = db.Column(db.String(15), primary_key=True)
    Description = db.Column(db.String(100), nullable=False)
    Price = db.Column(DECIMAL(10, 2), nullable=False)

    details = db.relationship("OrderDetail", backref="service", cascade="all, delete-orphan")

    def __init__(self, Service_ID, Description, Price):
        self.Service_ID = Service_ID
        self.Description = Description
        self.Price = Price

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Service {self.Service_ID}: {self.Description[:10]}...>"


class OrderDetail(db.Model):
    __tablename__ = "Order_detail"
    Detail_ID = db.Column(db.String(15), primary_key=True)
    Order_ID = db.Column(db.String(15), ForeignKey('Orders.Order_ID'), nullable=False)
    Service_ID = db.Column(db.String(15), ForeignKey('Service.Service_ID'), nullable=False)
    Product_ID = db.Column(db.String(15), ForeignKey('Product.Product_ID'), nullable=False)
    Subtotal = db.Column(db.String(15), nullable=False) 

    def __init__(self, Detail_ID, Order_ID, Service_ID, Product_ID, Subtotal):
        self.Detail_ID = Detail_ID
        self.Order_ID = Order_ID
        self.Service_ID = Service_ID
        self.Product_ID = Product_ID
        self.Subtotal = Subtotal

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Detail {self.Detail_ID} for O:{self.Order_ID}>"


class Supplier(db.Model):
    __tablename__ = "Supplier"
    Supplier_ID = db.Column(db.String(15), primary_key=True)
    Supplier_Name = db.Column(db.String(30), nullable=False)
    Phone_number = db.Column(db.String(10), nullable=False)
    Email = db.Column(db.String(30), nullable=False)

    materials = db.relationship("Materials", backref="supplier", cascade="all, delete-orphan")

    def __init__(self, Supplier_ID, Supplier_Name, Phone_number, Email):
        self.Supplier_ID = Supplier_ID
        self.Supplier_Name = Supplier_Name
        self.Phone_number = Phone_number
        self.Email = Email

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Supplier {self.Supplier_ID}: {self.Supplier_Name}>"

class Materials(db.Model):
    __tablename__ = "Materials"
    Material_ID = db.Column(db.String(15), primary_key=True)
    Supplier_ID = db.Column(db.String(15), ForeignKey('Supplier.Supplier_ID'), nullable=False)
    Stock = db.Column(db.String(15), nullable=False)
    Name = db.Column(db.String(15), nullable=False)

    used_in_batches = db.relationship("MaterialUsed", backref="material", cascade="all, delete-orphan")

    def __init__(self, Material_ID, Supplier_ID, Stock, Name):
        self.Material_ID = Material_ID
        self.Supplier_ID = Supplier_ID
        self.Stock = Stock
        self.Name = Name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Material {self.Material_ID}: {self.Name}>"


class MaterialUsed(db.Model):
    __tablename__ = "Material_used"
    Material_ID = db.Column(db.String(15), ForeignKey('Materials.Material_ID'), primary_key=True)
    Garment_batch_ID = db.Column(db.String(15), ForeignKey('Garment_batch.Garment_batch_ID'), primary_key=True)
    Quantity_used = db.Column(db.String(30), nullable=False)

    def __init__(self, Material_ID, Garment_batch_ID, Quantity_used):
        self.Material_ID = Material_ID
        self.Garment_batch_ID = Garment_batch_ID
        self.Quantity_used = Quantity_used

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __repr__(self):
        return f"<MatUsed M:{self.Material_ID} B:{self.Garment_batch_ID}>"

   

from sqlalchemy import Column, Integer, String, Date, Enum, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    creator_name = Column(String(255), nullable=False)
    project_name = Column(String(255), nullable=False)
    current_stage = Column(Enum('CONCEPT', 'DESIGN', 'MODELING', 'PROTOTYPE', 'CONTRACT', 'PRODUCTION', 'LAUNCHED', 'COMPLETED', 'CANCELLED'), nullable=False)
    first_contact_date = Column(Date)
    first_response_date = Column(Date)
    last_contact_date = Column(Date)
    last_response_date = Column(Date)
    primary_communication_method = Column(String(50))

    communication = relationship("Communication", back_populates="project")
    design = relationship("Design", back_populates="project")
    modeling = relationship("Modeling", back_populates="project")
    prototype = relationship("Prototype", back_populates="project")
    product_pictures = relationship("ProductPictures", back_populates="project")
    contract = relationship("Contract", back_populates="project")
    tooling = relationship("Tooling", back_populates="project")
    launch = relationship("Launch", back_populates="project")
    production = relationship("Production", back_populates="project")
    packaging = relationship("Packaging", back_populates="project")
    customer_service = relationship("CustomerService", back_populates="project")
    freight = relationship("Freight", back_populates="project")
    shipping = relationship("Shipping", back_populates="project")

class Communication(Base):
    __tablename__ = 'communication'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    num_phone_calls = Column(Integer)
    num_messages_client = Column(Integer)
    num_messages_us = Column(Integer)
    response_time_max_client = Column(Integer)
    response_time_avg_client = Column(Integer)
    response_time_min_client = Column(Integer)
    response_time_max_us = Column(Integer)
    response_time_avg_us = Column(Integer)
    response_time_min_us = Column(Integer)
    files = relationship("File", back_populates="communication")
    project = relationship("Project", back_populates="communication")

class Design(Base):
    __tablename__ = 'design'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    artist = Column(String(255))
    files = relationship("File", back_populates="design")
    project = relationship("Project", back_populates="design")

class Modeling(Base):
    __tablename__ = 'modeling'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    artist = Column(String(255))
    files = relationship("File", back_populates="modeling")
    project = relationship("Project", back_populates="modeling")

class Prototype(Base):
    __tablename__ = 'prototype'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    num_exploded_pieces = Column(Integer)
    shipped_date = Column(Date)
    dimensions_height = Column(Float)
    dimensions_length = Column(Float)
    dimensions_depth = Column(Float)
    weight = Column(Float)
    files = relationship("File", back_populates="prototype")
    project = relationship("Project", back_populates="prototype")

class ProductPictures(Base):
    __tablename__ = 'product_pictures'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    files = relationship("File", back_populates="product_pictures")
    project = relationship("Project", back_populates="product_pictures")

class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    sent_date = Column(Date)
    signed_date = Column(Date)
    files = relationship("File", back_populates="contract")
    project = relationship("Project", back_populates="contract")

class Tooling(Base):
    __tablename__ = 'tooling'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    num_tools = Column(Integer)
    cost = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    files = relationship("File", back_populates="tooling")
    project = relationship("Project", back_populates="tooling")

class Production(Base):
    __tablename__ = 'production'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    files = relationship("File", back_populates="production")
    project = relationship("Project", back_populates="production")

class Launch(Base):
    __tablename__ = 'launch'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    units_sold = Column(Integer)
    retail_price = Column(Float)
    cash_collected = Column(Float)
    commission_paid = Column(Float)
    files = relationship("File", back_populates="launch", cascade="all, delete-orphan")
    project = relationship("Project", back_populates="launch")

class Packaging(Base):
    __tablename__ = 'packaging'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    artist = Column(String(255))
    files = relationship("File", back_populates="packaging")
    project = relationship("Project", back_populates="packaging")

class Freight(Base):
    __tablename__ = 'freight'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    freight_type = Column(String(50))
    cost = Column(Float)
    size = Column(String(50))
    weight = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    files = relationship("File", back_populates="freight")
    project = relationship("Project", back_populates="freight")

class CustomerService(Base):
    __tablename__ = 'customer_service'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    num_breakages = Column(Integer)
    num_refunds = Column(Integer)
    num_customer_service_messages = Column(Integer)
    files = relationship("File", back_populates="customer_service")
    project = relationship("Project", back_populates="customer_service")

class Shipping(Base):
    __tablename__ = 'shipping'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    avg_price = Column(Float)
    avg_cost = Column(Float)
    domestic_price = Column(Float)
    avg_international_price = Column(Float)
    avg_international_cost = Column(Float)
    files = relationship("File", back_populates="shipping")
    project = relationship("Project", back_populates="shipping")
    
class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    upload_date = Column(DateTime, nullable=False)
    file_type = Column(String(50))
    
    communication_id = Column(Integer, ForeignKey('communication.id'))
    design_id = Column(Integer, ForeignKey('design.id'))
    modeling_id = Column(Integer, ForeignKey('modeling.id'))
    prototype_id = Column(Integer, ForeignKey('prototype.id'))
    product_pictures_id = Column(Integer, ForeignKey('product_pictures.id'))
    contract_id = Column(Integer, ForeignKey('contract.id'))
    tooling_id = Column(Integer, ForeignKey('tooling.id'))
    launch_id = Column(Integer, ForeignKey('launch.id'))
    production_id = Column(Integer, ForeignKey('production.id'))
    packaging_id = Column(Integer, ForeignKey('packaging.id'))
    customer_service_id = Column(Integer, ForeignKey('customer_service.id'))
    freight_id = Column(Integer, ForeignKey('freight.id'))
    shipping_id = Column(Integer, ForeignKey('shipping.id'))

    communication = relationship("Communication", back_populates="files")
    design = relationship("Design", back_populates="files")
    modeling = relationship("Modeling", back_populates="files")
    prototype = relationship("Prototype", back_populates="files")
    product_pictures = relationship("ProductPictures", back_populates="files")
    contract = relationship("Contract", back_populates="files")
    tooling = relationship("Tooling", back_populates="files")
    launch = relationship("Launch", back_populates="files")
    production = relationship("Production", back_populates="files")
    packaging = relationship("Packaging", back_populates="files")
    customer_service = relationship("CustomerService", back_populates="files")
    freight = relationship("Freight", back_populates="files")
    shipping = relationship("Shipping", back_populates="files")
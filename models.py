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
    launch_type = Column(String(50))
    launch_start_date = Column(Date)
    launch_end_date = Column(Date)
    units_sold = Column(Integer)
    retail_price = Column(Float)
    cash_collected = Column(Float)
    commissions_paid = Column(Float)
    num_breakages = Column(Integer)
    num_refunds = Column(Integer)
    num_customer_service_messages = Column(Integer)

    communication = relationship("Communication", uselist=False, back_populates="project")
    design = relationship("Design", uselist=False, back_populates="project")
    modeling = relationship("Modeling", uselist=False, back_populates="project")
    prototype = relationship("Prototype", uselist=False, back_populates="project")
    product_pictures = relationship("ProductPictures", uselist=False, back_populates="project")
    contract = relationship("Contract", uselist=False, back_populates="project")
    mold = relationship("Mold", uselist=False, back_populates="project")
    production = relationship("Production", uselist=False, back_populates="project")
    packaging = relationship("Packaging", uselist=False, back_populates="project")
    freight = relationship("Freight", uselist=False, back_populates="project")
    shipping = relationship("Shipping", uselist=False, back_populates="project")
    attachments = relationship("Attachment", back_populates="project")

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
    project = relationship("Project", back_populates="communication")

class Design(Base):
    __tablename__ = 'design'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    project = relationship("Project", back_populates="design")

class Modeling(Base):
    __tablename__ = 'modeling'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    num_exploded_pieces = Column(Integer)
    project = relationship("Project", back_populates="modeling")

class Prototype(Base):
    __tablename__ = 'prototype'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    shipped_date = Column(Date)
    dimensions_height = Column(Float)
    dimensions_length = Column(Float)
    dimensions_depth = Column(Float)
    weight = Column(Float)
    project = relationship("Project", back_populates="prototype")

class ProductPictures(Base):
    __tablename__ = 'product_pictures'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    project = relationship("Project", back_populates="product_pictures")

class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    sent_date = Column(Date)
    signed_date = Column(Date)
    project = relationship("Project", back_populates="contract")

class Mold(Base):
    __tablename__ = 'mold'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    num_molds = Column(Integer)
    cost = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    project = relationship("Project", back_populates="mold")

class Production(Base):
    __tablename__ = 'production'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
    project = relationship("Project", back_populates="production")

class Packaging(Base):
    __tablename__ = 'packaging'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
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
    project = relationship("Project", back_populates="freight")

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
    project = relationship("Project", back_populates="shipping")

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    attachment_type = Column(Enum('CREATOR_LOGO', 'CONCEPT_IMAGE', 'DESIGN_IMAGE', '3D_MODEL_IMAGE', '3D_MODEL_LINK', 
                                  'PROTOTYPE_QUOTE', 'PROTOTYPE_IMAGE', 'EXPLODED_PROTOTYPE_IMAGE', 'PRODUCT_IMAGE', 
                                  'MOLD_QUOTE', 'PRODUCTION_QUOTE', 'CONTRACT', 'LAUNCH_VIDEO', 'OTHER'), nullable=False)
    file_name = Column(String(255))
    file_path = Column(String(255))
    file_type = Column(String(50))
    url = Column(String(255))
    description = Column(Text)
    upload_date = Column(DateTime)
    project = relationship("Project", back_populates="attachments")
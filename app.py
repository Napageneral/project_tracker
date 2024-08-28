from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, db_session
from models import Project, Communication, Design, Modeling, Prototype, ProductPictures, Contract, Mold, Production, Packaging, Freight, Shipping
from datetime import datetime
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.before_first_request
def initialize_database():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def dashboard():
    projects = Project.query.all()
    return render_template('dashboard.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/project/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        try:
            project = Project(
                creator_name=request.form['creator_name'],
                project_name=request.form['project_name'],
                current_stage=request.form['current_stage'],
                first_contact_date=datetime.strptime(request.form['first_contact_date'], '%Y-%m-%d').date() if request.form['first_contact_date'] else None,
                first_response_date=datetime.strptime(request.form['first_response_date'], '%Y-%m-%d').date() if request.form['first_response_date'] else None,
                last_contact_date=datetime.strptime(request.form['last_contact_date'], '%Y-%m-%d').date() if request.form['last_contact_date'] else None,
                last_response_date=datetime.strptime(request.form['last_response_date'], '%Y-%m-%d').date() if request.form['last_response_date'] else None,
                primary_communication_method=request.form['primary_communication_method'],
                launch_type=request.form['launch_type'],
                launch_start_date=datetime.strptime(request.form['launch_start_date'], '%Y-%m-%d').date() if request.form['launch_start_date'] else None,
                launch_end_date=datetime.strptime(request.form['launch_end_date'], '%Y-%m-%d').date() if request.form['launch_end_date'] else None,
                units_sold=int(request.form['units_sold']) if request.form['units_sold'] else None,
                retail_price=float(request.form['retail_price']) if request.form['retail_price'] else None,
                cash_collected=float(request.form['cash_collected']) if request.form['cash_collected'] else None,
                commissions_paid=float(request.form['commissions_paid']) if request.form['commissions_paid'] else None,
                num_breakages=int(request.form['num_breakages']) if request.form['num_breakages'] else None,
                num_refunds=int(request.form['num_refunds']) if request.form['num_refunds'] else None,
                num_customer_service_messages=int(request.form['num_customer_service_messages']) if request.form['num_customer_service_messages'] else None
            )
            db_session.add(project)
            db_session.flush()  # This assigns an id to the project

            communication = Communication(
                project_id=project.id,
                num_phone_calls=int(request.form['num_phone_calls']) if request.form['num_phone_calls'] else None,
                num_messages_client=int(request.form['num_messages_client']) if request.form['num_messages_client'] else None,
                num_messages_us=int(request.form['num_messages_us']) if request.form['num_messages_us'] else None,
                response_time_max_client=int(request.form['response_time_max_client']) if request.form['response_time_max_client'] else None,
                response_time_avg_client=int(request.form['response_time_avg_client']) if request.form['response_time_avg_client'] else None,
                response_time_min_client=int(request.form['response_time_min_client']) if request.form['response_time_min_client'] else None,
                response_time_max_us=int(request.form['response_time_max_us']) if request.form['response_time_max_us'] else None,
                response_time_avg_us=int(request.form['response_time_avg_us']) if request.form['response_time_avg_us'] else None,
                response_time_min_us=int(request.form['response_time_min_us']) if request.form['response_time_min_us'] else None
            )
            db_session.add(communication)

            design = Design(
                project_id=project.id,
                start_date=datetime.strptime(request.form['design_start_date'], '%Y-%m-%d').date() if request.form['design_start_date'] else None,
                end_date=datetime.strptime(request.form['design_end_date'], '%Y-%m-%d').date() if request.form['design_end_date'] else None,
                cost=float(request.form['design_cost']) if request.form['design_cost'] else None
            )
            db_session.add(design)

            modeling = Modeling(
                project_id=project.id,
                start_date=datetime.strptime(request.form['modeling_start_date'], '%Y-%m-%d').date() if request.form['modeling_start_date'] else None,
                end_date=datetime.strptime(request.form['modeling_end_date'], '%Y-%m-%d').date() if request.form['modeling_end_date'] else None,
                cost=float(request.form['modeling_cost']) if request.form['modeling_cost'] else None,
                num_exploded_pieces=int(request.form['num_exploded_pieces']) if request.form['num_exploded_pieces'] else None
            )
            db_session.add(modeling)

            prototype = Prototype(
                project_id=project.id,
                start_date=datetime.strptime(request.form['prototype_start_date'], '%Y-%m-%d').date() if request.form['prototype_start_date'] else None,
                end_date=datetime.strptime(request.form['prototype_end_date'], '%Y-%m-%d').date() if request.form['prototype_end_date'] else None,
                cost=float(request.form['prototype_cost']) if request.form['prototype_cost'] else None,
                shipped_date=datetime.strptime(request.form['prototype_shipped_date'], '%Y-%m-%d').date() if request.form['prototype_shipped_date'] else None,
                dimensions_height=float(request.form['prototype_dimensions_height']) if request.form['prototype_dimensions_height'] else None,
                dimensions_length=float(request.form['prototype_dimensions_length']) if request.form['prototype_dimensions_length'] else None,
                dimensions_depth=float(request.form['prototype_dimensions_depth']) if request.form['prototype_dimensions_depth'] else None,
                weight=float(request.form['prototype_weight']) if request.form['prototype_weight'] else None
            )
            db_session.add(prototype)

            product_pictures = ProductPictures(
                project_id=project.id,
                start_date=datetime.strptime(request.form['product_pictures_start_date'], '%Y-%m-%d').date() if request.form['product_pictures_start_date'] else None,
                end_date=datetime.strptime(request.form['product_pictures_end_date'], '%Y-%m-%d').date() if request.form['product_pictures_end_date'] else None,
                cost=float(request.form['product_pictures_cost']) if request.form['product_pictures_cost'] else None
            )
            db_session.add(product_pictures)

            contract = Contract(
                project_id=project.id,
                sent_date=datetime.strptime(request.form['contract_sent_date'], '%Y-%m-%d').date() if request.form['contract_sent_date'] else None,
                signed_date=datetime.strptime(request.form['contract_signed_date'], '%Y-%m-%d').date() if request.form['contract_signed_date'] else None
            )
            db_session.add(contract)

            mold = Mold(
                project_id=project.id,
                num_molds=int(request.form['mold_num_molds']) if request.form['mold_num_molds'] else None,
                cost=float(request.form['mold_cost']) if request.form['mold_cost'] else None,
                start_date=datetime.strptime(request.form['mold_start_date'], '%Y-%m-%d').date() if request.form['mold_start_date'] else None,
                end_date=datetime.strptime(request.form['mold_end_date'], '%Y-%m-%d').date() if request.form['mold_end_date'] else None
            )
            db_session.add(mold)

            production = Production(
                project_id=project.id,
                start_date=datetime.strptime(request.form['production_start_date'], '%Y-%m-%d').date() if request.form['production_start_date'] else None,
                end_date=datetime.strptime(request.form['production_end_date'], '%Y-%m-%d').date() if request.form['production_end_date'] else None,
                cost=float(request.form['production_cost']) if request.form['production_cost'] else None
            )
            db_session.add(production)

            packaging = Packaging(
                project_id=project.id,
                start_date=datetime.strptime(request.form['packaging_start_date'], '%Y-%m-%d').date() if request.form['packaging_start_date'] else None,
                end_date=datetime.strptime(request.form['packaging_end_date'], '%Y-%m-%d').date() if request.form['packaging_end_date'] else None,
                cost=float(request.form['packaging_cost']) if request.form['packaging_cost'] else None
            )
            db_session.add(packaging)

            freight = Freight(
                project_id=project.id,
                freight_type=request.form['freight_type'],
                cost=float(request.form['freight_cost']) if request.form['freight_cost'] else None,
                size=request.form['freight_size'],
                weight=float(request.form['freight_weight']) if request.form['freight_weight'] else None,
                start_date=datetime.strptime(request.form['freight_start_date'], '%Y-%m-%d').date() if request.form['freight_start_date'] else None,
                end_date=datetime.strptime(request.form['freight_end_date'], '%Y-%m-%d').date() if request.form['freight_end_date'] else None
            )
            db_session.add(freight)

            shipping = Shipping(
                project_id=project.id,
                start_date=datetime.strptime(request.form['shipping_start_date'], '%Y-%m-%d').date() if request.form['shipping_start_date'] else None,
                end_date=datetime.strptime(request.form['shipping_end_date'], '%Y-%m-%d').date() if request.form['shipping_end_date'] else None,
                avg_price=float(request.form['shipping_avg_price']) if request.form['shipping_avg_price'] else None,
                avg_cost=float(request.form['shipping_avg_cost']) if request.form['shipping_avg_cost'] else None,
                domestic_price=float(request.form['shipping_domestic_price']) if request.form['shipping_domestic_price'] else None,
                avg_international_price=float(request.form['shipping_avg_international_price']) if request.form['shipping_avg_international_price'] else None,
                avg_international_cost=float(request.form['shipping_avg_international_cost']) if request.form['shipping_avg_international_cost'] else None
            )
            db_session.add(shipping)

            db_session.commit()
            flash('New project created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error creating new project: {str(e)}")
            flash(f'Error creating new project: {str(e)}', 'error')
    return render_template('project_form.html')

@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        # Update main project details
        project.creator_name = request.form['creator_name']
        project.project_name = request.form['project_name']
        project.current_stage = request.form['current_stage']
        project.first_contact_date = datetime.strptime(request.form['first_contact_date'], '%Y-%m-%d').date() if request.form['first_contact_date'] else None
        project.first_response_date = datetime.strptime(request.form['first_response_date'], '%Y-%m-%d').date() if request.form['first_response_date'] else None
        project.last_contact_date = datetime.strptime(request.form['last_contact_date'], '%Y-%m-%d').date() if request.form['last_contact_date'] else None
        project.last_response_date = datetime.strptime(request.form['last_response_date'], '%Y-%m-%d').date() if request.form['last_response_date'] else None
        project.primary_communication_method = request.form['primary_communication_method']
        project.launch_type = request.form['launch_type']
        project.launch_start_date = datetime.strptime(request.form['launch_start_date'], '%Y-%m-%d').date() if request.form['launch_start_date'] else None
        project.launch_end_date = datetime.strptime(request.form['launch_end_date'], '%Y-%m-%d').date() if request.form['launch_end_date'] else None
        project.units_sold = int(request.form['units_sold']) if request.form['units_sold'] else None
        project.retail_price = float(request.form['retail_price']) if request.form['retail_price'] else None
        project.cash_collected = float(request.form['cash_collected']) if request.form['cash_collected'] else None
        project.commissions_paid = float(request.form['commissions_paid']) if request.form['commissions_paid'] else None
        project.num_breakages = int(request.form['num_breakages']) if request.form['num_breakages'] else None
        project.num_refunds = int(request.form['num_refunds']) if request.form['num_refunds'] else None
        project.num_customer_service_messages = int(request.form['num_customer_service_messages']) if request.form['num_customer_service_messages'] else None

        # Update or create related entities
        if project.communication:
            communication = project.communication
        else:
            communication = Communication(project_id=project.id)
            db_session.add(communication)
        
        communication.num_phone_calls = int(request.form['num_phone_calls']) if request.form['num_phone_calls'] else None
        communication.num_messages_client = int(request.form['num_messages_client']) if request.form['num_messages_client'] else None
        communication.num_messages_us = int(request.form['num_messages_us']) if request.form['num_messages_us'] else None
        communication.response_time_max_client = int(request.form['response_time_max_client']) if request.form['response_time_max_client'] else None
        communication.response_time_avg_client = int(request.form['response_time_avg_client']) if request.form['response_time_avg_client'] else None
        communication.response_time_min_client = int(request.form['response_time_min_client']) if request.form['response_time_min_client'] else None
        communication.response_time_max_us = int(request.form['response_time_max_us']) if request.form['response_time_max_us'] else None
        communication.response_time_avg_us = int(request.form['response_time_avg_us']) if request.form['response_time_avg_us'] else None
        communication.response_time_min_us = int(request.form['response_time_min_us']) if request.form['response_time_min_us'] else None

        if project.design:
            design = project.design
        else:
            design = Design(project_id=project.id)
            db_session.add(design)
        
        design.start_date = datetime.strptime(request.form['design_start_date'], '%Y-%m-%d').date() if request.form['design_start_date'] else None
        design.end_date = datetime.strptime(request.form['design_end_date'], '%Y-%m-%d').date() if request.form['design_end_date'] else None
        design.cost = float(request.form['design_cost']) if request.form['design_cost'] else None

        if project.modeling:
            modeling = project.modeling
        else:
            modeling = Modeling(project_id=project.id)
            db_session.add(modeling)
        
        modeling.start_date = datetime.strptime(request.form['modeling_start_date'], '%Y-%m-%d').date() if request.form['modeling_start_date'] else None
        modeling.end_date = datetime.strptime(request.form['modeling_end_date'], '%Y-%m-%d').date() if request.form['modeling_end_date'] else None
        modeling.cost = float(request.form['modeling_cost']) if request.form['modeling_cost'] else None
        modeling.num_exploded_pieces = int(request.form['num_exploded_pieces']) if request.form['num_exploded_pieces'] else None

        if project.prototype:
            prototype = project.prototype
        else:
            prototype = Prototype(project_id=project.id)
            db_session.add(prototype)
        
        prototype.start_date = datetime.strptime(request.form['prototype_start_date'], '%Y-%m-%d').date() if request.form['prototype_start_date'] else None
        prototype.end_date = datetime.strptime(request.form['prototype_end_date'], '%Y-%m-%d').date() if request.form['prototype_end_date'] else None
        prototype.cost = float(request.form['prototype_cost']) if request.form['prototype_cost'] else None
        prototype.shipped_date = datetime.strptime(request.form['prototype_shipped_date'], '%Y-%m-%d').date() if request.form['prototype_shipped_date'] else None
        prototype.dimensions_height = float(request.form['prototype_dimensions_height']) if request.form['prototype_dimensions_height'] else None
        prototype.dimensions_length = float(request.form['prototype_dimensions_length']) if request.form['prototype_dimensions_length'] else None
        prototype.dimensions_depth = float(request.form['prototype_dimensions_depth']) if request.form['prototype_dimensions_depth'] else None
        prototype.weight = float(request.form['prototype_weight']) if request.form['prototype_weight'] else None

        if project.product_pictures:
            product_pictures = project.product_pictures
        else:
            product_pictures = ProductPictures(project_id=project.id)
            db_session.add(product_pictures)
        
        product_pictures.start_date = datetime.strptime(request.form['product_pictures_start_date'], '%Y-%m-%d').date() if request.form['product_pictures_start_date'] else None
        product_pictures.end_date = datetime.strptime(request.form['product_pictures_end_date'], '%Y-%m-%d').date() if request.form['product_pictures_end_date'] else None
        product_pictures.cost = float(request.form['product_pictures_cost']) if request.form['product_pictures_cost'] else None

        if project.contract:
            contract = project.contract
        else:
            contract = Contract(project_id=project.id)
            db_session.add(contract)
        
        contract.sent_date = datetime.strptime(request.form['contract_sent_date'], '%Y-%m-%d').date() if request.form['contract_sent_date'] else None
        contract.signed_date = datetime.strptime(request.form['contract_signed_date'], '%Y-%m-%d').date() if request.form['contract_signed_date'] else None

        if project.mold:
            mold = project.mold
        else:
            mold = Mold(project_id=project.id)
            db_session.add(mold)
        
        mold.num_molds = int(request.form['mold_num_molds']) if request.form['mold_num_molds'] else None
        mold.cost = float(request.form['mold_cost']) if request.form['mold_cost'] else None
        mold.start_date = datetime.strptime(request.form['mold_start_date'], '%Y-%m-%d').date() if request.form['mold_start_date'] else None
        mold.end_date = datetime.strptime(request.form['mold_end_date'], '%Y-%m-%d').date() if request.form['mold_end_date'] else None

        if project.production:
            production = project.production
        else:
            production = Production(project_id=project.id)
            db_session.add(production)
        
        production.start_date = datetime.strptime(request.form['production_start_date'], '%Y-%m-%d').date() if request.form['production_start_date'] else None
        production.end_date = datetime.strptime(request.form['production_end_date'], '%Y-%m-%d').date() if request.form['production_end_date'] else None
        production.cost = float(request.form['production_cost']) if request.form['production_cost'] else None

        if project.packaging:
            packaging = project.packaging
        else:
            packaging = Packaging(project_id=project.id)
            db_session.add(packaging)
        
        packaging.start_date = datetime.strptime(request.form['packaging_start_date'], '%Y-%m-%d').date() if request.form['packaging_start_date'] else None
        packaging.end_date = datetime.strptime(request.form['packaging_end_date'], '%Y-%m-%d').date() if request.form['packaging_end_date'] else None
        packaging.cost = float(request.form['packaging_cost']) if request.form['packaging_cost'] else None

        if project.freight:
            freight = project.freight
        else:
            freight = Freight(project_id=project.id)
            db_session.add(freight)
        
        freight.freight_type = request.form['freight_type']
        freight.cost = float(request.form['freight_cost']) if request.form['freight_cost'] else None
        freight.size = request.form['freight_size']
        freight.weight = float(request.form['freight_weight']) if request.form['freight_weight'] else None
        freight.start_date = datetime.strptime(request.form['freight_start_date'], '%Y-%m-%d').date() if request.form['freight_start_date'] else None
        freight.end_date = datetime.strptime(request.form['freight_end_date'], '%Y-%m-%d').date() if request.form['freight_end_date'] else None

        if project.shipping:
            shipping = project.shipping
        else:
            shipping = Shipping(project_id=project.id)
            db_session.add(shipping)
        
        shipping.start_date = datetime.strptime(request.form['shipping_start_date'], '%Y-%m-%d').date() if request.form['shipping_start_date'] else None
        shipping.end_date = datetime.strptime(request.form['shipping_end_date'], '%Y-%m-%d').date() if request.form['shipping_end_date'] else None
        shipping.avg_price = float(request.form['shipping_avg_price']) if request.form['shipping_avg_price'] else None
        shipping.avg_cost = float(request.form['shipping_avg_cost']) if request.form['shipping_avg_cost'] else None
        shipping.domestic_price = float(request.form['shipping_domestic_price']) if request.form['shipping_domestic_price'] else None
        shipping.avg_international_price = float(request.form['shipping_avg_international_price']) if request.form['shipping_avg_international_price'] else None
        shipping.avg_international_cost = float(request.form['shipping_avg_international_cost']) if request.form['shipping_avg_international_cost'] else None

        db_session.commit()
        return redirect(url_for('project_detail', project_id=project.id))
    return render_template('project_form.html', project=project)

if __name__ == '__main__':
    app.run(debug=True)
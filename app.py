from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from database import init_db, db_session
from models import CustomerService, Launch, Project, Communication, Design, Modeling, Prototype, ProductPictures, Contract, Production, Packaging, Freight, Shipping, File, Tooling
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'your_secret_key_here'  # Set a secret key for flash messages

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_files(files, parent_id, parent_type):
    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            new_file = File(
                filename=filename,
                file_path=file_path,
                upload_date=datetime.now(),
                file_type=file.filename.rsplit('.', 1)[1].lower()
            )
            if parent_type == 'launch':
                new_file.launch_id = parent_id
            # Add other conditions for other parent types if needed
            saved_files.append(new_file)
    return saved_files

# Helper function to safely convert string to date
def safe_date(date_string):
    return safe_date(date_string, '%Y-%m-%d').date() if date_string else None

# Helper function to safely convert string to float
def safe_float(float_string):
    return safe_float(float_string) if float_string else None

# Helper function to safely convert string to int
def safe_int(int_string):
    returnsafe_int(int_string) if int_string else None

@app.before_first_request
def initialize_database():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(400)
def bad_request_error(error):
    logger.error(f"400 Error: {error}", exc_info=True)
    return 'Bad Request', 400

@app.errorhandler(Exception)
def unhandled_exception(e):
    logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
    return 'Internal Server Error', 500

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
        print("Form Data:")
        for key, value in request.form.items():
            print(f"{key}: {value}")
        
        print("Files:")
        for key, file in request.files.items():
            print(f"{key}: {file.filename}")

        try:
            logger.debug("Processing new project form submission")

            project = Project(
                creator_name=request.form['creator_name'],
                project_name=request.form['project_name'],
                current_stage=request.form['current_stage'],
                first_contact_date=safe_date(request.form['first_contact_date']),
                first_response_date=safe_date(request.form['first_response_date']),
                last_contact_date=safe_date(request.form['last_contact_date']),
                last_response_date=safe_date(request.form['last_response_date']),
                primary_communication_method=request.form['primary_communication_method'],
            )
            logger.debug("Project object created")

            db_session.add(project)
            db_session.flush()  # This assigns an id to the project
            logger.debug("Project object added")

            communication = Communication(
                project_id=project.id,
                num_phone_calls=safe_int(request.form['num_phone_calls']),
                num_messages_client=safe_int(request.form['num_messages_client']),
                num_messages_us=safe_int(request.form['num_messages_us']),
                response_time_max_client=safe_int(request.form['response_time_max_client']),
                response_time_avg_client=safe_int(request.form['response_time_avg_client']),
                response_time_min_client=safe_int(request.form['response_time_min_client']),
                response_time_max_us=safe_int(request.form['response_time_max_us']),
                response_time_avg_us=safe_int(request.form['response_time_avg_us']),
                response_time_min_us=safe_int(request.form['response_time_min_us'])
            )
            db_session.add(communication)
            logger.debug("Communication object added")
            communication.files = save_files(request.files.getlist('communication_files'), communication.id, 'communication')

            if project.current_stage == 'CONCEPT':
                design = Design(
                    project_id=project.id,
                    start_date=safe_date(request.form['design_start_date']),
                    end_date=safe_date(request.form['design_end_date']),
                    cost=safe_float(request.form['design_cost']),
                    artist=request.form['design_artist']
                )
                db_session.add(design)
                logger.debug("Design object added")
                design.files = save_files(request.files.getlist('design_files'), design.id, 'design')

            if project.current_stage == 'MODELING':
                modeling = Modeling(
                    project_id=project.id,
                    start_date=safe_date(request.form['modeling_start_date']),
                    end_date=safe_date(request.form['modeling_end_date']),
                    cost=safe_float(request.form['modeling_cost']),
                    artist=request.form['modeling_artist']
                )
                db_session.add(modeling)
                db_session.flush()
                modeling.files = save_files(request.files.getlist('modeling_files'), modeling.id, 'modeling')
                db_session.add_all(modeling.files)
                logger.debug("Modeling object added")

            if project.current_stage == 'PROTOTYPE':
                prototype = Prototype(
                    project_id=project.id,
                    start_date=safe_date(request.form['prototype_start_date']),
                    end_date=safe_date(request.form['prototype_end_date']),
                    cost=safe_float(request.form['prototype_cost']),
                    num_exploded_pieces=safe_int(request.form['num_exploded_pieces']),
                    shipped_date=safe_date(request.form['prototype_shipped_date']),
                    dimensions_height=safe_float(request.form['prototype_dimensions_height']),
                    dimensions_length=safe_float(request.form['prototype_dimensions_length']),
                    dimensions_depth=safe_float(request.form['prototype_dimensions_depth']),
                    weight=safe_float(request.form['prototype_weight']),
                )
                db_session.add(prototype)
                prototype.files = save_files(request.files.getlist('prototype_files'), prototype.id, 'prototype')
                logger.debug("Prototype object added")


            if project.current_stage == 'PROTOTYPE':
                product_pictures = ProductPictures(
                    project_id=project.id,
                    start_date=safe_date(request.form['product_pictures_start_date']),
                    end_date=safe_date(request.form['product_pictures_end_date']),
                    cost=safe_float(request.form['product_pictures_cost'])
                )
                db_session.add(product_pictures)
                product_pictures.files = save_files(request.files.getlist('product_pictures_files'), product_pictures.id, 'product_pictures')
                logger.debug("Product Pictures object added")

            if project.current_stage == 'CONTRACT':
                contract = Contract(
                    project_id=project.id,
                    sent_date=safe_date(request.form['contract_sent_date']),
                    signed_date=safe_date(request.form['contract_signed_date']),
                )
                db_session.add(contract)
                contract.files = save_files(request.files.getlist('contract_files'), contract.id, 'contract')
                logger.debug("Contract object added")

            if project.current_stage == 'CONTRACT':
                tooling = Tooling(
                    project_id=project.id,
                    num_tools=safe_int(request.form['tooling_num_tools']),
                    cost=safe_float(request.form['tooling_cost']),
                    start_date=safe_date(request.form['tooling_start_date']),
                    end_date=safe_date(request.form['tooling_end_date']),
                )
                db_session.add(tooling)
                db_session.flush()
                logger.debug("Tooling object added")
                tooling.files = save_files(request.files.getlist('tooling_files'), tooling.id, 'tooling')
            
            if project.current_stage == 'CONTRACT':
                production = Production(
                    project_id=project.id,
                    start_date=safe_date(request.form['production_start_date']),
                    end_date=safe_date(request.form['production_end_date']),
                    cost=safe_float(request.form['production_cost'])
                )
                db_session.add(production)
                production.files = save_files(request.files.getlist('production_files'), production.id, 'production')
                logger.debug("Production object added")

            if project.current_stage == 'PRODUCTION':
                packaging = Packaging(
                    project_id=project.id,
                    start_date=safe_date(request.form['packaging_start_date']),
                    end_date=safe_date(request.form['packaging_end_date']),
                    cost=safe_float(request.form['packaging_cost']),
                    artist=request.form['packaging_artist']
                )
                db_session.add(packaging)
                packaging.files = save_files(request.files.getlist('packaging_files'), packaging.id, 'packaging')
                logger.debug("Packaging object added")

            if project.current_stage == 'PRODUCTION':
                launch = Launch(
                    project_id=project.id,
                    start_date=safe_date(request.form['launch_start_date']),
                    end_date=safe_date(request.form['launch_end_date']),
                    units_sold=safe_int(request.form['units_sold']),
                    retail_price=safe_float(request.form['retail_price']),
                    cash_collected=safe_float(request.form['cash_collected']),
                    commission_paid=safe_float(request.form['commission_paid'])
                )
                db_session.add(launch)
                launch.files = save_files(request.files.getlist('launch_files'), launch.id, 'launch')
                logger.debug("Launch object added")

            if project.current_stage == 'LAUNCHED':
                customer_service = CustomerService(
                    project_id=project.id,
                    num_breakages=safe_int(request.form['num_breakages']),
                    num_refunds=safe_int(request.form['num_refunds']),
                    num_customer_service_messages=safe_int(request.form['num_customer_service_messages'])
                )
                db_session.add(customer_service)
                customer_service.files = save_files(request.files.getlist('customer_service_files'), customer_service.id, 'customer_service')
                logger.debug("Customer Service object added")

            if project.current_stage == 'LAUNCHED':
                freight = Freight(
                    project_id=project.id,
                    freight_type=request.form['freight_type'],
                    cost=safe_float(request.form['freight_cost']),
                    size=request.form['freight_size'],
                    weight=safe_float(request.form['freight_weight']),
                    start_date=safe_date(request.form['freight_start_date']),
                    end_date=safe_date(request.form['freight_end_date']),
                )
                db_session.add(freight)
                freight.files = save_files(request.files.getlist('freight_files'), freight.id, 'freight')
                logger.debug("Freight object added")

            if project.current_stage == 'LAUNCHED':
                shipping = Shipping(
                    project_id=project.id,
                    start_date=safe_date(request.form['shipping_start_date']),
                    end_date=safe_date(request.form['shipping_end_date']),
                    avg_price=safe_float(request.form['shipping_avg_price']),
                    avg_cost=safe_float(request.form['shipping_avg_cost']),
                    domestic_price=safe_float(request.form['shipping_domestic_price']),
                    avg_international_price=safe_float(request.form['shipping_avg_international_price']),
                    avg_international_cost=safe_float(request.form['shipping_avg_international_cost'])
                )
                db_session.add(shipping)
                shipping.files = save_files(request.files.getlist('shipping_files'), shipping.id, 'shipping')
                logger.debug("Shipping object added")

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
        project.current_stage = request.form['current_stage']
        project.first_contact_date = safe_date(request.form['first_contact_date']),
        project.first_response_date = safe_date(request.form['first_response_date']),
        project.last_contact_date = safe_date(request.form['last_contact_date']),
        project.last_response_date = safe_date(request.form['last_response_date']),
        project.primary_communication_method = request.form['primary_communication_method']
        project.launch_type = request.form['launch_type']
        project.launch_start_date = safe_date(request.form['launch_start_date'])
        project.launch_end_date = safe_date(request.form['launch_end_date'])
        project.units_sold =safe_int(request.form['units_sold'])
        project.retail_price = safe_float(request.form['retail_price'])
        project.cash_collected = safe_float(request.form['cash_collected'])
        project.commissions_paid = safe_float(request.form['commissions_paid'])
        project.num_breakages = safe_int(request.form['num_breakages'])
        project.num_refunds = safe_int(request.form['num_refunds'])
        project.num_customer_service_messages = safe_int(request.form['num_customer_service_messages'])

        # Update or create related entities
        if project.communication:
            communication = project.communication
        else:
            communication = Communication(project_id=project.id)
            db_session.add(communication)
        
        communication.num_phone_calls =safe_int(request.form['num_phone_calls'])
        communication.num_messages_client =safe_int(request.form['num_messages_client'])
        communication.num_messages_us =safe_int(request.form['num_messages_us'])
        communication.response_time_max_client =safe_int(request.form['response_time_max_client'])
        communication.response_time_avg_client =safe_int(request.form['response_time_avg_client'])
        communication.response_time_min_client =safe_int(request.form['response_time_min_client'])
        communication.response_time_max_us =safe_int(request.form['response_time_max_us'])
        communication.response_time_avg_us =safe_int(request.form['response_time_avg_us'])
        communication.response_time_min_us =safe_int(request.form['response_time_min_us'])

        if project.design:
            design = project.design
        else:
            design = Design(project_id=project.id)
            db_session.add(design)
        
        design.start_date = safe_date(request.form['design_start_date'])
        design.end_date = safe_date(request.form['design_end_date'])
        design.cost = safe_float(request.form['design_cost'])
        design.files.extend(save_files(request.files.getlist('design_files'), design.id, 'design'))

        if project.modeling:
            modeling = project.modeling
        else:
            modeling = Modeling(project_id=project.id)
            db_session.add(modeling)
        
        modeling.start_date = safe_date(request.form['modeling_start_date'])
        modeling.end_date = safe_date(request.form['modeling_end_date'])
        modeling.cost = safe_float(request.form['modeling_cost'])
        modeling.num_exploded_pieces = safe_int(request.form['num_exploded_pieces'])
        modeling.files.extend(save_files(request.files.getlist('modeling_files'), modeling.id, 'modeling'))

        if project.prototype:
            prototype = project.prototype
        else:
            prototype = Prototype(project_id=project.id)
            db_session.add(prototype)
        
        prototype.start_date = safe_date(request.form['prototype_start_date'])
        prototype.end_date = safe_date(request.form['prototype_end_date'])
        prototype.cost = safe_float(request.form['prototype_cost'])
        prototype.shipped_date = safe_date(request.form['prototype_shipped_date'])
        prototype.dimensions_height = safe_float(request.form['prototype_dimensions_height'])
        prototype.dimensions_length = safe_float(request.form['prototype_dimensions_length'])
        prototype.dimensions_depth = safe_float(request.form['prototype_dimensions_depth'])
        prototype.weight = safe_float(request.form['prototype_weight'])
        prototype.files.extend(save_files(request.files.getlist('prototype_files'), prototype.id, 'prototype'))

        if project.product_pictures:
            product_pictures = project.product_pictures
        else:
            product_pictures = ProductPictures(project_id=project.id)
            db_session.add(product_pictures)
        
        product_pictures.start_date = safe_date(request.form['product_pictures_start_date'])
        product_pictures.end_date = safe_date(request.form['product_pictures_end_date'])
        product_pictures.cost = safe_float(request.form['product_pictures_cost'])
        product_pictures.files.extend(save_files(request.files.getlist('product_pictures_files'), product_pictures.id, 'product_pictures'))

        if project.contract:
            contract = project.contract
        else:
            contract = Contract(project_id=project.id)
            db_session.add(contract)
        
        contract.sent_date = safe_date(request.form['contract_sent_date'])
        contract.signed_date = safe_date(request.form['contract_signed_date'])
        contract.files.extend(save_files(request.files.getlist('contract_files'), contract.id, 'contract'))

        if project.mold:
            mold = project.mold
        else:
            mold = Mold(project_id=project.id)
            db_session.add(mold)
        
        mold.num_molds = safe_int(request.form['num_molds'])
        mold.cost = safe_float(request.form['mold_cost'])
        mold.start_date = safe_date(request.form['mold_start_date'])
        mold.end_date = safe_date(request.form['mold_end_date'])
        mold.files.extend(save_files(request.files.getlist('mold_files'), mold.id, 'mold'))

        if project.production:
            production = project.production
        else:
            production = Production(project_id=project.id)
            db_session.add(production)
        
        production.start_date = safe_date(request.form['production_start_date'])
        production.end_date = safe_date(request.form['production_end_date'])
        production.cost = safe_float(request.form['production_cost'])
        production.files.extend(save_files(request.files.getlist('production_files'), production.id, 'production'))

        if project.packaging:
            packaging = project.packaging
        else:
            packaging = Packaging(project_id=project.id)
            db_session.add(packaging)
        
        packaging.start_date = safe_date(request.form['packaging_start_date'])
        packaging.end_date = safe_date(request.form['packaging_end_date'])
        packaging.cost = safe_float(request.form['packaging_cost'])
        packaging.files.extend(save_files(request.files.getlist('packaging_files'), packaging.id, 'packaging'))

        if project.freight:
            freight = project.freight
        else:
            freight = Freight(project_id=project.id)
            db_session.add(freight)
        
        freight.freight_type = request.form['freight_type']
        freight.cost = safe_float(request.form['freight_cost']) if request.form['freight_cost'] else None
        freight.size = request.form['freight_size']
        freight.weight = safe_float(request.form['freight_weight'])
        freight.start_date = safe_date(request.form['freight_start_date'])
        freight.end_date = safe_date(request.form['freight_end_date'])
        freight.files.extend(save_files(request.files.getlist('freight_files'), freight.id, 'freight'))

        if project.shipping:
            shipping = project.shipping
        else:
            shipping = Shipping(project_id=project.id)
            db_session.add(shipping)
        
        shipping.start_date = safe_date(request.form['shipping_start_date'])
        shipping.end_date = safe_date(request.form['shipping_end_date'])
        shipping.avg_price = safe_float(request.form['shipping_avg_price'])
        shipping.avg_cost = safe_float(request.form['shipping_avg_cost'])
        shipping.domestic_price = safe_float(request.form['shipping_domestic_price'])
        shipping.avg_international_price = safe_float(request.form['shipping_avg_international_price'])
        shipping.avg_international_cost = safe_float(request.form['shipping_avg_international_cost'])
        shipping.files.extend(save_files(request.files.getlist('shipping_files'), shipping.id, 'shipping'))
        
        db_session.commit()
        return redirect(url_for('project_detail', project_id=project.id))
    return render_template('project_form.html', project=project)

if __name__ == '__main__':
    app.run(debug=True)
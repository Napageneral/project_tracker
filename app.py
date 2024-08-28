from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, make_response
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
            if parent_type == 'design':
                new_file.design_id = parent_id
            elif parent_type == 'modeling':
                new_file.modeling_id = parent_id
            elif parent_type == 'prototype':
                new_file.prototype_id = parent_id
            elif parent_type == 'product_pictures':
                new_file.product_pictures_id = parent_id
            elif parent_type == 'contract':
                new_file.contract_id = parent_id
            elif parent_type == 'tooling':
                new_file.tooling_id = parent_id
            elif parent_type == 'production':
                new_file.production_id = parent_id
            elif parent_type == 'packaging':
                new_file.packaging_id = parent_id
            elif parent_type == 'launch':
                new_file.launch_id = parent_id
            
            saved_files.append(new_file)
    return saved_files

def get_project_or_404(project_id):
    project = Project.query.get(project_id)
    if project is None:
        abort(404, description="Project not found")
    return project

def safe_date(date_string):
    if date_string:
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None

def safe_float(float_string):
    if float_string:
        try:
            return float(float_string)
        except ValueError:
            return None
    return None

def safe_int(int_string):
    if int_string:
        try:
            return int(int_string)
        except ValueError:
            return None
    return None

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

@app.route('/favicon.ico')
def favicon():
    return make_response('', 204)

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



            product_pictures = ProductPictures(
                project_id=project.id,
                start_date=safe_date(request.form['product_pictures_start_date']),
                end_date=safe_date(request.form['product_pictures_end_date']),
                cost=safe_float(request.form['product_pictures_cost'])
            )
            db_session.add(product_pictures)
            product_pictures.files = save_files(request.files.getlist('product_pictures_files'), product_pictures.id, 'product_pictures')
            logger.debug("Product Pictures object added")


            contract = Contract(
                project_id=project.id,
                sent_date=safe_date(request.form['contract_sent_date']),
                signed_date=safe_date(request.form['contract_signed_date']),
            )
            db_session.add(contract)
            contract.files = save_files(request.files.getlist('contract_files'), contract.id, 'contract')
            logger.debug("Contract object added")


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
        

            production = Production(
                project_id=project.id,
                start_date=safe_date(request.form['production_start_date']),
                end_date=safe_date(request.form['production_end_date']),
                cost=safe_float(request.form['production_cost'])
            )
            db_session.add(production)
            production.files = save_files(request.files.getlist('production_files'), production.id, 'production')
            logger.debug("Production object added")


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


            customer_service = CustomerService(
                project_id=project.id,
                num_breakages=safe_int(request.form['num_breakages']),
                num_refunds=safe_int(request.form['num_refunds']),
                num_customer_service_messages=safe_int(request.form['num_customer_service_messages'])
            )
            db_session.add(customer_service)
            customer_service.files = save_files(request.files.getlist('customer_service_files'), customer_service.id, 'customer_service')
            logger.debug("Customer Service object added")


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
    project = get_project_or_404(project_id)

    # Explicitly fetch all related objects
    communication = Communication.query.filter_by(project_id=project_id).first()
    design = Design.query.filter_by(project_id=project_id).first()
    modeling = Modeling.query.filter_by(project_id=project_id).first()
    prototype = Prototype.query.filter_by(project_id=project_id).first()
    product_pictures = ProductPictures.query.filter_by(project_id=project_id).first()
    contract = Contract.query.filter_by(project_id=project_id).first()
    tooling = Tooling.query.filter_by(project_id=project_id).first()
    production = Production.query.filter_by(project_id=project_id).first()
    packaging = Packaging.query.filter_by(project_id=project_id).first()
    launch = Launch.query.filter_by(project_id=project_id).first()
    customer_service = CustomerService.query.filter_by(project_id=project_id).first()
    freight = Freight.query.filter_by(project_id=project_id).first()
    shipping = Shipping.query.filter_by(project_id=project_id).first()

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
        design.artist = request.form['design_artist']

        new_files = save_files(request.files.getlist('design_files'), design.id, 'design')
        for file in new_files:
            db_session.add(file)


        if project.modeling:
            modeling = project.modeling
        else:
            modeling = Modeling(project_id=project.id)
            db_session.add(modeling)
        
        modeling.start_date = safe_date(request.form['modeling_start_date'])
        modeling.end_date = safe_date(request.form['modeling_end_date'])
        modeling.cost = safe_float(request.form['modeling_cost'])
        modeling.artist = request.form['modeling_artist']
        modeling.num_exploded_pieces = safe_int(request.form['num_exploded_pieces'])
        
        new_files = save_files(request.files.getlist('modeling_files'), modeling.id, 'modeling')
        for file in new_files:
            db_session.add(file)

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
        new_files = save_files(request.files.getlist('prototype_files'), prototype.id, 'prototype')
        for file in new_files:
            db_session.add(file)

        if project.product_pictures:
            product_pictures = project.product_pictures
        else:
            product_pictures = ProductPictures(project_id=project.id)
            db_session.add(product_pictures)
        
        product_pictures.start_date = safe_date(request.form['product_pictures_start_date'])
        product_pictures.end_date = safe_date(request.form['product_pictures_end_date'])
        product_pictures.cost = safe_float(request.form['product_pictures_cost'])
        new_files = save_files(request.files.getlist('product_pictures_files'), product_pictures.id, 'product_pictures')
        for file in new_files:
            db_session.add(file)

        if project.contract:
            contract = project.contract
        else:
            contract = Contract(project_id=project.id)
            db_session.add(contract)
        
        contract.sent_date = safe_date(request.form['contract_sent_date'])
        contract.signed_date = safe_date(request.form['contract_signed_date'])
        new_files = save_files(request.files.getlist('contract_files'), contract.id, 'contract')
        for file in new_files:
            db_session.add(file)

        if project.launch:
            launch = project.launch
        else:
            launch = Launch(project_id=project.id)
            db_session.add(launch)
        
        launch.start_date = safe_date(request.form['launch_start_date'])
        launch.end_date = safe_date(request.form['launch_end_date'])
        launch.units_sold = safe_int(request.form['units_sold'])
        launch.retail_price = safe_float(request.form['retail_price'])
        launch.cash_collected = safe_float(request.form['cash_collected'])
        launch.commission_paid = safe_float(request.form['commission_paid'])
        new_files = save_files(request.files.getlist('launch_files'), launch.id, 'launch')
        for file in new_files:
            db_session.add(file)

        if project.tooling:
            tooling = project.tooling
        else:
            tooling = Tooling(project_id=project.id)
            db_session.add(tooling)
        
        tooling.num_tools = safe_int(request.form['num_tools'])
        tooling.cost = safe_float(request.form['tooling_cost'])
        tooling.start_date = safe_date(request.form['tooling_start_date'])
        tooling.end_date = safe_date(request.form['tooling_end_date'])
        new_files = save_files(request.files.getlist('tooling_files'), tooling.id, 'tooling')
        for file in new_files:
            db_session.add(file)

        if project.production:
            production = project.production
        else:
            production = Production(project_id=project.id)
            db_session.add(production)
        
        production.start_date = safe_date(request.form['production_start_date'])
        production.end_date = safe_date(request.form['production_end_date'])
        production.cost = safe_float(request.form['production_cost'])
        new_files = save_files(request.files.getlist('production_files'), production.id, 'production')
        for file in new_files:
            db_session.add(file)

        if project.packaging:
            packaging = project.packaging
        else:
            packaging = Packaging(project_id=project.id)
            db_session.add(packaging)
        
        packaging.start_date = safe_date(request.form['packaging_start_date'])
        packaging.end_date = safe_date(request.form['packaging_end_date'])
        packaging.cost = safe_float(request.form['packaging_cost'])
        new_files = save_files(request.files.getlist('packaging_files'), packaging.id, 'packaging')
        for file in new_files:
            db_session.add(file)

        if project.customer_service:
            customer_service = project.customer_service
        else:
            customer_service = CustomerService(project_id=project.id)
            db_session.add(customer_service)
        
        customer_service.num_breakages = safe_int(request.form['num_breakages'])
        customer_service.num_refunds = safe_int(request.form['num_refunds'])
        customer_service.num_customer_service_messages = safe_int(request.form['num_customer_service_messages'])
        new_files = save_files(request.files.getlist('customer_service_files'), customer_service.id, 'customer_service')
        for file in new_files:
            db_session.add(file)

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
        new_files = save_files(request.files.getlist('freight_files'), freight.id, 'freight')
        for file in new_files:
            db_session.add(file)

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
        new_files = save_files(request.files.getlist('shipping_files'), shipping.id, 'shipping')
        for file in new_files:
            db_session.add(file)
        
        db_session.commit()
        return redirect(url_for('project_detail', project_id=project.id))
    return render_template('project_form.html', 
                           project=project,
                           communication=communication,
                           design=design,
                           modeling=modeling,
                           prototype=prototype,
                           product_pictures=product_pictures,
                           contract=contract,
                           tooling=tooling,
                           production=production,
                           packaging=packaging,
                           launch=launch,
                           customer_service=customer_service,
                           freight=freight,
                           shipping=shipping)

@app.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    try:
        project = get_project_or_404(project_id)
        
        # Manually delete associated files and records
        associated_models = [
            (Communication, 'communication_id'),
            (Design, 'design_id'),
            (Modeling, 'modeling_id'),
            (Prototype, 'prototype_id'),
            (ProductPictures, 'product_pictures_id'),
            (Contract, 'contract_id'),
            (Tooling, 'tooling_id'),
            (Production, 'production_id'),
            (Packaging, 'packaging_id'),
            (Launch, 'launch_id'),
            (CustomerService, 'customer_service_id'),
            (Freight, 'freight_id'),
            (Shipping, 'shipping_id')
        ]

        for model, id_column in associated_models:
            associated_record = model.query.filter_by(project_id=project_id).first()
            if associated_record:
                # Delete associated files
                associated_files = File.query.filter_by(**{id_column: associated_record.id}).all()
                for file in associated_files:
                    if os.path.exists(file.file_path):
                        os.remove(file.file_path)
                    db_session.delete(file)
                
                # Delete the associated record
                db_session.delete(associated_record)

        # Delete the project
        db_session.delete(project)
        db_session.commit()
        
        return jsonify({"success": True, "message": "Project deleted successfully"}), 200
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error deleting project: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
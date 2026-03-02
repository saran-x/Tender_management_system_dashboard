from flask import Flask,render_template,redirect,url_for,request,flash
import os
from pymongo import MongoClient
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
password=os.environ.get('mongo_db_password')
connection_db=f"mongodb+srv://saranrajtsaranrajt27:{password}""@saran.kz45sjy.mongodb.net/?retryWrites=true&w=majority&appName=saran"
client=MongoClient(connection_db)
tendor_db=client.tendor
v_detail=tendor_db.vendor #vendors db
t_detail=tendor_db.tendor_place #tender details
client.close()
app = Flask(__name__)
#secreatkey
app.secret_key='12345'
#main page
@app.route("/")
def home():
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    #last 3 or recent tendor details
    t_detail=tendor_db.tendor_place #tender details
    list_tender=t_detail.find().sort('_id',-1).limit(3)
    recent_tender=list(list_tender)
    #count tender Active
    counts=t_detail.count_documents({'status':'Published'})
    #total vendor
    v_detail=tendor_db.vendor 
    counts_vendor=v_detail.count_documents(filter={})
    #total pending tender
    pending=v_detail.count_documents({'status':'PENDING'})
    #month calculation
    return render_template("home.html",result_recent_tender=recent_tender,counts_Publish=counts,result_v_counts=counts_vendor,result_pending=pending)
#add tendor details
@app.route('/new_tender',methods=['POST','GET'])
def new_tender():
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    t_detail=tendor_db.tendor_place 
    try:
        if request.method == 'POST':
            tender_id=request.form['tender_id']
            referenceNo=request.form['reference_no']
            title=request.form['title']
            description=request.form['description']
            category=request.form['category']
            status=request.form['status']
            budget=request.form['budget']
            currency=request.form['currency']
            deadline=request.form['deadline']
            published_date=request.form['timeline.published_date']
            bid_opening_date=request.form['timeline.bid_opening_date']
            bid_closing_date=request.form['timeline.bid_closing_date']
            evaluation_period_days=request.form['timeline.evaluation_period_days']
            expected_award_date=request.form['timeline.expected_award_date']
            project_start_date=request.form['timeline.project_start_date']
            project_duration_days=request.form['timeline.project_duration_days']
            tender_type=request.form['additional_info.tender_type']
            evaluation_method=request.form['additional_info.evaluation_method']
            bid_bond_required=request.form['additional_info.bid_bond_required']
            bid_bond_amount=request.form['additional_info.bid_bond_amount']
            performance_bond_required=request.form['additional_info.performance_bond_required']
            performance_bond_percentage=request.form['additional_info.performance_bond_percentage']
            views=request.form['statistics.views']
            downloads=request.form['statistics.downloads']
            clarifications_requested=request.form['statistics.clarifications_requested']
            bids_received=request.form['statistics.bids_received']
            days_remaining=request.form['statistics.days_remaining']
            v_docs={
                'tender_id':tender_id,
                'reference_no':referenceNo,
                'title':title,
                'description':description,
                'category':category,
                'status':status,
                'budget':budget,
                'currency':currency,
                'deadline':deadline,
                'timeline':{
                    'published_date':published_date,
                    'bid_opening_date':bid_opening_date,
                    'bid_closing_date':bid_closing_date,
                    'evaluation_period_days':evaluation_period_days,
                    'expected_award_date':expected_award_date,
                    'project_start_date':project_start_date,
                    'project_duration_days':project_duration_days
                },
                'additional_info':{
                    'tender_type':tender_type,
                    'evaluation_method':evaluation_method,
                    'bid_bond_required':bid_bond_required,
                    'bid_bond_amount':bid_bond_amount,
                    'performance_bond_required':performance_bond_required,
                    'performance_bond_percentage':performance_bond_percentage
                },
                'statistics':{
                    'views':views,
                    'downloads':downloads,
                    'clarifications_requested':clarifications_requested,
                    'bids_received':bids_received,
                    'days_remaining':days_remaining
                }
            }
            t_detail.insert_one(v_docs)
            flash('successfully create a tender details','success')
            return redirect(url_for('tendor'))
    except:
        flash('please fill the correct way','danger')
        return redirect(url_for('new_tender'))
    return render_template("add_tendor.html")
#tendor page
@app.route("/tendor")
def tendor():
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    t_detail=tendor_db.tendor_place 
    tendor_result=t_detail.find()
    return render_template('tender.html',tendor_results=tendor_result)
#edit tender page
@app.route('/edit_tendor/<string:id>',methods=['POST','GET'])
def edit_tendor(id):
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    t_detail=tendor_db.tendor_place 
    from bson.objectid import ObjectId
    _id=ObjectId(id)
    tender_person=t_detail.find_one({'_id':_id})
    if request.method == 'POST':
        Tender_id=request.form['tender_id']
        Tender_Title=request.form['title']
        Category=request.form['category']
        Estimated_Budget=request.form['budget']
        Reference_Number=request.form['reference_no']
        Status=request.form['status']
        Currency=request.form['currency']
        Published_Date=request.form['timeline.published_date']
        Expected_Award_Date=request.form['timeline.expected_award_date']
        Bid_Opening_Date=request.form['timeline.bid_opening_date']
        Project_Start_Date=request.form['timeline.project_start_date']
        Bid_Closing_Date=request.form['timeline.bid_closing_date']
        ProjectDuration=request.form['timeline.project_duration_days']
        Tender_Type=request.form['additional_info.tender_type']
        Evaluation_Method=request.form['additional_info.evaluation_method']
        Bid_Bond_Required=request.form['additional_info.bid_bond_required']
        Performance_Bond_Required=request.form['additional_info.performance_bond_required']
        Bid_Bond_Amount=request.form['additional_info.bid_bond_amount']
        Performance_Bond=request.form['additional_info.performance_bond_percentage']
        docs_tender={
            'tender_id':Tender_id,
            'reference_no':Reference_Number,
            'title':Tender_Title,
            'category':Category,
            'budget':Estimated_Budget,
            'status':Status,
            'currency':Currency,
            'timeline':{
                'published_date':Published_Date,
                'expected_award_date':Expected_Award_Date,
                'bid_opening_date':Bid_Opening_Date,
                'project_start_date':Project_Start_Date,
                'bid_closing_date':Bid_Closing_Date,
                'project_duration_days':ProjectDuration,
            },
            'additional_info':{
                'tender_type':Tender_Type,
                'evaluation_method':Evaluation_Method,
                'bid_bond_required':Bid_Bond_Required,
                'performance_bond_required':Performance_Bond_Required,
                'bid_bond_amount':Bid_Bond_Amount,
                'performance_bond_percentage':Performance_Bond
            }
        }
        t_detail.update_one({'_id':_id},{'$set':docs_tender})
        return redirect(url_for('tendor'))
    return render_template('edit_tender.html',tender_persons=tender_person)
#vendor page
@app.route('/vendor')
def vendor():
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    v_detail=tendor_db.vendor
    results=v_detail.find()
    return render_template('vendor.html',result=results)
#edit vendor page
@app.route('/edit_vendor/<string:id>',methods=['POST','GET'])
def edit_vendor(id):
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    v_detail=tendor_db.vendor
    from bson.objectid import ObjectId
    _id=ObjectId(id)
    perticular_vendor=v_detail.find_one({'_id':_id})
    if request.method == 'POST':
        company_name=request.form['company_name']
        Contact_Person =request.form['contact_person']
        Email_Address =request.form["email"]
        Phone_Number=request.form["phone"]
        Category=request.form["category"]
        Status=request.form["status"]
        Street_Address=request.form["address.street"]
        City=request.form["address.city"]
        State=request.form["address.state"]
        ZIP_Code=request.form["address.zip_code"]
        Country=request.form["address.country"]
        docs={
            'company_name':company_name,
            'contact_person':Contact_Person,
            'email':Email_Address,
            'phone':Phone_Number,
            'category':Category,
            'status':Status,
            'address':
                {
                'street':Street_Address,
                'city':City,
                'state':State,
                'zip_code':ZIP_Code,
                'country':Country
                }
        
        }
        v_detail.update_one({'_id':_id},{'$set': docs})
        return redirect(url_for('vendor'))
    return render_template('edit_vendor.html',person_detail=perticular_vendor)
#report page
@app.route('/report_tender')
def report_tender():
    client=MongoClient(connection_db)
    tendor_db=client.tendor
    v_detail=tendor_db.vendor #vendors db
    t_detail=tendor_db.tendor_place
    #total tender
    counts=t_detail.count_documents(filter={})
    #active vendor
    v_active=v_detail.count_documents({'status':'ACTIVE'})
    return render_template('report_tender.html',counters=counts,v_actives=v_active)
#contract page
@app.route('/contract')
def contract():
    return render_template('contract.html')
if __name__ == "__main__":
    app.run(debug=True)
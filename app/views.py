import json 
import logging
from sqlalchemy import insert
from flask import render_template, flash, request, redirect, url_for, session, jsonify
from app import app, db, models
from .forms import LoginForm, SignupForm, ApplianceForm, ApplianceEditForm, TargetForm, ProviderForm, UserEditForm, ProfileForm, AdminPasscodeForm
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime # to get current time
from .calulateApp import calculateAll, calculateSum
from .chatbot import chatbot
from flask_share import Share
share = Share(app)

# logging
logger = logging.getLogger(__name__)
logger.info("index route request")


# flask-login, taken from previous coursework
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    # get user from user id
    return models.User.query.get(user_id)




# PAGES #

# HOME

@app.route("/",methods=["GET", "POST"])
def home():
    return render_template('home.html', title="Welcome")


@app.route("/usage", methods=["GET", "POST"])
@login_required
def usage():
    userUseage = models.Usage.query.filter_by(email=current_user.email).first()
        
    if userUseage:
        energy_consumed = usage.energyConsumed
        cost = usage.cost
        carbon_emissions = usage.carbonEmissions

        return render_template('usage.html', energy_consumed=energy_consumed, cost=cost, carbon_emissions=carbon_emissions, title="Usage")
    else:
        flash('No appliance usage data found for the logged-in user.', 'warning')
        return redirect(url_for('your_appliances'))


# AUTHENTICATION
# login/logout, sign up is inspired by previous coursework
# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    # get form data
    form = LoginForm()
    # received form data
    if form.validate_on_submit():
        # get the user from their email
        user = models.User.query.filter_by(email=form.email.data).first()
        # check if user with the email inputted exists and password is correct
        if user and check_password_hash(user.passwordHash, form.password.data):
            session["logged_in"] = True
            session["email"] = user.email
            login_user(user)
            flash("Successfully logged in!", "success")
            return redirect(url_for("usage"))
        else:
            flash("Incorrect Username or password", "warning")
    # on get method
    return render_template("login.html", form=form, title="Login")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home"))


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # check if user already exists
        userExists = models.User.query.filter_by(email=form.email.data).all()
        providerOption = form.provider.data
        if not userExists:
            newUser = models.User(
                name=form.name.data,
                email=form.email.data,
                postcode=form.postcode.data,
                provider=form.provider.data,
                passwordHash=generate_password_hash(form.password.data),
                dateCreated=datetime.now()
            )

            # add to database and commit
            db.session().add(newUser)
            db.session().commit()

            if (providerOption == "Other"):
                # pass user's email to add provider name in addProvider.
                return redirect(url_for("addProvider", userEmail = form.email.data))
            else:
                # add to database and commit
                db.session().add(newUser)
                db.session().commit()
                flash("Account created successfully!", "success")
                return redirect(url_for("login"))
        else:
            flash("Email has already been used!", "warning")
    return render_template("signup.html", form=form, title="Sign Up")

# add provider
@app.route("/addProvider", methods=["GET", "POST"])
def addProvider():
    form = ProviderForm()
    if form.validate_on_submit():
        newSupplier = models.Provider (
            energyProvider=form.providerName.data,
            tariff=form.providerTariff.data
        )

        # add to database and commit
        db.session().add(newSupplier)
        db.session().commit()

        # change provider name in the user's struct.
        user = models.User.query.filter_by(email=request.args["userEmail"]).first()
        user.provider = form.providerName.data
        db.session().commit()         


        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("addProvider.html", form=form, title="Add provider")
# show calculator
@app.route("/calculator", methods=["GET", "POST"])
@login_required
def calculator():
    appliances = models.Appliance.query.all()
    return render_template("calculator.html", appliances=appliances, title="Calculator")


# show suggestions
@app.route("/suggestions", methods=["GET", "POST"])
@login_required
def suggestions():
    return render_template("suggestions.html")

# show addAppliance
@app.route("/addAppliance", methods=["GET", "POST"])
@login_required
def addAppliance():
    form = ApplianceForm()
    # returns true when a button is pressed
    if form.validate_on_submit(): 
        # checks which button is pressed
        if "addButton" in request.form:
            # Get provider tariff and insert into calculations
            provider_name = current_user.provider
            tariff = models.Provider.query.filter_by(energyProvider=provider_name).first().tariff
            
            # Calculate relevant data. 
            results = calculateAll(form.watts.data, form.hoursPerDay.data, tariff, current_user.postcode)

            newAppliance = models.Appliance(
                email = current_user.email,
                applianceName = form.applianceName.data, 
                powerRating = form.watts.data, 
                hoursPerDay=form.hoursPerDay.data,
                dateUsedOn = datetime.now().date(), #Returns the date only 
                cost = results[1],
                emissions = results[2],
                energyUsed = results[0]
                )
            db.session().add(newAppliance)
            db.session().commit()
            flash("Successfully added an appliance!", "success")
            userEntries = models.Appliance.query.filter_by(email=current_user.email).all()

            if not userEntries: # i.e. no appliance in the database associated to the user
                flash("Please add an appliance", "warning")
            else:
                results = calculateSum(userEntries)
                entryExists = models.Usage.query.filter_by(email=current_user.email).all()

                usageResults = calculateSum(userEntries)
                entryExists = models.Usage.query.filter_by(email=current_user.email).all()

                if not entryExists:
                    # Create a new entry with the calculated results.
                    newUsageEntry = models.Usage(
                        email = current_user.email,
                        energyConsumed = results[0], 
                        cost = results[1],
                        carbonEmissions = results[2]
                    )
                    db.session().add(newUsageEntry)
                    db.session().commit()
            
                else:
                    # find the entry and override the calculated results on to it.
                    existingEntry = models.Usage.query.filter_by(email=current_user.email).first()
                    existingEntry.energyConsumed = usageResults[0]
                    existingEntry.cost = usageResults[1]
                    existingEntry.carbonEmissions = usageResults[2]   
                db.session().commit()
                return redirect(url_for("addAppliance")) # refresh so it resets form fields.

        elif "calButton" in request.form:
            # When pressing the calculate button, it will take all your appliances and sum it all up, overriding the variables in Usage.
            userEntries = models.Appliance.query.filter_by(email=current_user.email).all()

            if not userEntries: # i.e. no appliance in the database associated to the user
                flash("Please add an appliance", "warning")
            else:
                results = calculateSum(userEntries)
                entryExists = models.Usage.query.filter_by(email=current_user.email).all()

                if not entryExists:
                # Create a new entry with the calculated results.
                    newUsageEntry = models.Usage(
                        email = current_user.email,
                        energyConsumed = results[0], 
                        cost = results[1],
                        carbonEmissions = results[2]
                    )
                    db.session().add(newUsageEntry)
                else:
                    # find the entry and override the calculated results on to it.
                    existingEntry = models.Usage.query.filter_by(email=current_user.email).first()
                    existingEntry.energyConsumed = results[0]
                    existingEntry.cost = results[1]
                    existingEntry.carbonEmissions = results[2]
                db.session.commit()    
                return redirect(url_for("usage")) 

    return render_template("appliance.html", form=form, title="Appliances")

# show your appliances
@app.route("/your_appliances", methods=["GET", "POST"])
@login_required
def your_appliances():
    form = ApplianceEditForm()
    appliances = models.Appliance.query.filter_by(User=current_user)
    return render_template("your_appliances.html", title="Your Appliances", appliances=appliances, form=form)


# show goals
@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():

    # get goal data and set.
    form = TargetForm()
    if form.validate_on_submit():
        current_user.costTarget = form.costTarget.data
        current_user.energyTarget = form.energyTarget.data
        current_user.emissionTarget = form.emissionTarget.data
        db.session.commit()
    
    userUseage = models.Usage.query.filter_by(email=current_user.email).first()
    if userUseage:
        emGoal = current_user.emissionTarget
        costGoal = current_user.costTarget
        energyGoal = current_user.energyTarget
        
        # Retrieve from the usage table. 
        user = models.Usage.query.filter_by(email=current_user.email).first()
        emCurrent = user.carbonEmissions
        energyCurrent = user.energyConsumed
        costCurrent = user.cost

        # Error check for division by zero
        energyPercent = round(energyCurrent/energyGoal * 100) if energyGoal else 0
        costPercent = round(costCurrent/costGoal * 100) if costGoal else 0
        emPercent = round(emCurrent/emGoal * 100) if emGoal else 0 
        
        # Round to three decimal place, easier to read for users.
        emCurrent = round(emCurrent, 3) 
        energyCurrent = round(energyCurrent, 3) 
        costCurrent = round(costCurrent, 3) 

        
         
        #if statement for energy, assign text based on percent
        if (energyPercent > 100):
            prompt = models.Prompt.query.filter_by(id=2).first()
            energyText = prompt.message
        elif (energyPercent > 50 and energyPercent < 100):
            prompt = models.Prompt.query.filter_by(id=1).first()
            energyText = prompt.message
        elif (energyPercent <= 50):
            prompt = models.Prompt.query.filter_by(id=0).first()
            energyText = prompt.message
        
        #if statement for em, assign text based on percent
        if (emPercent > 100):
            prompt = models.Prompt.query.filter_by(id=5).first()
            emText = prompt.message
        elif (emPercent > 50 and energyPercent < 100):
            prompt = models.Prompt.query.filter_by(id=4).first()
            emText = prompt.message
        elif (emPercent <= 50):
            prompt = models.Prompt.query.filter_by(id=3).first()
            emText = prompt.message

        #if statement for cost, assign text based on percent
        if (costPercent > 100):
            prompt = models.Prompt.query.filter_by(id=8).first()
            emText = prompt.message
        elif (costPercent > 50 and energyPercent < 100):
            prompt = models.Prompt.query.filter_by(id=7).first()
            costText = prompt.message
        elif (costPercent <= 50):
            prompt = models.Prompt.query.filter_by(id=6).first()
            costText = prompt.message
        
        #If goals are 0, goals are not set, change the text.
        if energyGoal==0: energyText = "Input an energy goal to start tracking your energy usage!" 
        if emGoal==0: emText = "Input an emission goal to start tracking your carbon emissions!" 
        if costGoal==0: costText = "Input a cost goal to start tracking your spending!" 
            
        # Assign variables and render.
        return render_template("goals.html", title="Your Goals", form=form, emGoal = emGoal, emCurrent = emCurrent, emPercent = emPercent,
                            energyGoal = energyGoal, energyCurrent = energyCurrent, energyPercent = energyPercent,
                            costGoal = costGoal, costCurrent = costCurrent, costPercent = costPercent, energyText = energyText, emText = emText, costText = costText)
    else:
        flash('No appliance usage data found for the logged-in user.', 'warning')
        return redirect(url_for('your_appliances'))


# show admin page
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    passcode = "123"
    passcodeForm = AdminPasscodeForm()
    if passcodeForm.validate_on_submit():
        if passcodeForm.passcode.data == passcode:
            userForm = UserEditForm()
            users = models.User.query.all()
            return render_template("admin.html", title="Admin", users=users, form=userForm)

    return render_template("admin_pass.html", title="Admin", form=passcodeForm)


# show profile page
@app.route("/your_profile", methods=["GET", "POST"])
@login_required
def your_profile():
    form = ProfileForm()
    # update user
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.passwordHash = generate_password_hash(form.password.data)
        current_user.postcode = form.postcode.data
        current_user.provider = form.provider.data
        current_user.energyTarget = form.energyTarget.data
        current_user.emissionTarget = form.emissionTarget.data
        current_user.costTarget = form.costTarget.data

        db.session.commit()

    return render_template("your_profile.html", title="Profile", user=current_user, form=form)


@app.route("/bot", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        print("Received POST request:", request.form)
        message = request.form.get('message')
        if message:
            response = chatbot(message)
            print("Chatbot response:", response)
            return jsonify({'response': response})
        else:
            return jsonify({'error': 'No message provided'}), 400

    return render_template("chatbot.html")


# AJAX

# when click update button on your_appliances.html
@app.route('/updateAppliances', methods=['POST'])
def updateAppliances():

	# Load the JSON data
    removedApplianceIds = json.loads(request.data)['removedApplianceIds']
    appliancesData = json.loads(request.data)['appliancesData']

	# loop through appliance ids and delete them
    for i in range(len(removedApplianceIds)):
        models.Appliance.query.filter_by(id=int(removedApplianceIds[i])).delete()
    
    # update appliances data
    for i in range(len(appliancesData)):
        curApplianceId = appliancesData[i][0]['value']
        curAppliance = models.Appliance.query.filter_by(id=curApplianceId).first()
        curAppliance.applianceName = appliancesData[i][1]['value']
        curAppliance.hoursPerDay = int(appliancesData[i][2]['value'])
        curAppliance.powerRating = int(appliancesData[i][3]['value'])
        curAppliance.dateUsedOn = datetime.strptime(appliancesData[i][4]['value'], "%Y-%m-%d").date()
    db.session.commit()
    
    # updates usage based on new appliance data
    userEntries = models.Appliance.query.filter_by(email=current_user.email).all()
    if not userEntries: # i.e. no appliance in the database associated to the user
        flash("Please add an appliance", "warning")
    else:
        results = calculateSum(userEntries)
        entryExists = models.Usage.query.filter_by(email=current_user.email).all()

        if not entryExists:
                # Create a new entry with the calculated results.
                newUsageEntry = models.Usage(
                    email = current_user.email,
                    energyConsumed = results[0], 
                    cost = results[1],
                    carbonEmissions = results[2]
                )
                db.session().add(newUsageEntry)
        else:
            # find the entry and override the calculated results on to it.
            existingEntry = models.Usage.query.filter_by(email=current_user.email).first()
            existingEntry.energyConsumed = results[0]
            existingEntry.cost = results[1]
            existingEntry.carbonEmissions = results[2]

    db.session.commit()

    flash("Successfully updated database", "success")

    return json.dumps({'status':'OK'})



# when click update button on admin.html
@app.route('/updateUsers', methods=['POST'])
def updateUsers():

	# Load the JSON data
    removedUserIds = json.loads(request.data)['removedUserIds']
    usersData = json.loads(request.data)['usersData']

	# loop through user ids and delete them
    for i in range(len(removedUserIds)):
        models.User.query.filter_by(id=int(removedUserIds[i])).delete()
    
    # update users data
    for i in range(len(usersData)):
        curUserId = usersData[i][0]['value']
        curUser = models.User.query.filter_by(id=curUserId).first()
        curUser.name = usersData[i][1]['value']
        curUser.email = usersData[i][2]['value']
        curUser.passwordHash = generate_password_hash(usersData[i][3]['value'])
        curUser.dateCreated = datetime.strptime(usersData[i][4]['value'], "%Y-%m-%d %H:%M:%S.%f")
        curUser.postcode = usersData[i][5]['value']
        curUser.provider = usersData[i][6]['value']
        curUser.energyTarget = usersData[i][7]['value']
        curUser.emissionTarget = usersData[i][8]['value']
        curUser.costTarget = usersData[i][9]['value']

    db.session.commit()

    flash("Successfully updated database", "success")

    return json.dumps({'status':'OK'})


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)


from app import views, models
import logging

migrate = Migrate(app, db, render_as_batch=True)


logging.basicConfig(level=logging.DEBUG)




with app.app_context():
    db.create_all()
    
    from app.dash.applianceAnalytics import init_dashApp
    app = init_dashApp(app)

    db.session.query(models.Prompt).delete()
    # Promts to be displayed in the webpage to the user
    prompts = ["Keep it up! Your commitment to reducing energy consumption is admirable and making a difference.",
            "Watch out for energy consumptions, its ramping up!",
            "You're above the energy limit!, ask Terra for how to reduce this",
            "Well done! You're making a positive impact on the environment by reducing your carbon emissions.",
            "Your carbon emissions are increasing. Keep an eye on it!",
            "Uh oh, it looks like you've gone over the carbon limit. Ask terra for a closer look at your usage and find ways to reduce it.",
            "Keep up the great work! Your wallet is safe (for now)",
            "Be mindful of your energy consumption as it is impacting your wallet. Are there any changes you can make to lower costs?",
            "It seems like your costs have surpassed the goal set. Ask Terra to find ways to reduce them."]

    for x in range(len(prompts)):
        newPrompt = models.Prompt(id=x, message=prompts[x])
        db.session.add(newPrompt)
    db.session().commit()

    # List of initial providers for the user to pick from with their preset tariff
    presetDict = {
        "Scottish Power" : 0.1,
        "British Gas" : 0.1,
        "SSE" : 0.1,
        "E.On" : 0.1,
        "npower" : 0.1,
        "EDF Energy" : 0.1
    }
    for key, value in presetDict.items():
        presetExist = models.Provider.query.filter_by(energyProvider = key).all()
        if not presetExist:
            newPreset = models.Provider(energyProvider = key, tariff = value)
            db.session.add(newPreset)
    db.session.commit()
    

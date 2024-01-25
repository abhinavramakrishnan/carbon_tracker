from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    SelectField,
    DateTimeField,
    FloatField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

# Form for Login
class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email(), Length(5, 45)])
    password = PasswordField("password", validators=[DataRequired()])

# Form for Sign up 
class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 45, "Name is too long.")])
    email = StringField('email', validators=[DataRequired(), Email(), Length(5, 45, 'Email is too long.')])
    postcode = StringField('post code', validators=[DataRequired(), Length(6, 9, "Post code too long")])
    provider = SelectField('supplier', choices=[('British Gas','British Gas'),
                                             ('Scottish Power','Scottish Power'),
                                             ('SSE','SSE'),
                                             ('npower','npower'),
                                             ('E.ON','E.ON'),
                                             ('EDF Energy','EDF Energy'),
                                             ('Other','Other')], 
                       validators=[DataRequired(), Length(1, 50, "Supplier code too long")])

	password = PasswordField('password', validators=[DataRequired(), EqualTo('password_confirm', 'Passwords are not the same.')])
	password_confirm = PasswordField('Confirm the password.')

# Form for adding an appliance 
class ApplianceForm(FlaskForm):
    applianceName = StringField(
        "name", validators=[DataRequired(), Length(1, 45, "Name is too long.")]
    )
    watts = IntegerField("watts", validators=[DataRequired()])
    hoursPerDay = IntegerField("hoursPerDay", validators=[DataRequired(), NumberRange(0, 24)])

# Form for editing an appliance 
class ApplianceEditForm(FlaskForm):
    id = IntegerField("id")
    applianceName = StringField(
        "name", validators=[DataRequired(), Length(1, 45, "Name is too long.")]
    )
    watts = IntegerField("watts", validators=[DataRequired()])
    hoursPerDay = IntegerField("hoursPerDay", validators=[DataRequired(), NumberRange(0, 24)])
    dateUsedOn = DateTimeField("dateUsedOn", validators=[DataRequired()])

# Form for adding a custom supplier
class ProviderForm(FlaskForm):
    providerName = StringField('provider name', validators=[Length(1, 45, "Name is too long.")])
    providerTariff = FloatField('tariff')

# Form for adding a goal
class TargetForm(FlaskForm):
    energyTarget = FloatField("energyTarget")
    emissionTarget = FloatField("emTarget")
    costTarget = FloatField("costTarget")

# Form for editing user info
class UserEditForm(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired(), Length(1, 45, "Name is too long.")])
    email = StringField('email', validators=[DataRequired(), Email(), Length(5, 45, 'Email is too long.')])
    password = PasswordField('password', validators=[DataRequired()])
    dateCreated = DateTimeField("dateCreated", validators=[DataRequired()])
    postcode = StringField('post code', validators=[DataRequired(), Length(6, 9, "Post code too long")])
    provider = SelectField('supplier', choices=[('British Gas','British Gas'),
                                             ('Scottish Power','Scottish Power'),
                                             ('SSE','SSE'),
                                             ('npower','npower'),
                                             ('E.ON','E.ON'),
                                             ('EDF Energy','EDF Energy'),
                                             ('Other','Other')], 
                       validators=[DataRequired(), Length(1, 50, "Supplier code too long")])
    energyTarget = FloatField("energyTarget")
    emissionTarget = FloatField("emissionTarget")
    costTarget = FloatField("emissionTarget")

# Form for editing user details
class ProfileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 45, "Name is too long.")])
    email = StringField('email', validators=[DataRequired(), Email(), Length(5, 45, 'Email is too long.')])
    password = PasswordField('password', validators=[DataRequired()])
    postcode = StringField('post code', validators=[DataRequired(), Length(6, 9, "Post code too long")])
    provider = SelectField('supplier', choices=[('British Gas','British Gas'),
                                             ('Scottish Power','Scottish Power'),
                                             ('SSE','SSE'),
                                             ('npower','npower'),
                                             ('E.ON','E.ON'),
                                             ('EDF Energy','EDF Energy'),
                                             ('Other','Other')], 
                       validators=[DataRequired(), Length(1, 50, "Supplier code too long")])
    energyTarget = FloatField("energyTarget")
    emissionTarget = FloatField("emissionTarget")
    costTarget = FloatField("emissionTarget")


class AdminPasscodeForm(FlaskForm):
	passcode = PasswordField('passcode', validators=[DataRequired()])
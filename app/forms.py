from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, FloatField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired


class NewPropertyForm(FlaskForm):
    title = StringField("Property Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    no_rooms = FloatField("No. of Rooms", validators=[InputRequired()])
    no_bathrooms = FloatField("No. of Bathrooms", validators=[InputRequired()])
    price = DecimalField("Price", validators=[InputRequired()])
    property_type = SelectField("Property Type", validators=[InputRequired()], choices=["House", "Apartment"])
    location = StringField("Location", validators=[InputRequired()])
    photo = FileField("Photo", validators=[FileRequired(), FileAllowed(["png", "jpeg", "jpg"])])

"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from .forms import NewPropertyForm
from .models import Property
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename, send_from_directory


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/properties/create', methods=["POST", "GET"])
def new_property():
    """Render the website's about new property page."""
    form = NewPropertyForm()
    if form.validate_on_submit():
        [title, description, no_rooms, no_bathrooms, price, property_type, location, photo, token] = form
        filename = secure_filename(photo.data.filename)
        photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p = Property(title=title.data, description=description.data, no_rooms=no_rooms.data,
                     no_bathrooms=no_bathrooms.data, price=price.data, property_type=property_type.data,
                     location=location.data, photo=filename)
        db.session.add(p)
        db.session.commit()
        flash("Property Added Successfully")
        return redirect(url_for('properties'))
    return render_template('new-property.html', form=form)


@app.route('/properties')
def properties():
    """Render the website's properties page."""
    Properties = db.session.execute(db.select(Property)).scalars()
    return render_template('properties.html', properties=Properties)

@app.route('/properties/<id>')
def get_property(id):
    """Render the website's properties page based on an ID."""
    PropertyData = db.session.execute(db.select(Property).filter_by(id=id)).scalar_one()
    return render_template('property.html', property=PropertyData)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

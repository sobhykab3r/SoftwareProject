from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class ReviewForm(FlaskForm):
    title = StringField('Review title',validators=[DataRequired()])
    review = TextAreaField('Movie review')
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Tell us about yourself", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddToWatchlistForm(FlaskForm): 
    submit = SubmitField('Add to Watchlist')
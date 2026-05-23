from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ProjectForm(FlaskForm):
    name = StringField('Proje Adı', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Açıklama', validators=[Length(max=500)])
    submit = SubmitField('Projeyi Kaydet')

class BugTicketForm(FlaskForm):
    title = StringField('Bug Başlığı', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Detaylı Açıklama', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Bug Ekle')

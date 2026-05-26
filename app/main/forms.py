from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user
from app import db
from app.models import User

class UpdateProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('E-posta', validators=[DataRequired(), Email(), Length(max=120)])
    avatar = FileField('Profil Resmi Güncelle', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları yüklenebilir!')])
    dark_mode = BooleanField('Karanlık Tema')
    submit = SubmitField('Güncelle')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.scalar(db.select(User).filter_by(username=username.data))
            if user is not None:
                raise ValidationError('Bu kullanıcı adı zaten alınmış.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.scalar(db.select(User).filter_by(email=email.data))
            if user is not None:
                raise ValidationError('Bu e-posta adresi zaten kullanımda.')

class ProjectForm(FlaskForm):
    name = StringField('Proje Adı', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Açıklama', validators=[Length(max=500)])
    submit = SubmitField('Projeyi Kaydet')

class BugTicketForm(FlaskForm):
    title = StringField('Bug Başlığı', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Detaylı Açıklama', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Bug Ekle')

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, EqualTo, Length, Email, ValidationError

from .. import Msg
from ..models import USER_OCCUPATIONS, USER_GENDERS

data_required = InputRequired(Msg.UserRegistration.ERROR_REQUIRED_FIELD)

# Password validator function for all forms in which a new password is created.


def validate_password(field):
    """
        Password constraints:
        - At least one number
        - At least one upper case letter
        - At least one lower case letter
        - At least one special symbol (list between double quotes): "!#$%&()*+-/:;<=>?@[\]^{|}~"
        - Length between 6 and 64 characters long
    """

    password_validation_message = \
        "La contraseña debe contener más de 8 caracteres, una letra mayúscula, un número, y un caracter especial: !#$%&()*+-/:;<=>?@[\]^{|}~"
    password = field.data

    if len(password) < 8 or \
        len(password) > 64 or \
        not any(char.isdigit() for char in password) or \
        not any(char.isupper() for char in password) or \
        not any(char.islower() for char in password) or \
        not any(char in RegisterForm._special_characters for char in password):
            raise ValidationError(password_validation_message)

    return True


class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(
        Msg.UserRegistration.ERROR_INVALID_EMAIL)])
    password = PasswordField("Contraseña", validators=[data_required])
    remember_me = BooleanField("Mantener mi sesión iniciada")
    submit = SubmitField("Iniciar sesión")


class RegisterForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(
        Msg.UserRegistration.ERROR_INVALID_EMAIL)])
    first_name = StringField("Nombre", validators=[data_required])
    paternal_last_name = StringField(
        "Apellido paterno", validators=[data_required])
    maternal_last_name = StringField(
        "Apellido materno", validators=[data_required])
    birth_date = DateField("Fecha de nacimiento", validators=[data_required])
    gender = SelectField("Género", choices=USER_GENDERS,
                         validators=[data_required])
    occupation = SelectField(
        "Ocupación", choices=USER_OCCUPATIONS, validators=[data_required])

    password = PasswordField("Contraseña", validators=[data_required, EqualTo(
        "confirm_password", message=Msg.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField(
        "Confirmar contraseña", validators=[data_required])

    accept_terms_and_conditions = BooleanField(Msg.UserRegistration.ACCEPT_TERMS, validators=[
                                               InputRequired(message=Msg.UserRegistration.ERROR_ACCEPT_TERMS)])
    submit = SubmitField("Registrarse")

    _special_characters_raw = R"""!#$%&()*+-/:;<=>?@[\]^{|}~"""
    _special_characters = tuple(_special_characters_raw)

    def validate_password(self, field):
        return validate_password(field)

# Form for changing a new password when the old one is known.


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        "Antigua contraseña", validators=[data_required])
    password = PasswordField("Contraseña", validators=[data_required, EqualTo(
        "confirm_password", message=Msg.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField(
        "Confirmar contraseña", validators=[data_required])

    submit = SubmitField("Modficar contraseña")


class PasswordResetRequestForm(FlaskForm):
    # Form to request email to reset password.
    email = StringField("Correo", validators=[data_required, Email(
        Msg.UserRegistration.ERROR_INVALID_EMAIL)])

    submit = SubmitField("Enviar")


class PasswordResetForm(FlaskForm):
    # Form to change password from lost password email request.
    password = PasswordField("Nueva contraseña", validators=[data_required, EqualTo(
        "confirm_password", message=Msg.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField(
        "Confirmar contraseña", validators=[data_required])

    submit = SubmitField("Reestablecer contraseña")

    def validate_password(self, field):
        return validate_password(field)


class UserProfileForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(
        Msg.UserRegistration.ERROR_INVALID_EMAIL)])
    first_name = StringField("Nombre", validators=[data_required])
    paternal_last_name = StringField(
        "Apellido paterno", validators=[data_required])
    maternal_last_name = StringField(
        "Apellido materno", validators=[data_required])
    birth_date = DateField("Fecha de nacimiento", validators=[data_required])
    gender = SelectField("Género", choices=USER_GENDERS,
                         validators=[data_required])
    occupation = SelectField(
        "Ocupación", choices=USER_OCCUPATIONS, validators=[data_required])

    submit = SubmitField("Modificar perfil")

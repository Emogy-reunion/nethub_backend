from wtforms.validators import ValidationError

def length_check(min_length, max_length, field_name="Field"):
    def _length_check(form, field):
        length = len(field.data or '')
        if length < min_length:
            raise ValidationError(f"{field_name} is too short. Minimum {min_length} characters required.")

        if length > max_length:
            raise ValidationError(f"{field_name} is too long. Maximum {max_length} characters allowed.")
        
        return _length_check

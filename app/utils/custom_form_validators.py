from wtforms.validators import ValidationError

def length_check(min_length, max_length, field_name="Field"):
    def _length_check(form, field):
        length = len(field.data or '')
        if length < min_length:
            raise ValidationError(f"{field_name} is too short. Minimum {min_length} characters required.")

        if length > max_length:
            raise ValidationError(f"{field_name} is too long. Maximum {max_length} characters allowed.")
        
    return _length_check


def validate_features_field(form, field):

    """
    Validates a multiline text field where each line is a feature.
    Returns a cleaned list of features.
    """
    # Split the input by newlines and strip whitespace
    feature_list = [f.strip() for f in field.data.splitlines() if f.strip()]

    if not feature_list:
        raise ValidationError('Please enter at least one feature.')

    for i, feature in enumerate(feature_list):
        if len(feature) > 100:
            raise ValidationError(f'Feature at position {i+1} is too long (max 100 characters).')

    # Optional: overwrite field.data with the cleaned list
    field.data = feature_list

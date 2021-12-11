import os  
from django.core.exceptions import ValidationError

def file_validator_image(value):
    """
        Validates the type of image, file and size
    """
    file_size = value.size
    valid_file_extension = ['.jpg', '.png', '.jpeg','.JPG','.PNG','.JPEG',]

    file_extension = os.path.splitext(value.name)[1] 

    file_size_kb = file_size * 0.001
    file_size_mb = file_size_kb * 0.0001 

    if not file_extension in valid_file_extension: 
        raise ValidationError("Invalid file! Valid files only: ('.jpg', '.png', '.jpeg', 'pdf', 'doc', 'docx')")

    else:
        if file_size_mb > 5: # 5MB 
            raise ValidationError("The maximum file size can be upload is 5 MB")
        else: 
            return value

def file_validator_valid_attachment(value):
    """    
        Validates the type of image, file and size
    """
    file_size = value.size
    valid_file_extension = ['.pdf','.jpg', '.png', '.jpeg',]

    file_extension = os.path.splitext(value.name)[1] 

    file_size_kb = file_size * 0.001
    file_size_mb = file_size_kb * 0.0001 

    if not file_extension.lower() in valid_file_extension: 
        raise ValidationError("Invalid file! Valid files only: ('.pdf', '.png', '.jpg', '.jpeg')")

    else:
        if file_size_mb > 5: # 5MB 
            raise ValidationError("The maximum file size can be upload is 5 MB")
        else: 
            return value
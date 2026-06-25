'''
Validation helper functions.

'''

import re


def is_valid_password(password):
    """
    Validate password strength.

    Requirements:
    - At least 8 characters
    - At least 1 letter
    - At least 1 number 
    """
    if len(password) < 8:
        return False
    
    if not re.search(r"[A-Za-z]", password):
        return False
    
    if not re.search(r"[0-9]", password):
        return False
    
    return True






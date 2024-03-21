import bleach

def sanitize_input(input_string):
    # Use bleach to remove any harmful HTML tags
    sanitized_input = bleach.clean(input_string, strip=True)
    
    # Trim leading and trailing whitespace
    sanitized_input = sanitized_input.strip()
    
    # Replace sequences of whitespace with a single space
    sanitized_input = ' '.join(sanitized_input.split())
    
    return sanitized_input
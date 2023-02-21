

def analyze_file(file):
    file=convert_file_to_text(file)
    find_keywords(file)
    tag_document_by_keyword(file)
    analyze_text(file)
    return True

def find_keywords(file):
    return True

def analyze_text(file):
    return True

def convert_file_to_text(file):
    return True

def tag_document_by_keyword(file):
    return True

def get_definition(keyword):
    words={'sun':'sun','moon':'moon'}
    return words[keyword] if keyword in words else None

def get_document_summary(file_id):
    summary={1:'doc 1',2:'doc 2'}
    return summary[file_id] if file_id in summary else None
def list_to_dict(obj, key='Key', value='Value'):
    return {o[key]: o[value] for o in obj}

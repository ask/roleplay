import inspect
def load_module(module_name):
    can_load_module = 1
    try:
        module = __import__(module_name)
    except ImportError:
        can_load_module = 0
    assert can_load_module
    return module

def check_module_symbol_table(module_name, module_contents):
    module = load_module(module_name)
    #print str(dir(module))
    #for top_item in module_contents:
        
interface = {
    "roleplay.meta": {
        "AttributeIsPrototypeError": {"is":"Exception"},
        "RoleConflictDetected":      {"is":"Exception"},
        "RoleInheritsFromRole":      {"is":"Exception"},
        
        "CommonRole":   {
            "is":"Object",
            "has": "__is_role__".split(),
        },
    },
}


for module_name, module_contents in interface.items():
    check_module_symbol_table(module_name, module_contents)
    
        

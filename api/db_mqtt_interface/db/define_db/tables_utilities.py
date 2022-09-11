# imports database tables definitions 
from ambiental_variables            import *
from ambiental_variables_intervals  import *
from actuators_settings             import *
from users_table                    import *

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm         import Session
from sqlalchemy             import Table


def find_existent_tables(engine = None) -> list:

    """
        Finds the existent tables in the database.
    """

    base = automap_base()
    base.prepare(engine, reflect=True)
    
    # returns the list of the existent tables
    return base.classes.keys()


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


def load_all_tables(engine = None, metadata = None) -> dict:

    """
        Loads all the tables in the database.
    """
    
    table_names = find_existent_tables(engine)

    if not table_names:
        return {}

    # dictionaries to store the generated tables
    all_tables = {}
    var_tables = {}

    for table_name in table_names:

        table = Table(table_name,            
                      metadata,
                      autoload = True,
                      autoload_with = engine)

        # If the table name ends with '_var' we get to know that 
        # it is of type Variable, and we can create an instance based on that
        # same class
        if table_name.endswith("_var"):
            var_tables[table.name] = Variable_From_DB(engine = engine, 
                                                      table  = table)
            

        # if the table name is "actuators_configuration" or "variables_intervals"
        # then we create an instance for extending functionalities of the table

        if table_name == "actuators_configuration":
            all_tables["actuators"] =  Actuators_From_DB(engine = engine, 
                                                         table  = table)

        if table_name == "variables_intervals":
            all_tables["intervals"] =  Variable_Intervals_From_DB(engine = engine, 
                                                                  table  = table)

    all_tables["variables"] = var_tables
                                     
    return all_tables


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#



def create_tables_from_file(file_name: str, engine = None) -> None:
    

    """
        Creates the tables from a json file.
    """

    file_path = dirname(abspath(__file__)) + '/' + file_name
    data = {}

    # dictionaries to store the generated tables
    all_tables = {}
    var_tables = {}

    # reads the file and converts it to a dictionary
    print("Creating tables from file: " + current_file_dir + '/' + file_name)

    with open(file_path, "r") as file:
        data = json.load(file)


    # creates the tables related to ambiental variables measurements
    for table_name in data["variables"].keys():
        var_tables[table_name] = Variable(engine,
                                          table_name = table_name,
                                          column     = data["variables"][table_name]["column"],
                                          precision  = 3)
        var_tables[table_name].create_table()


    # stores the dictionaries of the tables
    all_tables["variables"] = var_tables

    # creates the tables related to acceptable and optimal values intervals
    all_tables["intervals"] = Variable_Intervals(engine, precision = 3)
    all_tables["intervals"].create_table()

    # creates the tables related to actuators and their functioning
    all_tables["actuators"] = Actuators(engine)
    all_tables["actuators"].create_table()


    return all_tables

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

def load_users_table(engine = None, metadata = None) -> dict:

    """
        Loads all the tables in the database.
    """

    table_name = find_existent_tables(engine)
    print(table_name)

    if table_name == []:
        return None

    table = Table(table_name[0],            
                  metadata,
                  autoload = True,
                  autoload_with = engine)

    table = Users_From_DB(table, engine)

    return table

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#






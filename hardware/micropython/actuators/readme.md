In the actuators_config.json we have the following structure

{
    "variable0":       {
                         "1":  {"pin_number": 23},
                        "-1":  {"pin_number": 22}
                      },

            ...

    "variableN":      {
                          "code":  {"pin_number": 21},
                         "-code":  {"pin_number": 19}
                      }

}

The hole idea of this is that for example we have the variable ph, then it's levels should be controlled and 
it could be by lowering the ph (using a waterpump and acid solution), or by increasing the levels (with 
another pump and basic solution), then we notice that we need to control 2 actuators, and by turning them 
on or off we can control the levels of ph.

To configure the actuators we follow the structure depicted above in the json file.

code 1 indicates increase on the value variable;
code -1 indicates decrease on the value of the variable.

and to each action performed by the codes 1 or -1 we have to assign a pin that corresponds to the control
of the water pumps used to pour basic or acid solutions. A more concrete example would be:


{
    "ph":       {
                     1:  {"pin_number": 23},
                    -1:  {"pin_number": 22}
                }
}

IMPORTANT:
---------------------------------------------

Please make sure the alias for the variables e.j "ph" or "ec" for electroconductivity should be the same aliases
that are used in the mqtt_config.json.






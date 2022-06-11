
----------------------------------------------------------------------------
--					Tablas de condiciones aceptables
----------------------------------------------------------------------------


-----------------------------------------------
-- Crea la tabla de  configuracion para funcionamiento de bomba de agua--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.water_pump(                                     
                                "time"		timestamp	NOT NULL,                          
                                frequency	float4		NOT NULL,                                
                                duration	float4		NOT NULL,                                
								start_time	time		NOT NULL,
								end_time	time		NOT NULL,
                                CONSTRAINT water_pump_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.water_pump OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  configuracion para funcionamiento de luces--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.lights(                                     
                                "time"		timestamp	NOT NULL,                          
								start_time	time		NOT NULL,
								end_time	time		NOT NULL,
                                CONSTRAINT lights_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.lights OWNER TO dave;




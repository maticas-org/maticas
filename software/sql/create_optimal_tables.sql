----------------------------------------------------------------------------
--					Tablas de condiciones optimas
----------------------------------------------------------------------------
						

-----------------------------------------------
-- Crea la tabla de  niveles optimos de humedad--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.humidity_optimal(                                
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT humidity_optimal_pk PRIMARY KEY ("time")
							);  
ALTER TABLE public.humidity_optimal OWNER TO dave;




-----------------------------------------------
-- Crea la tabla de  niveles optimos de temperatura--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                                 
public.temperature_optimal(                                 
                                "time" timestamp NOT NULL,                              
                                min float4 NOT NULL,                                    
                                max float4 NOT NULL,                                    
                                CONSTRAINT temperature_optimal_pk PRIMARY KEY ("time")
							);   
ALTER TABLE public.temperature_optimal OWNER TO dave;
							

-----------------------------------------------
-- Crea la tabla de  niveles optimos de ph--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.ph_optimal(                                      
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT ph_optimal_pk PRIMARY KEY ("time")
							);        
ALTER TABLE public.ph_optimal OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles optimos de ec--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.electroconductivity_optimal(                                      
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT electroconductivity_optimal_pk PRIMARY KEY ("time")
							);        
ALTER TABLE public.electroconductivity_optimal OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  niveles optimos de lux--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.lux_optimal(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT lux_optimal_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.lux_optimal OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles aceptables de temperatura del agua--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.water_temperature_optimal(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT water_temperature_optimal_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.water_temperature_optimal OWNER TO dave;






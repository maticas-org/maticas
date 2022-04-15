----------------------------------------------------------------------------
--					Tablas de variables del cultivo
----------------------------------------------------------------------------

-- Crea la tabla de humedad --
CREATE TABLE IF NOT EXISTS                  
public.temperature (                
							temp_level float4 NOT NULL,         
							"time" timestamp NOT NULL,          
							CONSTRAINT temperature_pk PRIMARY KEY ("time")
						);
ALTER TABLE public.temperature OWNER TO dave;


						
-------------------------------------------
-- Crea la tabla de humedad --
-------------------------------------------
CREATE TABLE if NOT EXISTS              
public.humidity(               
			hum_level float4 NOT NULL,      
			"time" timestamp NOT NULL,      
			CONSTRAINT humidity_pk PRIMARY KEY ("time")
				); 
ALTER TABLE public.humidity OWNER TO dave;


-------------------------------------------
-- Crea la tabla de temperatura del agua --
-------------------------------------------
CREATE TABLE if NOT EXISTS              
public.water_temperature(              
							wtemp_level float8 NOT NULL,    
							"time" timestamp NOT NULL,      
							CONSTRAINT water_temperature_pk PRIMARY KEY ("time")
					   	); 
ALTER TABLE public.water_temperature OWNER TO dave;


-------------------------------------------
-- Crea la tabla de electroconductividad --
-------------------------------------------
CREATE TABLE if NOT EXISTS              
public.electroconductivity(            
							ec_level float4 NOT NULL,           
							"time" timestamp NOT NULL,          
							CONSTRAINT electroconductivity_pk PRIMARY KEY ("time")
						  ); 
ALTER TABLE public.electroconductivity OWNER TO dave;


-------------------------------------------
-- Crea la tabla de electroconductividad --
-------------------------------------------
CREATE TABLE if NOT EXISTS              
public.electroconductivity (            
                                ec_level float4 NOT NULL,           
                                "time" timestamp NOT NULL,          
                                CONSTRAINT electroconductivity_pk PRIMARY KEY ("time")
							); 
ALTER TABLE public.electroconductivity OWNER TO dave;



-------------------------------------------
-- Crea la tabla de lux --
-------------------------------------------
CREATE TABLE if NOT EXISTS      
public.lux (                    
                                lux_level float8 NOT NULL,  
                                "time" timestamp NOT NULL,  
                                CONSTRAINT lux_pk PRIMARY KEY ("time")
							); 
ALTER TABLE public.lux OWNER TO dave;



-------------------------------------------
-- Crea la tabla de presión atmosférica --
-------------------------------------------
CREATE TABLE if NOT EXISTS              
public.atm_pressure (                   
                            pressure_level float4 NOT NULL,     
                            "time" timestamp NOT NULL,          
                            CONSTRAINT atm_pressure_pk PRIMARY KEY ("time")
						); 
ALTER TABLE public.atm_pressure OWNER TO dave;


----------------------------------------------------------------------------
--					Tablas de condiciones optimas
----------------------------------------------------------------------------
						

-----------------------------------------------
-- Crea la tabla de  niveles optimos de humedad--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.optimal_humidity(                                
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT optimal_humidity PRIMARY KEY ("time")
							);  
ALTER TABLE public.optimal_humidity OWNER TO dave;




-----------------------------------------------
-- Crea la tabla de  niveles optimos de temperatura--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                                 
public.optimal_temperature(                                 
                                "time" timestamp NOT NULL,                              
                                min float4 NOT NULL,                                    
                                max float4 NOT NULL,                                    
                                CONSTRAINT optimal_temperature PRIMARY KEY ("time")
							);   
ALTER TABLE public.optimal_temperature OWNER TO dave;
							

-----------------------------------------------
-- Crea la tabla de  niveles optimos de ph--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.optimal_ph(                                      
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT optimal_ph PRIMARY KEY ("time")
							);        
ALTER TABLE public.optimal_ph OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles optimos de ec--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.optimal_ec(                                      
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT optimal_ec PRIMARY KEY ("time")
							);        
ALTER TABLE public.optimal_ec OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de lux--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.optimal_lux(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT optimal_lux PRIMARY KEY ("time")
							);       
ALTER TABLE public.optimal_lux OWNER TO dave;



----------------------------------------------------------------------------
--					Tablas de condiciones aceptables
----------------------------------------------------------------------------


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de humedad--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.ok_humidity(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT ok_humidity PRIMARY KEY ("time")
							);       
ALTER TABLE public.ok_humidity OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de temperatura--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.ok_temperature(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT ok_temperature PRIMARY KEY ("time")
							);       
ALTER TABLE public.ok_temperature OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de ec--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.ok_ec(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT ok_ec PRIMARY KEY ("time")
							);       
ALTER TABLE public.ok_ec OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles aceptables de ph--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.ok_ph(                                     
			"time" timestamp NOT NULL,                          
			min float4 NOT NULL,                                
			max float4 NOT NULL,                                
			CONSTRAINT ok_ph PRIMARY KEY ("time")
			);       
ALTER TABLE public.ok_ph OWNER TO dave;









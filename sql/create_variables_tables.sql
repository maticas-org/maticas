----------------------------------------------------------------------------
--					Tablas de variables del cultivo
----------------------------------------------------------------------------


-------------------------------------------
-- Crea la tabla de temperatura --
-------------------------------------------
CREATE TABLE IF NOT EXISTS                  
public.temperature_ (                
							temp_level float4 NOT NULL,         
							"time" timestamp NOT NULL,          
							CONSTRAINT temperature_pk PRIMARY KEY ("time")
						);
ALTER TABLE public.temperature_ OWNER TO dave;


						
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
-- Crea la tabla de ph --
-------------------------------------------
CREATE TABLE if NOT EXISTS      
public.ph (                     
							ph_level float4 NOT NULL,   
							"time" timestamp NOT NULL,  
							CONSTRAINT ph_pk PRIMARY KEY ("time")); 
ALTER TABLE public.ph OWNER TO dave;


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





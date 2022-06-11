----------------------------------------------------------------------------
--					Tablas de condiciones aceptables
----------------------------------------------------------------------------


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de humedad--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.humidity_ok(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT humidity_ok_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.humidity_ok OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de temperatura--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.temperature_ok(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT temperature_ok_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.temperature_ok OWNER TO dave;


-----------------------------------------------
-- Crea la tabla de  niveles aceptables de ec--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.electroconductivity_ok(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT electroconductivity_ok_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.electroconductivity_ok OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles aceptables de ph--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.ph_ok(                                     
			"time" timestamp NOT NULL,                          
			min float4 NOT NULL,                                
			max float4 NOT NULL,                                
			CONSTRAINT ph_ok_pk PRIMARY KEY ("time")
			);       
ALTER TABLE public.ph_ok OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles aceptables de lux--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.lux_ok(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT lux_ok_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.lux_ok OWNER TO dave;



-----------------------------------------------
-- Crea la tabla de  niveles aceptables de temperatura del agua--
-----------------------------------------------
CREATE TABLE if NOT EXISTS                             
public.water_temperature_ok(                                     
                                "time" timestamp NOT NULL,                          
                                min float4 NOT NULL,                                
                                max float4 NOT NULL,                                
                                CONSTRAINT water_temperature_ok_pk PRIMARY KEY ("time")
							);       
ALTER TABLE public.water_temperature_ok OWNER TO dave;





# coding: utf-8

# # Thing

# In[1]:


thing = {
    "name": "TECO DustTracker",
    "description": "Version 1.0"
}


# # Datastreams

# In[2]:


datastream_PM10 = {
    "name": "PM10 Datastream",
    "description": "Collection of PM10 measurements",
    "unitOfMeasurement": {
        "name": "microgram per cubic meter",
        "symbol": "ug/m^3",
        "definition": "none"
    },
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
}

datastream_PM25 = {
    "name": "PM2.5 Datastream",
    "description": "Collection of PM2.5 measurements",
    "unitOfMeasurement": {
        "name": "microgram per cubic meter",
        "symbol": "ug/m^3",
        "definition": "none"
    },
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
}

datastream_temp = {
    "name": "Temperature Datastream",
    "description": "Collection of temperature measurements",
    "unitOfMeasurement": {
        "name": "degree Celsius",
        "symbol": "degC",
        "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
    },
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
}

datastream_hum = {
    "name": "Humidity Datastream",
    "description": "Collection of humidity measurements",
    "unitOfMeasurement": {
        "name": "percent",
        "symbol": "%",
        "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Percent"
    },
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
}

datastream_atpress = {
    "name": "Atmospheric Pressure Datastream",
    "description": "Collection of atmospheric Pressure measurements",
    "unitOfMeasurement": {
        "name": "Pascal",
        "symbol": "Pa",
        "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Pascal"
    },
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
}


# # Observed Properties

# In[3]:


observedproperty_PM10 = {
    "name": "PM10",
    "description": "Particulate matter with an approximate diameter of less than 10 micrometers",
    "definition": "https://www.eea.europa.eu/themes/air/air-quality/resources/glossary/pm10",
    "@iot.id": "PM10"
}

observedproperty_PM25 = {
    "name": "PM2.5",
    "description": "Particulate matter with an approximate diameter of less than 2.5 micrometers",
    "definition": "https://www.eea.europa.eu/themes/air/air-quality/resources/glossary/pm10",
    "@iot.id": "PM25"
}

observedproperty_temp = {
    "name": "Temperature",
    "description": "The degree or intensity of heat present in the area",
    "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature",
    "@iot.id": "temperature"
}

observedproperty_hum = {
    "name": "Humidity",
    "description": "Absolute humidity is the mass of water in a particular volume of air.",
    "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AbsoluteHumidity",
    "@iot.id": "humidity"
}

observedproperty_atpress = {
    "name": "Atmospheric Pressure",
    "description": "The pressure exerted at a point due to the presence of an atmosphere",
    "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AtmosphericPressure",
    "@iot.id": "atmospheric_pressure"
}


# # Sensors

# In[4]:


sensor_SDS011 = {
    "name": "Nova SDS011",
    "description": "Particulate matter sensor for PM10 and PM2.5",
    "encodingType": "application/pdf",
    "metadata": "http://www.teco.edu/~koepke/SDS011.pdf",
    "@iot.id": "SDS011"
}

sensor_BME280 = {
    "name": "Bosch BME280",
    "description": "Temperature, humidity and atmospheric pressure sensor",
    "encodingType": "application/pdf",
    "metadata": "http://www.teco.edu/~koepke/BME280.pdf",
    "@iot.id": "BME280"
}


# # Events

# In[5]:


event = {
    "phenomenonTime": "1963-11-22T18:30:34.000Z",
    "result": -1.0,
    "FeatureOfInterest": {
        "name": "Dallas",
        "description": "Dealey Plaza",
        "encodingType": "application/vnd.geo+json",
        "feature": {
            "type": "Point",
            "coordinates": [-96.80867, 32.77903]
        }
    }
}


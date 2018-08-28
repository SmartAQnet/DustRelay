
# coding: utf-8

# # imports

# In[ ]:


import requests
import json
import sys
import struct
import queue
import logging

try:
    get_ipython()
    isnotebook = True
except Exception:
    isnotebook = False
    
if isnotebook:
    # convert notebooks and import
    get_ipython().system('jupyter nbconvert --to script default_entities.ipynb')
    
import default_entities


# # logging

# In[ ]:


log = logging.getLogger("server_worker")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s(%(name)s): %(message)s")

fh = logging.FileHandler('./log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

sh = logging.StreamHandler(sys.stderr)
sh.setLevel(logging.ERROR)
sh.setFormatter(formatter)
log.addHandler(sh)


# # run()

# In[ ]:


def run(q, sturl, rawdata):
    try:
        dh = DataHandler(sturl, rawdata)
        dh.Decode()
        dh.CreateEverything()
    except Exception:
        log.error("cannot parse/send SensorThings data from " + rawdata[1][0])
        raise
    finally:
        q.task_done()


# # class: DataHandler

# In[ ]:


class DataHandler:
    
    def __init__(self, sturl, rawdata):
        """TODO: add doc string"""
        self.__bytedata = rawdata[0]
        self.__datatype = self.__bytedata[0]
        
        self.__address = rawdata[1]
        self.__sturl = sturl
        
        # create entity dictionaries
        self.__thing = dict(default_entities.thing)
        
        self.__sensor_SDS011 = dict(default_entities.sensor_SDS011)
        self.__sensor_BME280 = dict(default_entities.sensor_BME280)
        
        self.__datastream_PM10 = dict(default_entities.datastream_PM10)
        self.__observedproperty_PM10 = dict(default_entities.observedproperty_PM10)
        self.__event_PM10 = dict(default_entities.event)
        
        self.__datastream_PM25 = dict(default_entities.datastream_PM25)
        self.__observedproperty_PM25 = dict(default_entities.observedproperty_PM25)
        self.__event_PM25 = dict(default_entities.event)
        
        self.__datastream_temp = dict(default_entities.datastream_temp)
        self.__observedproperty_temp = dict(default_entities.observedproperty_temp)
        self.__event_temp = dict(default_entities.event)
        
        self.__datastream_hum = dict(default_entities.datastream_hum)
        self.__observedproperty_hum = dict(default_entities.observedproperty_hum)
        self.__event_hum = dict(default_entities.event)
        
        self.__datastream_atpress = dict(default_entities.datastream_atpress)
        self.__observedproperty_atpress = dict(default_entities.observedproperty_atpress)
        self.__event_atpress = dict(default_entities.event)
        
        
    def Decode(self):
        """TODO: add doc string"""
        if self.__datatype == 1:
            self.__DecodeType001();
        else:
            self.__thingid = "test thingid3!"
        
            self.__time = "1989-10-15T05:30:00.000Z"
            self.__coords = [50.0, 50.0, 50.0]
        
            self.__value_PM10 = 1337.10
            self.__value_PM25 = 1337.25
            self.__value_temp = -180.0
            self.__value_hum = 20.0
            self.__value_atpress = 101325.1337
            
        
    def __DecodeType001(self):
        byteorder = "<Bhi32sI"
        
        if self.__datatype != 1:
            raise TypeError("trying to decode invalid data type " + str(datatype))
        
        splitdata = struct.unpack(byteorder, self.__bytedata)
        decodeddata = list(map(lambda elem:                                elem.partition(b"\0")[0].decode("utf8") if type(elem) == bytes                                else elem, splitdata))
        
        self.__thingid = decodeddata[3]
        
        self.__time = "1989-10-15T05:30:00.000Z"
        self.__coords = [50.0, 50.0, 50.0]

        self.__value_PM10 = 1337.10
        self.__value_PM25 = 1337.25
        self.__value_temp = -180.0
        self.__value_hum = 20.0
        self.__value_atpress = 101325.1337
        
        
    def CreateEverything(self):
        """TODO: add docstring"""
        self.CreateThing()
        
        self.CreateDatastream_PM10()
        self.CreateDatastream_PM25()
        self.CreateDatastream_temp()
        self.CreateDatastream_hum()
        self.CreateDatastream_atpress()
        
        self.CreateEvent_PM10()
        self.CreateEvent_PM25()
        self.CreateEvent_temp()
        self.CreateEvent_hum()
        self.CreateEvent_atpress()
        
        
    def __PostEntity(self, where, entity):
        """TODO: add docstring"""
        try:
            entityid = entity["@iot.id"]
        except KeyError:
            entityid = "new ID"
            
        p = requests.post(self.__sturl + where, json.dumps(entity))
        if (p.status_code  == 201):
            log.debug("entity created: " + where + "('" + entityid + ")'")
            return True
        else:
            body = b"";
            for chunk in p.iter_content(chunk_size=128):
                body += chunk
                
            body = body.decode("utf8");
            body = body.replace('\n', ' ').replace('\r', '')
            
            if (p.status_code  == 500 and entityid != "new ID"):
                log.warning("entity exists already: " + where + "('" + entityid + ")'" + " - body: " + body)
                return False
            
            log.error("cannot create entity: " + where + "('" + entityid + ")'" +                       " - exit code: " + str(p.status_code) + " - body: " + body)
            raise TypeError("invalid entity")
            
            
    def CreateThing(self):
        """TODO: add docstring"""
        self.__thing["@iot.id"] = self.__thingid
        
        retval = self.__PostEntity("/Things", self.__thing)
        return retval
        
        
    def CreateDatastream_PM10(self):
        """TODO: add docstring"""
        self.__datastream_PM10["@iot.id"] = self.__thingid + "_PM10_Datastream"
        self.__datastream_PM10["ObservedProperty"] = self.__observedproperty_PM10
        self.__datastream_PM10["Sensor"] = self.__sensor_SDS011
        self.__datastream_PM10["Thing"] = {"@iot.id": self.__thingid}
        
        retval = self.__PostEntity("/Datastreams", self.__datastream_PM10)
        return retval
        
        
    def CreateDatastream_PM25(self):
        """TODO: add docstring"""
        self.__datastream_PM25["@iot.id"] = self.__thingid + "_PM25_Datastream"
        self.__datastream_PM25["ObservedProperty"] = self.__observedproperty_PM25
        self.__datastream_PM25["Sensor"] = self.__sensor_SDS011
        self.__datastream_PM25["Thing"] = {"@iot.id": self.__thingid}
        
        retval = self.__PostEntity("/Datastreams", self.__datastream_PM25)
        return retval
    
    
    def CreateDatastream_temp(self):
        """TODO: add docstring"""
        self.__datastream_temp["@iot.id"] = self.__thingid + "_temperature_Datastream"
        self.__datastream_temp["ObservedProperty"] = self.__observedproperty_temp
        self.__datastream_temp["Sensor"] = self.__sensor_BME280
        self.__datastream_temp["Thing"] = {"@iot.id": self.__thingid}
        
        retval = self.__PostEntity("/Datastreams", self.__datastream_temp)
        return retval
    
    
    def CreateDatastream_hum(self):
        """TODO: add docstring"""
        self.__datastream_hum["@iot.id"] = self.__thingid + "_humidity_Datastream"
        self.__datastream_hum["ObservedProperty"] = self.__observedproperty_hum
        self.__datastream_hum["Sensor"] = self.__sensor_BME280
        self.__datastream_hum["Thing"] = {"@iot.id": self.__thingid}
        
        retval = self.__PostEntity("/Datastreams", self.__datastream_hum)
        return retval
    
    
    def CreateDatastream_atpress(self):
        """TODO: add docstring"""
        self.__datastream_atpress["@iot.id"] = self.__thingid + "_atmospheric_pressure_Datastream"
        self.__datastream_atpress["ObservedProperty"] = self.__observedproperty_atpress
        self.__datastream_atpress["Sensor"] = self.__sensor_BME280
        self.__datastream_atpress["Thing"] = {"@iot.id": self.__thingid}
        
        retval = self.__PostEntity("/Datastreams", self.__datastream_atpress)
        return retval
        
        
    def CreateEvent_PM10(self):
        self.__event_PM10["result"] = self.__value_PM10
        self.__event_PM10["Datastream"] = {"@iot.id": self.__thingid + "_PM10_Datastream"}
        self.__event_PM10["phenomenonTime"] = self.__time
        self.__event_PM10["FeatureOfInterest"]["feature"]["coordinates"] = self.__coords
        self.__event_PM10["FeatureOfInterest"]["name"] = "none"
        self.__event_PM10["FeatureOfInterest"]["description"] = "none"
        
        retval = self.__PostEntity("/Observations", self.__event_PM10)
        return retval
        
        
    def CreateEvent_PM25(self):
        self.__event_PM25["result"] = self.__value_PM25
        self.__event_PM25["Datastream"] = {"@iot.id": self.__thingid + "_PM25_Datastream"}
        self.__event_PM25["phenomenonTime"] = self.__time
        self.__event_PM25["FeatureOfInterest"]["feature"]["coordinates"] = self.__coords
        self.__event_PM25["FeatureOfInterest"]["name"] = "none"
        self.__event_PM25["FeatureOfInterest"]["description"] = "none"
        
        retval = self.__PostEntity("/Observations", self.__event_PM25)
        return retval
    
    
    def CreateEvent_temp(self):
        self.__event_temp["result"] = self.__value_temp
        self.__event_temp["Datastream"] = {"@iot.id": self.__thingid + "_temperature_Datastream"}
        self.__event_temp["phenomenonTime"] = self.__time
        self.__event_temp["FeatureOfInterest"]["feature"]["coordinates"] = self.__coords
        self.__event_temp["FeatureOfInterest"]["name"] = "none"
        self.__event_temp["FeatureOfInterest"]["description"] = "none"
        
        retval = self.__PostEntity("/Observations", self.__event_temp)
        return retval
    
    
    def CreateEvent_hum(self):
        self.__event_hum["result"] = self.__value_hum
        self.__event_hum["Datastream"] = {"@iot.id": self.__thingid + "_humidity_Datastream"}
        self.__event_hum["phenomenonTime"] = self.__time
        self.__event_hum["FeatureOfInterest"]["feature"]["coordinates"] = self.__coords
        self.__event_hum["FeatureOfInterest"]["name"] = "none"
        self.__event_hum["FeatureOfInterest"]["description"] = "none"
        
        retval = self.__PostEntity("/Observations", self.__event_hum)
        return retval
    
    
    def CreateEvent_atpress(self):
        self.__event_atpress["result"] = self.__value_atpress
        self.__event_atpress["Datastream"] = {"@iot.id": self.__thingid + "_atmospheric_pressure_Datastream"}
        self.__event_atpress["phenomenonTime"] = self.__time
        self.__event_atpress["FeatureOfInterest"]["feature"]["coordinates"] = self.__coords
        self.__event_atpress["FeatureOfInterest"]["name"] = "none"
        self.__event_atpress["FeatureOfInterest"]["description"] = "none"
        
        retval = self.__PostEntity("/Observations", self.__event_atpress)
        return retval


# # tests

# In[ ]:


if __name__ ==  "__main__":
    testq = queue.Queue()
    testq.put((b"eine nachricht!", ("server und port", 123)))
    run(testq, "http://localhost:8080/FROST-Server/v1.0", testq.get())


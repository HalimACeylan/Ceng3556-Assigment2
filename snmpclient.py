# Native dependency required! Linux net-snmp
import typing
from typing import Optional
from easysnmp import *
from pydantic import BaseModel
import csv
import time



def snmp_session():
    return Session(hostname='localhost', community='public', version=2,remote_port=1161)

class SnmpMib(BaseModel):
    oid: str
    t: Optional[str] = None
    value: typing.Any = None

class System(BaseModel):
    sysDescr = SnmpMib(oid='1')
    sysUpTime = SnmpMib(oid='3')
    sysContact = SnmpMib(oid='4')
    sysName = SnmpMib(oid='5')
    sysLocation = SnmpMib(oid='6')
    sysORLastChange = SnmpMib(oid='8')
    sysORTable = SnmpMib(oid='9')

    class Meta:
        PREFIX = '1.3.6.1.2.1.1'

    @classmethod
    def find_all_system(cls):
        snmp = snmp_session()
        data = snmp.walk(cls.Meta.PREFIX)
        iso_prefix = 'iso.3.6.1.2.1.1'
        fields = cls.__fields__
        system_object = System()
        for d in data:
            key = next((k for k, v in fields.items() if f'{iso_prefix}.{v.default.oid}' == d.oid), None)
            if key is None:
                continue
            value = system_object.__getattribute__(key)
            value.value = d.value
            system_object.__setattr__(key, value)
        return system_object
    
class Resource(BaseModel):
    hrStorageOther = SnmpMib(oid='1')
    hrStorageRam = SnmpMib(oid='2')
    hrStorageVirtualMemory = SnmpMib(oid='3')
    hrStorageFixedDisk = SnmpMib(oid='4')
    hrStorageCompactDisc = SnmpMib(oid='7')
    hrStorageRamDisk = SnmpMib(oid='8')

    class Meta:
        PREFIX = '1.3.6.1.2.1.4.20.1.1.10.0.0'

    @classmethod
    def test(cls):
        snmp = snmp_session()
        data = snmp.walk(cls.Meta.PREFIX)
        for item in data:
            print('{oid}.{oid_index} {snmp_type} = {value}'.format(
                oid=item.oid,
                oid_index=item.oid_index,
                snmp_type=item.snmp_type,
                value=item.value
        ))
    @classmethod
    def find_all(cls):
        snmp = snmp_session()
        data = snmp.walk(cls.Meta.PREFIX)
        iso_prefix = 'iso.3.6.1.2.1.4.20.1.1.10.0.0'
        fields = cls.__fields__
        resource_object = Resource()
        for d in data:
            key = next((k for k, v in fields.items() if f'{iso_prefix}.{v.default.oid}' == d.oid), None)
            if key is None:
                continue
            value = resource_object.__getattribute__(key)
            value.value = d.value
            resource_object.__setattr__(key, value)
        return resource_object
    
system = System.find_all_system()
resource = Resource.find_all()
result = tuple(system) + tuple(resource)

# with open("data.csv", "w") as stream:
#     writer = csv.writer(stream)
#     for row in result:
#         writer.writerow(row)




def send_request():
        try:
            #get data
            system = System.find_all_system()
            resource = Resource.find_all()
            result = tuple(system) + tuple(resource)
        except:
            print("An error occurred:")
            return 0
        #write data
        with open("data.csv", "a") as stream:
            writer = csv.writer(stream)
            for row in result:
                writer.writerow(row)
    

# create file
with open("data.csv", "a") as stream:
    writer = csv.writer(stream)
    for row in result:
        writer.writerow(row)
 #send first request  for create 
system = System.find_all_system()
resource = Resource.find_all()
result = tuple(system) + tuple(resource)

while True:
    time.sleep(60)
    send_request()



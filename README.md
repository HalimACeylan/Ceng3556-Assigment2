# Ceng3556-Assigment2

## Personal Information
__Name__: Halim Abdurrahman Ceylan  \
__StudentId__ : 190709043 

## Requirements:
* HostResources MIB support (CPU load, disk partitions etc...).
* SNMPv2-MIB support(SystemName, SystemDescr, Hostname etc…)
* Server should serve to multiple clients.
* Clients should send requests on one minute intervals and record results on CSV files

## Note
To prevent confusion with an existing Linux net-snmp server in my test environment, I have chosen to use port number 1161 for my server implementation.
```python

#Client Side
def snmp_session():
    return Session(hostname='localhost', community='public', version=2,remote_port=1161)
    
#Server Side
async def main():
    sv = snmp_agent.Server(handler=handler, host='0.0.0.0', port=1161)
    await sv.start()
    while True:
        await asyncio.sleep(3600)
```


## Server Side
In the server-side code snippet, you have defined a handler function that handles SNMP requests. Some of the variables used in the function are in use, while others are not. Here's an explanation of the variables in the handler function:
```python 
async def handler(req: snmp_agent.SNMPRequest) -> snmp_agent.SNMPResponse:
    vbs = [
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.1', snmp_agent.OctetString('System')), #
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.3', snmp_agent.TimeTicks(100)), 
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.4', snmp_agent.OctetString('sysContact data')), 
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.5', snmp_agent.OctetString('fxp0')), 
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.6', snmp_agent.OctetString('sysLocation data')), 
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.8', snmp_agent.TimeTicks(200)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.9', snmp_agent.TimeTicks(1000)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.31.1.1.1.6.1', snmp_agent.Counter64(1000)), # not in use
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.31.1.1.1.10.1', snmp_agent.Counter64(1000)), # not in use
        snmp_agent.VariableBinding(
        '1.3.6.1.2.1.4.20.1.1.10.0.0.1', snmp_agent.Integer(1)), # not in use
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.4.20.1.1.10.0.0.2', snmp_agent.Integer(2)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.4.20.1.1.10.0.0.3', snmp_agent.Integer(3)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.4.20.1.1.10.0.0.4', snmp_agent.Integer(4)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.4.20.1.1.10.0.0.7', snmp_agent.Integer(7)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.4.20.1.1.10.0.0.8', snmp_agent.Integer(8))

        
    ]
    res_vbs = snmp_agent.utils.handle_request(req=req, vbs=vbs)
    res = req.create_response(res_vbs)
    return res 
```
    
## Client Side
The __Resource__ class is defined on the client side.In this case, the class is created based on the lesson content.[Source of Mibs](https://cric.grenoble.cnrs.fr/Administrateurs/Outils/MIBS/?oid=1.3.6.1.2.1.25.2.1).

```python 
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
```
### Client Side Request Loop
The provided code snippet represents the client-side request loop. It sends a request every 60 seconds using __time.sleep()__ and calls the __send_request()__ method. The retrieved data is then written to a data.csv file.
Here's an explanation of the client-side request loop:

```python
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
    time.sleep(5)
    send_request()

```

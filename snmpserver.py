import asyncio
import snmp_agent

async def handler(req: snmp_agent.SNMPRequest) -> snmp_agent.SNMPResponse:
    vbs = [
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.1.1', snmp_agent.OctetString('System')),
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
            '1.3.6.1.2.1.31.1.1.1.6.1', snmp_agent.Counter64(1000)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.31.1.1.1.10.1', snmp_agent.Counter64(1000)),
        snmp_agent.VariableBinding(
        '1.3.6.1.2.1.25.2.1.1', snmp_agent.Integer(1)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.25.2.1.2', snmp_agent.Integer(2)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.25.2.1.3', snmp_agent.Integer(3)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.25.2.1.4', snmp_agent.Integer(4)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.25.2.1.7', snmp_agent.Integer(7)),
        snmp_agent.VariableBinding(
            '1.3.6.1.2.1.25.2.1.8', snmp_agent.Integer(8))

        
    ]
    res_vbs = snmp_agent.utils.handle_request(req=req, vbs=vbs)
    res = req.create_response(res_vbs)
    return res

async def main():
    sv = snmp_agent.Server(handler=handler, host='0.0.0.0', port=1161)
    await sv.start()
    while True:
        await asyncio.sleep(3600)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
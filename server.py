import os
from oscpy.server import OSCThreadServer
import scripts.renderfarm_services as srs
import time

rf = None
def getRenderStatus(args):

	global rf
	print("Getting render status:")
	if rf is None:
		queues = ["/Storage/MNM_OMeninoMaluquinho/MNM_TBLIB/__TEMP_sandbox/render_farm/folder_001","/Storage/MNM_OMeninoMaluquinho/MNM_TBLIB/__TEMP_sandbox/render_farm/folder_002"]
		rf = srs.Renderfarm(os.getenv("OC_CLIENT"),os.getenv("OC_LOGIN"),os.getenv("OC_PASSWD"),queues)

	output = rf.checkRenderStatus(args[0] if len(args) > 0 else "")
	return output

def foo(args):

	print(args)

	return "output"

def getRoutes():


	return

routes = {'!check':getRenderStatus,'!juntator':foo}

def answer(args,port = None):

	print args
	args = [str.encode(a) for a in args]
	osc.answer(b'/response',args,port=port)

	return

def getRoute(address):

	return routes[address] if address in routes else None

def messageReceived(*msg):

	msg = [m.decode() for m in list(msg)]
	output = "ERRO:Comando desconhecido: {0}".format(msg[0])
	f = getRoute(msg[0])
	if f is not None:
		output = f(msg[1:-3])

	output = msg[-3] + output
	answer([str(output),str(msg[-1])],port=int(msg[-2]))
	return

#messageReceived(b'/ju',b'MNM_EP105',b'Ola fulano!\n',str(3500).encode(),b'asdasdsadasf23123asd')


osc = OSCThreadServer()  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='127.0.0.1', port=8030, default=True)

osc.bind(b'/request',messageReceived)

while(True):

	print("Listening...")
	time.sleep(5)

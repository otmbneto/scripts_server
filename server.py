import os
from oscpy.server import OSCThreadServer
import scripts.renderfarm_services as srs
import time

rf = None
def getRenderStatus(*args):

	global rf
	print("Getting render status")
	if rf is None:
		queues = ["/Storage/MNM_OMeninoMaluquinho/MNM_TBLIB/__TEMP_sandbox/render_farm/folder_001","/Storage/MNM_OMeninoMaluquinho/MNM_TBLIB/__TEMP_sandbox/render_farm/folder_002"]
		rf = srs.Renderfarm(os.getenv("OC_CLIENT"),os.getenv("OC_LOGIN"),os.getenv("OC_PASSWD"),queues)

	output = rf.checkRenderStatus(args[0] if len(args) > 0 else "")


osc = OSCThreadServer()  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='127.0.0.1', port=8030, default=True)
osc.bind(b'/check', getRenderStatus)

while(True):

	print("Listening...")
	time.sleep(5)


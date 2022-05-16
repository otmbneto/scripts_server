import os
from oscpy.server import OSCThreadServer
import scripts.renderfarm_services as srs

rf = None

def getRenderStatus(*args):

	print(values)
	if rf is None:
		queues = ["/Storage/MNM_OMeninoMaluquinho/MNM_TBLIB/__TEMP_sandbox/render_farm/folder_001","/Storage/MNM_OMeninoMaluquinho/MNM_TBLIB/__TEMP_sandbox/render_farm/folder_002"]
		rf = srs.Renderfarm(os.getenv("OC_CLIENT"),os.getenv("OC_LOGIN"),os.getenv("OC_PASSWD"),queues)

	output = rf.checkRenderStatus(args[0] if len(args) > 0 else "")
	osc.answer(str.encode(output))


osc = OSCThreadServer()  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/check', getRenderStatus)
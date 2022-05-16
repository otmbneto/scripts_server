import os
import owncloud
import time
import datetime
import json

#CALL : ($Check render,checkRenderStatus)

class Renderfarm:


	def __init__(self,site,login,password,queues):

		self.oc = self.oc_login(site,login,password)
		self.queues = queues
		self.name = ""

		return
	
	def hello(self):

		print("Hello world!")

	def oc_login(self,site,login,password):

		owncloud_client = owncloud.Client(site)
		owncloud_client.login(login,password)
		return owncloud_client


	def name_contains(self,file):

		return self.name in os.path.basename(file.path) 

	def get_renders(self,keyword):
		  
		files = []
		self.name = keyword
		for queue in self.queues:
			files += filter(self.name_contains,self.oc.list(queue))

		files.sort(key=lambda x: datetime.datetime.strptime(x.attributes["{DAV:}getlastmodified"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y%m%d_%H%M%S"))

		return files

	def getFileContent(self,oc_file):

		return json.loads(self.oc.get_file_contents(oc_file))

	def date_diff(self,date_1,date_2):

		date_format_str = '%d/%m/%Y, %H:%M:%S'
		start = datetime.datetime.strptime(date_1, date_format_str)
		end = datetime.datetime.strptime(date_2, date_format_str)

		return end - start

	#Calculate the difference in time between start and now.
	def getRenderTime(self,scene_file):
		
		renderTime = None
		if "started_at" in scene_file.keys():

			now = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())
			renderTime = self.date_diff(scene_file["started_at"],now)

		return renderTime

	def checkRenderStatus(self,keyword):

		scenes = self.get_renders(keyword)

		msg = ""
		for scene in scenes:

			scene_name = os.path.basename(scene.path).replace(".json","")
			scene_file = self.getFileContent(scene)
			msg+="--------------------------------\nCENA: {0}\nSTATUS:{1}\nTentativas: {2}\n"
			if scene_file["status"] == "rendering":
				renderTime = self.getRenderTime(scene_file)
				msg+="Renderizando por {}\n".format(renderTime)
			tries = len(scene_file["render_tries"]) if "render_tries" in scene_file.keys() else 0
			msg = msg.format(scene_name,scene_file["status"],tries)


		return msg if len(msg) > 0 else "Nenhum render foi encontrado na fila"

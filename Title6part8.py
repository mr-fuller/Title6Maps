import arcrest
import arcresthelper
from arcgis.gis import GIS

username = "fullerm"
password = "$parky460"
gis = GIS("https://arcgis.com",username,password)
buser = gis.users.get('michael.fuller')


# security handler
sh = arcrest.AGOLTokenSecurityHandler(username=username, password=password)
admin = arcrest.manageorg.Administration(securityHandler=sh)
user = admin.content.users.user()
#tent = admin.search("*")
ip = arcrest.manageorg.ItemParameter()
ip.title = "Railroad"
# ip.name = "Railroad"
ip.type = "Service Definition"
ip.tags = "service definition"
ip.description = "Railroad Projects"
ip.snippet = "snippet"
res = user.addItem(itemParameters=ip,
                       filePath="C:/Staging/Railroads.sd",
                       multipart=False)
#publishParameters = arcrest.manageorg.PublishSDParameters()
config = {'security_type':'ArcGIS','username':username, 'password':password}
from arcresthelper import securityhandlerhelper
token = securityhandlerhelper.securityhandlerhelper(config)
tent = gis.content.search('owner:fullerm AND Rail*')
print(tent)
ptool = arcresthelper.publishingtools.publishingtools(securityinfo=token)
itemId = ptool.getItemID(userContent=tent,title="Railroad",name=None,itemType="Service Definition")
user.publishItem(fileType="serviceDefinition",publishParameters=None,itemId=itemId)


from quetzal import document as Doc
from quetzal.utils import serializers
import web


#Schema instance
from api.public_resources.menus import model
Menus = model.Menus

######################## menus API ######################################

#Menus instance from schema
Menus = model.Menus



class ApiList(Doc.Json):
    def GET(self):
        try:
            #Append dictionary inside array
            arr = []
            for menu in Menus.objects:
                new = {}
                new['id'] = serializers.SerializeObject(menu.id)
                new['title'] = serializers.SerializeObject(menu.title)
                new['descr'] = serializers.SerializeObject(menu.descr)
                new['path'] = serializers.SerializeObject(menu.path)
                arr.append(new)
            #return json value
            json_result = self.contents(dict(r=arr))
            return json_result
        except Exception as e:
            raise web.notfound(e)
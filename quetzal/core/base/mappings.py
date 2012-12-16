from quetzal.filesystem import directory, module_operations, class_operations
import admin.app as admin
import app as site
import api
import web



#Mappings Manager will mapp provided mappings for site/admin
class Manager:


    def __init__(self, base, apiUrl, adminUrl):
        #stablish main app
        self.base = base
        #Admin stuff
        self.admin_app = admin.app
        self.adminApiUrl = adminUrl
        #Api stuff
        self.api_app = api.app
        self.apiUrl = apiUrl



    def get_main_mappings(self):
            main_mappings = (
                self.adminApiUrl.lower(), self.admin_app,
                self.apiUrl.lower(), self.api_app
            )
            return main_mappings



    def add_map_resource(self, resource_path, resource_type, api_class_prefix='Api'):

        resource_type = resource_type.lower()
        #Get a filtered list of files without .py, .pyc & starting with __...
        dirlist = directory.iterate_directory(resource_path)
        #Iterate through filtered list
        for i in range(len(dirlist)):
            #get resource path/name from filtered directory
            resource_path = resource_name = dirlist[i]
            try:
                #Build path for resources
                if resource_type=='admin':
                    module_resource_path = 'admin.app.'+resource_path+'.'+resource_name
                if resource_type=='site':
                    module_resource_path = 'app.'+resource_path+'.'+resource_name
                if resource_type=='apiadminresources':
                    module_resource_path = 'api.admin_resources.'+resource_path+'.'+resource_name
                if resource_type=='apiprivateresources':
                    module_resource_path = 'api.private_resources.'+resource_path+'.'+resource_name
                if resource_type=='apipublicresources':
                    module_resource_path = 'api.public_resources.'+resource_path+'.'+resource_name

                try:
                    #Load resource module
                    resource_module = module_operations.load_resource_module(module_resource_path)
                    #Iterate through classes
                    resources = class_operations.iterate_resource_class(resource_module, api_class_prefix)
                    #Iterate bidimensional array
                    #http://stackoverflow.com/a/1919055
                    for inst, name in zip(resources[0], resources[1]):
                        mapped_path = GetResourcePath(resource_type, inst, name, resource_path)
                        #Append to context accordingly
                        if resource_type=='admin':
                            self.admin_app.add_mapping(mapped_path, inst)
                        if resource_type=='apiadminresources' or resource_type=='apiprivateresources' or resource_type=='apipublicresources':
                            self.api_app.add_mapping(mapped_path, inst)
                        if resource_type=='site':
                            self.base.app.add_mapping(mapped_path, inst)
                except Exception as e:
                    #if some error is generated during mapping just pass to next resource module
                    pass
            except Exception, e:
                pass
                #Add main mapping at the end
        self.base.app.add_mapping('/', site.index)






def GetResourcePath(resource_type, mapped_class, class_name, resource_path):
    #Common
    api_name = class_name[3:]
    if resource_type=='site' or resource_type=='admin':
        try:
            if hasattr(mapped_class, 'path'):
                custom_path = getattr(mapped_class, 'path')
                return '/' + resource_path + custom_path.lower()
        except:
            pass
        return '/' + resource_path + '/' + api_name.lower()
    # API resource mappings - will map automatically according to privilege level:
    # 0 for anonymous users in public_resources
    # 1 for auhenticated users in private resources
    # 2 for administrators in admin resources

    #public modules: read only, just view data on current domain, can also view json like content
    #private modules: read & edit. Sometimes can add and remove some data like a user account
    #admin modules, can read, edit delete & add data from site & admin
    if resource_type=='apiadminresources':
        try:
            if hasattr(mapped_class, 'path'):
                custom_path = getattr(mapped_class, 'path')
                return '/2/' + resource_path + custom_path.lower()
        except:
            pass
        return '/2/' + resource_path + '/' + api_name.lower()

    if resource_type=='apiprivateresources':
        try:
            if hasattr(mapped_class, 'path'):
                custom_path = getattr(mapped_class, 'path')
                return '/1/' + resource_path + custom_path.lower()
        except:
            pass
        return '/1/' + resource_path + '/' + api_name.lower()

    if resource_type=='apipublicresources':
        try:
            if hasattr(mapped_class, 'path'):
                custom_path = getattr(mapped_class, 'path')
                return '/0/' + resource_path + custom_path.lower()
        except:
            pass
        return '/0/' + resource_path + '/' + api_name.lower()
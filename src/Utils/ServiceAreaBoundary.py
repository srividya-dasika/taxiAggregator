from src.Utils.database import Database
from src.Utils.ServiceArea import ServiceArea

class ServiceAreaBoundary():

    def create_boundary(self, city, boundary_file):
        service_obj = ServiceArea()
        service_area_def = service_obj.is_service_area_defined(city)
        if service_area_def is False:
            service_obj.create_service_area(boundary_file)





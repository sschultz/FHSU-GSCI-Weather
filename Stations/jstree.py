import json
import Stations.models as models


def jsTreeJSON():
    stations = [obj.name for obj in models.Station.objects.all()]
    data = []
    jstree_obj = {'core': {'data': data}}
    return json.dump(jstree_obj)

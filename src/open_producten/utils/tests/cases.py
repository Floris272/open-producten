from rest_framework.test import APITestCase


class BaseApiTestCase(APITestCase):
    path: str

    def get(self, object_id=""):
        end = "/" if object_id else ""
        return self.client.get(f"{self.path}{object_id}{end}")

    def post(self, data):
        return self.client.post(self.path, data, format="json")

    def put(self, object_id, data):
        return self.client.put(f"{self.path}{object_id}/", data, format="json")

    def patch(self, object_id, data):
        return self.client.patch(f"{self.path}{object_id}/", data, format="json")

    def delete(self, object_id):
        return self.client.delete(f"{self.path}{object_id}/")

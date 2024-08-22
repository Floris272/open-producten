from rest_framework.test import APITestCase


class BaseApiTestCase(APITestCase):
    endpoint: str

    def get(self, object_id=""):
        end = "/" if object_id else ""
        return self.client.get(f"{self.endpoint}{object_id}{end}")

    def post(self, data):
        return self.client.post(self.endpoint, data, format="json")

    def put(self, object_id, data):
        return self.client.put(f"{self.endpoint}{object_id}/", data, format="json")

    def patch(self, object_id, data):
        return self.client.patch(f"{self.endpoint}{object_id}/", data, format="json")

    def delete(self, object_id):
        return self.client.delete(f"{self.endpoint}{object_id}/")

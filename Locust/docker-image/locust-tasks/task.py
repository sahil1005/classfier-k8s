from email.mime import image
import requests
from io import BytesIO
from PIL import Image
from locust import HttpUser, TaskSet, task

image_raw = requests.get("https://i.kym-cdn.com/entries/icons/original/000/013/564/doge.jpg")
image = Image.open(BytesIO(image_raw.content))
image.save("/tmp/doge.jpg")
class UserBehavior(TaskSet):
    @task
    def predict(self):
        with open('/tmp/doge.jpg', 'rb') as image:
            self.client.post('/predict', files={'img_file': image})


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 500
    max_wait = 5000

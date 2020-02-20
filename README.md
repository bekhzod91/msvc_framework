# Microservice tools for django

### Install
```shell
pip install msvc_framework
```

settings.py

```python
INSTALL_APP = [
    ...,
    'msvc_framework',
]

MSVC_FRAMEWORK = {
    'ENGINE': 'msvc_framework.broker.kafka.KafkaBroker',
    'HOST': 'localhost',
    'TOPIC': 'topic'
}
```

### Service 1
register tasks in apps/{appname}/tasks.py
```python
from msvc_framework import tasks
from msvc_framework import SUCCESS

@tasks('user.user.get')
def get_users(data):
    print(data)
    return {
        'status': SUCCESS,
        'data': [{'id': 1, 'name': 'Mike'}]
    }
```


run command
```shell
python manange.py subscribe
```


### Service 2

#### Sync call tasks

```python
from msvc_framework import call

data = call('user.user.get', {'ids': [1]})
print(data)
```


use in model
```python
from msvc_framework import call

class Profile(models.Model):
    user = RemoteRelatedField('user.user.get')

    def __str__(self):
        return self.name


profile = Profile.objects.get(user=1)
print(profile.user.get())
print(profile.user.value)
```

use in Serializer

```python
from msvc_framework import ModelSerializer

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('id', 'user', )

```

#### Async call tasks

```python
from msvc_framework import async_call

async_call('user.user.get', {'ids': [1]})
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## How to deploy
Create config file in home directory `~/.pypirc`
```text
[distutils] 
index-servers=pypi
[pypi] 
repository = https://upload.pypi.org/legacy/ 
username = myrubapa
```
After run command for build and deploy
```shell
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```

for more detail read [packaging-projects](https://packaging.python.org/tutorials/packaging-projects/)
## License
[MIT](https://choosealicense.com/licenses/mit/)

# Django for microservice


settings.py

``` 
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
```
from msvc_framework import tasks
from msvc_framework import SUCCESS

@tasks('user.user.get')
def get_users(data):
    print(data)
    return {
        'status': SUCCESS,
        'data': [....]
    }
```


run command
```
python manange.py subscribe
```


### Service 2

sync call tasks
```
from msvc_framework import call

call('user.user.get', {'ids': [1]})
```


use in model
```
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

```
from msvc_framework import ModelSerializer

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('id', 'user', )

```
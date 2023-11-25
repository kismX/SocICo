from django.db import models
from django.contrib.auth import get_user_model


# neues model das eine Friednship darstellt
# es hat den 'from_user', von dem die anfrage ausgeht und 'to_user' an den die anfrage geht
# wann  die verbindung erstellt wurde geht automatisch: 'createtd_at' und wenn request angenommen, wird das leere 'acceptet_at' mit zeitpunkt ausgefüllt
class Friendship(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    

    # 2023-11-22 neu get_friends() um alle bestehenden freundschaften zu ermitteln
    # easy: ich verweise auf mein neu erstelltes model Friendship und filter mir aus den friedshipobjekten alle geaddeten raus
    def get_friends(self):
        friends = Friendship.objects.filter(accepted_at__isnull=False)
        return [friend for friend in friends] # spucke mir jeden friend in friends aus (wollt mal wieder dings hier üben.. [ ]) listcomprehension, junge!
from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50)
	email = models.CharField(max_length=50, unique=True)
	password = models.CharField(max_length=50)
	avatar = models.CharField(max_length=50)

class Messages(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.CharField(max_length=500)
	send_at = models.DateTimeField(auto_now_add=True)

class Stats(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	nb_games = models.IntegerField()
	nb_wins = models.IntegerField()

class Links(models.Model):
	user_id1 = models.ForeignKey(User, on_delete=models.CASCADE)
	user_id2 = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.CharField(max_length=50)


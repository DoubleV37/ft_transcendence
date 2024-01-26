from django.db import models

class User():
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50)
	email = models.CharField(max_length=50, unique=True)
	password = models.CharField(max_length=50)
	avatar = models.BitmapField()

class Messages():
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.CharField(max_length=500)
	send_at = models.DateTimeField(auto_now_add=True)

class Stats():
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	nb_games = models.IntegerField()
	nb_wins = models.IntegerField()

class Links():
	user_id1 = models.ForeignKey(User, on_delete=models.CASCADE)
	user_id2 = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.CharField(max_length=50)


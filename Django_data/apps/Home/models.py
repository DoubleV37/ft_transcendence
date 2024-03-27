# from django.db import models

# class Messages(models.Model):
#     idMsg = models.AutoField(primary_key=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     recipient = models.CharField(max_length=50)
#     body = models.CharField(max_length=500)
#     send_at = models.DateTimeField(auto_now_add=True)

# class Stats(models.Model):
#     idUser = models.ForeignKey(User, on_delete=models.CASCADE)
#     nb_games = models.IntegerField()
#     nb_wins = models.IntegerField()
#     nb_losses = models.IntegerField()

# class Links(models.Model):
#     user_id1 = models.ForeignKey(User, on_delete=models.CASCADE)
#     user_id2 = models.ForeignKey(User, on_delete=models.CASCADE)
#     link = models.CharField(max_length=50)

# class Settings(models.Model):
#     idUser = models.ForeignKey(User, on_delete=models.CASCADE)
#     background = models.CharField(max_length=50)
#     paddle = models.CharField(max_length=50)
#     ball = models.CharField(max_length=50)

# class UserGame(models.Model):
#     idUser = models.ForeignKey(User, on_delete=models.CASCADE)
#     idGame = models.AutoField(primary_key=True)
#     score = models.IntegerField()
#     win = models.BooleanField()

# class Game(models.Model):
#     idGame = models.AutoField(primary_key=True)
#     status = models.BooleanField()
#     date = models.DateTimeField(auto_now_add=True)
#     duration = models.IntegerField()
#     pwr_up = models.BooleanField()
#     nb_rounds = models.IntegerField()
#     in_tournament = models.BooleanField()

# class Tournament(models.Model):
#     idTournament = models.AutoField(primary_key=True)
#     nameTournament = models.CharField(max_length=50)
#     startDate = models.DateTimeField(auto_now_add=True)
#     endDate = models.DateTimeField()
#     nb_players = models.IntegerField()
#     nb_games = models.IntegerField()

# class GameTournament(models.Model):
#     idGame = models.ForeignKey(Game, on_delete=models.CASCADE)
#     idTournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     round = models.IntegerField()
#     winner = models.ForeignKey(User, on_delete=models.CASCADE)

# class UserTournament(models.Model):
#     idUser = models.ForeignKey(User, on_delete=models.CASCADE)
#     nickUser = models.CharField(max_length=50)
#     idTournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     score = models.IntegerField()

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Studio(models.Model):
    id_studio = models.AutoField(primary_key=True)
    nume_studio = models.CharField(unique=True, max_length=255)
    an_infintare = models.IntegerField(blank=True, null=True)
    sediu_studio = models.CharField(max_length=255, blank=True, null=True)
    tara_provenienta = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studio'


class Regizor(models.Model):
    id_regizor = models.AutoField(primary_key=True)
    nume_regizor = models.CharField(max_length=100)
    prenume_regizor = models.CharField(max_length=100)
    an_nastere_regizor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regizor'


class Actori(models.Model):
    id_actor = models.AutoField(primary_key=True)
    nume_actor = models.CharField(max_length=100)
    prenume_actor = models.CharField(max_length=100)
    an_nastere_actor = models.IntegerField(blank=True, null=True)
    sex_actor = models.CharField(max_length=1, blank=True, null=True)
    nationalitate_actor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actori'


class Gen(models.Model):
    id_gen = models.AutoField(primary_key=True)
    nume_gen = models.CharField(unique=True, max_length=100)
    descriere_gen = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen'


class Utilizator(models.Model):
    id_utilizator = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    parola_hash = models.CharField(max_length=255)
    data_inregistrare = models.DateTimeField(blank=True, null=True)
    varsta = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilizator'


class Filme(models.Model):
    id_film = models.AutoField(primary_key=True)
    an_aparitie = models.IntegerField(blank=True, null=True)
    nume_film = models.CharField(max_length=255)
    cost_prod = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    profit_brut = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    varsta_necesara = models.IntegerField(blank=True, null=True)
    id_studio = models.ForeignKey(Studio, models.DO_NOTHING, db_column='id_studio', blank=True, null=True)
    id_regizor = models.ForeignKey(Regizor, models.DO_NOTHING, db_column='id_regizor', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    durata = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filme'


class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    id_film = models.ForeignKey(Filme, models.DO_NOTHING, db_column='id_film')
    id_utilizator = models.ForeignKey(Utilizator, models.DO_NOTHING, db_column='id_utilizator')
    nume_comentariu = models.CharField(max_length=255, blank=True, null=True)
    descriere_comentariu = models.TextField(blank=True, null=True)
    rating_comentariu = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'


class FilmActor(models.Model):
    pk = models.CompositePrimaryKey('id_film', 'id_actor')
    id_film = models.ForeignKey(Filme, models.DO_NOTHING, db_column='id_film')
    id_actor = models.ForeignKey(Actori, models.DO_NOTHING, db_column='id_actor')
    rol = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'film_actor'


class FilmGen(models.Model):
    pk = models.CompositePrimaryKey('id_film', 'id_gen')
    id_film = models.ForeignKey(Filme, models.DO_NOTHING, db_column='id_film')
    id_gen = models.ForeignKey(Gen, models.DO_NOTHING, db_column='id_gen')

    class Meta:
        managed = False
        db_table = 'film_gen'


class FeedbackReactie(models.Model):
    pk = models.CompositePrimaryKey('id_feedback', 'id_utilizator', 'tip_actiune')
    id_feedback = models.ForeignKey(Feedback, models.DO_NOTHING, db_column='id_feedback')
    id_utilizator = models.ForeignKey(Utilizator, models.DO_NOTHING, db_column='id_utilizator')
    tip_actiune = models.CharField(max_length=20)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_reactie'

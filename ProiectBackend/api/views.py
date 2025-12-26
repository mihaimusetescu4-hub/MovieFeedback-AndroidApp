from django.db import connection
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
# from rest_framework.decorators import action
from .models import (
    Studio, Regizor, Actori, Gen, Utilizator, Filme, 
    Feedback, FilmActor, FilmGen, FeedbackReactie
)
from .serializers import (
    StudioSerializer, RegizorSerializer, ActorSerializer, GenSerializer, 
    UtilizatorSerializer, FilmSerializer, FeedbackSerializer, 
    FilmActorSerializer, FilmGenSerializer, FeedbackReactieSerializer
)

def fetch_one_dict(sql, params=None):
    if params is None: params = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if row is None: return None
        cols = [c[0] for c in cursor.description]
        return dict(zip(cols, row))

def fetch_all_dict(sql, params=None):
    if params is None: params = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, r)) for r in rows]

class RawSQLModelViewSet(viewsets.ViewSet):
    model = None
    serializer_class = None

    def _get_table_and_pk(self):
        meta = self.model._meta
        return meta.db_table, meta.pk.column

    def _get_columns(self):
        meta = self.model._meta
        cols = []
        for f in meta.get_fields():
            if not getattr(f, "concrete", False) or getattr(f, "auto_created", False) or getattr(f, "primary_key", False):
                continue
            cols.append(f.column)
        return cols

    def _row_to_dict(self, cursor, row):
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

    def list(self, request, *args, **kwargs):
        table, _ = self._get_table_and_pk()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            data = [self._row_to_dict(cursor, row) for row in rows]
        return Response(data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        table, pk_col = self._get_table_and_pk()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table} WHERE {pk_col} = %s", [pk])
            row = cursor.fetchone()
            if row is None:
                raise Http404
            data = self._row_to_dict(cursor, row)
        return Response(data)

    def create(self, request, *args, **kwargs):
        payload = request.data
        table, pk_col = self._get_table_and_pk()
        cols = self._get_columns()
        values = [payload.get(col) for col in cols]
        placeholders = ",".join(["%s"] * len(cols))
        col_list = ",".join(cols)
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) RETURNING {pk_col};",
                values,
            )
            new_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT * FROM {table} WHERE {pk_col} = %s", [new_id])
            row = cursor.fetchone()
            data = self._row_to_dict(cursor, row)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        payload = request.data
        table, pk_col = self._get_table_and_pk()
        cols = self._get_columns()
        set_expr = ", ".join([f"{col} = %s" for col in cols])
        values = [payload.get(col) for col in cols]
        values.append(pk)
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET {set_expr} WHERE {pk_col} = %s", values)
            cursor.execute(f"SELECT * FROM {table} WHERE {pk_col} = %s", [pk])
            row = cursor.fetchone()
            if row is None: raise Http404
            data = self._row_to_dict(cursor, row)
        return Response(data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        table, pk_col = self._get_table_and_pk()
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table} WHERE {pk_col} = %s", [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudioViewSet(RawSQLModelViewSet):
    model = Studio
    serializer_class = StudioSerializer

class RegizorViewSet(RawSQLModelViewSet):
    model = Regizor
    serializer_class = RegizorSerializer

class ActorViewSet(RawSQLModelViewSet):
    model = Actori
    serializer_class = ActorSerializer

class GenViewSet(RawSQLModelViewSet):
    model = Gen
    serializer_class = GenSerializer

# class UtilizatorViewSet(RawSQLModelViewSet):
#     model = Utilizator
#     serializer_class = UtilizatorSerializer
class UtilizatorViewSet(RawSQLModelViewSet):
    model = Utilizator
    serializer_class = UtilizatorSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data
        username = payload.get('username')
        parola_raw = payload.get('parola')
        email = payload.get('email')
        
        # Daca primim email, inseamna ca e INREGISTRARE
        if email:
            varsta = payload.get('varsta')
            data_acum = timezone.now()
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO utilizator (username, email, parola_hash, data_inregistrare, varsta) VALUES (%s, %s, %s, %s, %s) RETURNING id_utilizator",
                        [username, email, parola_raw, data_acum, varsta]
                    )
                    new_id = cursor.fetchone()[0]
                    return Response({"id_utilizator": new_id, "username": username}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Daca NU primim email, inseamna ca e LOGIN
        else:
            user_row = fetch_one_dict(
                "SELECT id_utilizator, username, parola_hash FROM utilizator WHERE username = %s",
                [username]
            )
            if user_row and parola_raw == user_row['parola_hash']:
                return Response({
                    "message": "Login reusit",
                    "id_utilizator": user_row['id_utilizator'],
                    "username": user_row['username']
                }, status=status.HTTP_200_OK)
            
            return Response({"error": "Credentiale invalide"}, status=status.HTTP_401_UNAUTHORIZED)

class FilmViewSet(RawSQLModelViewSet):
    model = Filme
    serializer_class = FilmSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        film_row = fetch_one_dict("""
            SELECT f.*, s.nume_studio, s.sediu_studio, s.tara_provenienta,
                   r.nume_regizor, r.prenume_regizor, r.an_nastere_regizor
            FROM filme f
            LEFT JOIN studio s ON f.id_studio = s.id_studio
            LEFT JOIN regizor r ON f.id_regizor = r.id_regizor
            WHERE f.id_film = %s;
        """, [pk])

        if not film_row: raise Http404

        data = {
            "id_film": film_row["id_film"],
            "nume_film": film_row["nume_film"],
            "an_aparitie": film_row["an_aparitie"],
            "durata": film_row["durata"],
            "rating": film_row["rating"],
            "cost_prod": film_row["cost_prod"],
            "profit_brut": film_row["profit_brut"],
            "varsta_necesara": film_row["varsta_necesara"],
            "studio": {
                "id_studio": film_row["id_studio"],
                "nume_studio": film_row["nume_studio"],
                "sediu_studio": film_row["sediu_studio"],
                "tara_provenienta": film_row["tara_provenienta"],
            },
            "regizor": {
                "id_regizor": film_row["id_regizor"],
                "nume_regizor": film_row["nume_regizor"],
                "prenume_regizor": film_row["prenume_regizor"],
                "an_nastere_regizor": film_row["an_nastere_regizor"],
            },
        }
        data["actori"] = fetch_all_dict("""
            SELECT a.*, fa.rol FROM film_actor fa
            JOIN actori a ON fa.id_actor = a.id_actor
            WHERE fa.id_film = %s;
        """, [pk])

        recenzii = fetch_all_dict("""
            SELECT fb.*, u.username FROM feedback fb
            JOIN utilizator u ON fb.id_utilizator = u.id_utilizator
            WHERE fb.id_film = %s ORDER BY fb.created_at DESC NULLS LAST;
        """, [pk])

        reactii = fetch_all_dict("""
            SELECT fr.id_feedback, fr.tip_actiune, COUNT(*) AS count_reactii
            FROM feedback_reactie fr
            JOIN feedback fb ON fr.id_feedback = fb.id_feedback
            WHERE fb.id_film = %s GROUP BY fr.id_feedback, fr.tip_actiune;
        """, [pk])

        reactii_map = {}
        for r in reactii:
            reactii_map.setdefault(r["id_feedback"], {})[r["tip_actiune"]] = r["count_reactii"]

        for rec in recenzii:
            rec["reactii"] = reactii_map.get(rec["id_feedback"], {})

        data["feedback"] = recenzii
        return Response(data)

# class FeedbackViewSet(RawSQLModelViewSet):
#     model = Feedback
#     serializer_class = FeedbackSerializer

class FeedbackViewSet(RawSQLModelViewSet):
    model = Feedback
    serializer_class = FeedbackSerializer

    def update(self, request, pk=None):
        nume = request.data.get('nume_comentariu')
        descriere = request.data.get('descriere_comentariu')
        rating = request.data.get('rating_comentariu')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE feedback 
                SET nume_comentariu = %s, 
                    descriere_comentariu = %s, 
                    rating_comentariu = %s,
                    updated_at = NOW() 
                WHERE id_feedback = %s
            """, [nume, descriere, rating, pk])
        
        return Response({'message': 'Update reusit!'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM feedback WHERE id_feedback = %s", [pk])
            
        return Response({'message': 'Sters cu succes!'}, status=status.HTTP_200_OK)

class FilmActorViewSet(viewsets.ViewSet):
    serializer_class = FilmActorSerializer
    def list(self, request):
        data = fetch_all_dict(f"SELECT * FROM {FilmActor._meta.db_table}")
        return Response(data)

class FilmGenViewSet(viewsets.ViewSet):
    serializer_class = FilmGenSerializer
    def list(self, request):
        data = fetch_all_dict(f"SELECT * FROM {FilmGen._meta.db_table}")
        return Response(data)

class FeedbackReactieViewSet(viewsets.ViewSet):
    serializer_class = FeedbackReactieSerializer
    def list(self, request):
        data = fetch_all_dict(f"SELECT * FROM {FeedbackReactie._meta.db_table}")
        return Response(data)
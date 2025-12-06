from django.db import connection
from django.http import Http404

from rest_framework import viewsets, status, serializers
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response

def fetch_one_dict(sql, params=None):
    if params is None:
        params = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if row is None:
            return None
        cols = [c[0] for c in cursor.description]
        return dict(zip(cols, row))


def fetch_all_dict(sql, params=None):
    if params is None:
        params = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, r)) for r in rows]


from .models import (
    Studio,
    Regizor,
    Actori,
    Gen,
    Utilizator,
    Filme,
    Feedback,
    FilmActor,
    FilmGen,
    FeedbackReactie,
)
from .serializers import (
    StudioSerializer,
    RegizorSerializer,
    ActorSerializer,
    GenSerializer,
    UtilizatorSerializer,
    FilmSerializer,
    FeedbackSerializer,
    FilmActorSerializer,
    FilmGenSerializer,
    FeedbackReactieSerializer,
)



class RawSQLModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet generic care face:
      - list()    -> SELECT * FROM table
      - retrieve()-> SELECT * FROM table WHERE pk = ...
      - create()  -> INSERT INTO table (...)
      - update()  -> UPDATE table SET ... WHERE pk = ...
      - destroy() -> DELETE FROM table WHERE pk = ...
    Toate folosesc doar SQL brut.
    Subclasele trebuie sa seteze: model, serializer_class.
    """

    model = None
    serializer_class = None


    def get_queryset(self):
        return self.model.objects.all()

    def _get_table_and_pk(self):
        meta = self.model._meta
        return meta.db_table, meta.pk.column


    def _get_columns(self):
        meta = self.model._meta
        cols = []
        for f in meta.get_fields():
            if not getattr(f, "concrete", False):
                continue
            if getattr(f, "auto_created", False):
                continue
            if getattr(f, "primary_key", False):
                continue
            cols.append(f.column)
        return cols

    # helper: tuplu -> dict
    def _row_to_dict(self, cursor, row):
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

    # ------- SELECT * FROM table -------
    def list(self, request, *args, **kwargs):
        table, _ = self._get_table_and_pk()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            data = [self._row_to_dict(cursor, row) for row in rows]
        return Response(data)

    # ------- SELECT * FROM table WHERE pk = %s -------
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field, None) or kwargs.get("pk")
        table, pk_col = self._get_table_and_pk()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table} WHERE {pk_col} = %s", [pk])
            row = cursor.fetchone()
            if row is None:
                raise Http404(f"{self.model.__name__} nu exista")
            data = self._row_to_dict(cursor, row)
        return Response(data)

    # ------- INSERT INTO table (...) VALUES (...) -------
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

    # ------- UPDATE table SET ... WHERE pk = %s -------
    def update(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field, None) or kwargs.get("pk")
        payload = request.data
        table, pk_col = self._get_table_and_pk()
        cols = self._get_columns()

        set_expr = ", ".join([f"{col} = %s" for col in cols])
        values = [payload.get(col) for col in cols]
        values.append(pk)

        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET {set_expr} WHERE {pk_col} = %s",
                values,
            )
            cursor.execute(f"SELECT * FROM {table} WHERE {pk_col} = %s", [pk])
            row = cursor.fetchone()
            if row is None:
                raise Http404(f"{self.model.__name__} nu exista")
            data = self._row_to_dict(cursor, row)

        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    # ------- DELETE FROM table WHERE pk = %s -------
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field, None) or kwargs.get("pk")
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


class UtilizatorViewSet(RawSQLModelViewSet):
    model = Utilizator
    serializer_class = UtilizatorSerializer


class FilmViewSet(RawSQLModelViewSet):
    model = Filme
    serializer_class = FilmSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field, None) or kwargs.get("pk")

        film_row = fetch_one_dict(
            """
            SELECT
                f.id_film,
                f.nume_film,
                f.an_aparitie,
                f.durata,
                f.rating,
                f.cost_prod,
                f.profit_brut,
                f.varsta_necesara,

                s.id_studio,
                s.nume_studio,
                s.sediu_studio,
                s.tara_provenienta,

                r.id_regizor,
                r.nume_regizor,
                r.prenume_regizor,
                r.an_nastere_regizor
            FROM filme f
            LEFT JOIN studio s   ON f.id_studio  = s.id_studio
            LEFT JOIN regizor r  ON f.id_regizor = r.id_regizor
            WHERE f.id_film = %s;
            """,
            [pk],
        )

        if film_row is None:
            raise Http404("Filmul nu exista")

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
        data["actori"] = fetch_all_dict(
            """
            SELECT
                a.id_actor,
                a.nume_actor,
                a.prenume_actor,
                fa.rol
            FROM film_actor fa
            JOIN actori a ON fa.id_actor = a.id_actor
            WHERE fa.id_film = %s;
            """,
            [pk],
        )

        recenzii = fetch_all_dict(
            """
            SELECT
                fb.id_feedback,
                fb.rating_comentariu,
                fb.nume_comentariu,
                fb.descriere_comentariu,
                fb.created_at,
                u.id_utilizator,
                u.username
            FROM feedback fb
            JOIN utilizator u ON fb.id_utilizator = u.id_utilizator
            WHERE fb.id_film = %s
            ORDER BY fb.created_at DESC NULLS LAST;
            """,
            [pk],
        )

        reactii = fetch_all_dict(
            """
            SELECT
                fr.id_feedback,
                fr.tip_actiune,
                COUNT(*) AS count_reactii
            FROM feedback_reactie fr
            JOIN feedback fb ON fr.id_feedback = fb.id_feedback
            WHERE fb.id_film = %s
            GROUP BY fr.id_feedback, fr.tip_actiune;
            """,
            [pk],
        )

        reactii_pe_feedback = {}
        for r in reactii:
            fid = r["id_feedback"]
            reactii_pe_feedback.setdefault(fid, {})
            reactii_pe_feedback[fid][r["tip_actiune"]] = r["count_reactii"]

        for rec in recenzii:
            fid = rec["id_feedback"]
            rec["reactii"] = reactii_pe_feedback.get(fid, {})

        data["recenzii"] = recenzii
        data["feedback"] = recenzii

        return Response(data)



class FeedbackViewSet(RawSQLModelViewSet):
    model = Feedback
    serializer_class = FeedbackSerializer


class FilmActorViewSet(ReadOnlyModelViewSet):
    queryset = FilmActor.objects.all()
    serializer_class = FilmActorSerializer

    def list(self, request, *args, **kwargs):
        table = FilmActor._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        raise Http404("Nu este definit retrieve pe cheie compusa aici.")


class FilmGenViewSet(ReadOnlyModelViewSet):
    queryset = FilmGen.objects.all()
    serializer_class = FilmGenSerializer

    def list(self, request, *args, **kwargs):
        table = FilmGen._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        raise Http404("Nu este definit retrieve pe cheie compusa aici.")


class FeedbackReactieViewSet(ReadOnlyModelViewSet):
    queryset = FeedbackReactie.objects.all()
    serializer_class = FeedbackReactieSerializer

    def list(self, request, *args, **kwargs):
        table = FeedbackReactie._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        raise Http404("Nu este definit retrieve pe cheie compusa aici.")

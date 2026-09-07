from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.CharField(max_length=500, blank=True, default='')

    class Meta:
        db_table = 'universities'
        verbose_name = 'Université'
        verbose_name_plural = 'Universités'

    def __str__(self):
        return self.name


class Student(models.Model):
    matricule = models.CharField(max_length=50, db_index=True)
    full_name = models.CharField(max_length=255, db_index=True)
    promotion = models.CharField(max_length=100, db_index=True)
    level = models.CharField(max_length=50, db_index=True)
    option = models.CharField(max_length=255, blank=True, default='')
    section = models.CharField(max_length=255, blank=True, default='')
    annee_academique = models.CharField(max_length=20, default='2024-2025')
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'students'
        verbose_name = 'Étudiant'
        verbose_name_plural = 'Étudiants'
        unique_together = ('matricule', 'promotion', 'annee_academique')

    def __str__(self):
        return f'{self.full_name} ({self.matricule})'


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    code_ue = models.CharField(max_length=50)
    intitule_ue = models.CharField(max_length=255)
    bci = models.CharField(max_length=100)
    categorie = models.CharField(max_length=10, default='A')
    credits = models.IntegerField(default=0)
    note = models.FloatField()
    session = models.CharField(max_length=50, default='Normal')
    note_ponderee = models.FloatField(default=0.0)

    class Meta:
        db_table = 'results'
        verbose_name = 'Résultat'
        verbose_name_plural = 'Résultats'

    def __str__(self):
        return f'{self.code_ue} - {self.student.full_name} ({self.note}/20)'


class SemesterReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    annee_academique = models.CharField(max_length=20)
    total_credits = models.IntegerField(default=0)
    total_pondere = models.FloatField(default=0.0)
    moyenne = models.FloatField(default=0.0)
    moyenne_a = models.FloatField(default=0.0)
    moyenne_b = models.FloatField(default=0.0)
    decision = models.CharField(max_length=20, blank=True, default='')
    mention = models.CharField(max_length=50, blank=True, default='')
    credits_capitalises = models.IntegerField(default=0)

    class Meta:
        db_table = 'semester_reports'
        verbose_name = 'Rapport semestriel'
        verbose_name_plural = 'Rapports semestriels'

    def __str__(self):
        return f'{self.student.full_name} - {self.semester} ({self.moyenne})'

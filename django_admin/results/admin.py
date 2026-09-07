from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Avg
from .models import University, Student, Result, SemesterReport


class ISPAdminSite(AdminSite):
    site_header = 'ISP-GOMBE — Administration'
    site_title = 'ISP-GOMBE Admin'
    index_title = 'Tableau de bord'


admin_site = ISPAdminSite(name='isp_admin')


@admin.register(Student, site=admin_site)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'full_name', 'promotion', 'level', 'option', 'section', 'annee_academique', 'result_count')
    list_filter = ('promotion', 'level', 'annee_academique', 'option', 'section')
    search_fields = ('matricule', 'full_name')
    list_per_page = 50
    ordering = ('matricule',)

    def result_count(self, obj):
        return obj.results.count()
    result_count.short_description = 'Nb résultats'
    result_count.admin_order_field = 'results__count'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(result_count=Count('results'))


@admin.register(Result, site=admin_site)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_matricule', 'student_name', 'code_ue', 'intitule_ue', 'bci', 'categorie', 'credits', 'note', 'note_ponderee', 'session')
    list_filter = ('session', 'categorie', 'code_ue')
    search_fields = ('student__matricule', 'student__full_name', 'code_ue', 'intitule_ue')
    list_per_page = 50
    raw_id_fields = ('student',)
    ordering = ('student__matricule', 'code_ue')

    def student_matricule(self, obj):
        return obj.student.matricule
    student_matricule.short_description = 'Matricule'
    student_matricule.admin_order_field = 'student__matricule'

    def student_name(self, obj):
        return obj.student.full_name
    student_name.short_description = 'Étudiant'
    student_name.admin_order_field = 'student__full_name'


@admin.register(University, site=admin_site)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_url')
    search_fields = ('name',)


@admin.register(SemesterReport, site=admin_site)
class SemesterReportAdmin(admin.ModelAdmin):
    list_display = ('student_matricule', 'student_name', 'semester', 'annee_academique', 'moyenne', 'decision', 'mention')
    list_filter = ('semester', 'annee_academique', 'decision')
    search_fields = ('student__matricule', 'student__full_name')

    def student_matricule(self, obj):
        return obj.student.matricule
    student_matricule.short_description = 'Matricule'

    def student_name(self, obj):
        return obj.student.full_name
    student_name.short_description = 'Étudiant'


admin_site.site_header = 'ISP-GOMBE — Administration'
admin_site.site_title = 'ISP-GOMBE Admin'
admin_site.index_title = 'Gestion des résultats'

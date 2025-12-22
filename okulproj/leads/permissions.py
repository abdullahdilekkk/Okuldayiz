from rest_framework.permissions import BasePermission

class IsLeadOwner(BasePermission):
    """
    Bu özel izin sınıfı, sadece okul sahibinin
    kendi okuluna gelen başvuruları görmesini sağlar.
    obj = Ulaşılmaya çalışılan Veri
    """
    def has_object_permission(self, request, view, obj):
        return obj.school.owner == request.user
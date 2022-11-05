from django.db import models

class Teacher(models.Model):
    name = models.CharField('nome', max_length=100)
    description = models.TextField('descrição', max_length=2000, null=True, blank=True)
    hour_value = models.DecimalField(
        'valor_hora', max_digits=9, decimal_places=2
        )
    picture = models.URLField('foto')

    class Meta:
        unique_together = ['name', 'description']


class ClassRoom(models.Model):
    name = models.CharField('aula', max_length=100)
    email = models.EmailField('email', max_length=255)
    teacher = models.ForeignKey(
        Teacher, 
        related_name='classes', 
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['email', 'teacher']
    
    @property
    def teacher_name(self):
        return self.teacher.name
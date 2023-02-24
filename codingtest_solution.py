from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=255)
    description = models.TextField()
    hiring_date = models.DateField()

    def __str__(self):
        return self.name

class Vacation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attachment_file_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.employee.name} ({self.start_date} - {self.end_date})'

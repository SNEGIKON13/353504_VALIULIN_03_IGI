from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
        message="Номер телефона должен быть в формате: '+375 (29) XXX-XX-XX'"
    )
    phone = models.CharField(validators=[phone_regex], max_length=20, unique=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True)
    is_instructor = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username
        
    def age(self):
        if self.birth_date:
            today = timezone.now()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
        
    def is_adult(self):
        return self.age() >= 18 if self.age() is not None else False

class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_local_time(self):
        return timezone.localtime(self.created_at)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class About(models.Model):  # Renamed from CompanyInfo to About
    title = models.CharField(max_length=200)  # Keep old field
    description = models.TextField()
    history = models.TextField(default='')  # Keep old field
    contacts = models.TextField(default='')  # Keep old field
    address = models.CharField(max_length=500)
    # New fields with null/blank allowed initially
    name = models.CharField(max_length=200, verbose_name="Название компании", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", null=True, blank=True)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)

    class Meta:
        db_table = 'about'
        verbose_name = "About"
        verbose_name_plural = "About"

class FAQ(models.Model):
    question = models.CharField(max_length=500, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        db_table = 'faq'
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question

class Staff(models.Model):
    name = models.CharField(max_length=200, verbose_name="ФИО")
    position = models.CharField(max_length=200, verbose_name="Должность")
    description = models.TextField(verbose_name="Описание работы")
    photo = models.ImageField(upload_to='staff_photos/', verbose_name="Фото")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        db_table = 'staff'
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name="Position Title")
    description = models.TextField(verbose_name="Job Description")
    requirements = models.TextField(verbose_name="Requirements")
    salary = models.CharField(max_length=100, verbose_name="Salary Range", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        db_table = 'vacancies'
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Name")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Rating")
    text = models.TextField(verbose_name="Review Text")
    created_at = models.DateTimeField(default=timezone.now)

    def get_local_time(self):
        return timezone.localtime(self.created_at)

    class Meta:
        db_table = 'reviews'
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}★"

class Promo(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Promo Code")
    description = models.TextField(verbose_name="Description")
    discount = models.IntegerField(verbose_name="Discount %")
    valid_from = models.DateTimeField(verbose_name="Valid From")
    valid_to = models.DateTimeField(verbose_name="Valid To")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        db_table = 'promos'
        verbose_name = "Promo"
        verbose_name_plural = "Promos"

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to

class Gym(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    capacity = models.IntegerField(verbose_name="Capacity")

    class Meta:
        db_table = 'gyms'
        verbose_name = "Gym"
        verbose_name_plural = "Gyms"

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='equipment')
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'equipment'
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Service Name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    duration = models.IntegerField(verbose_name="Duration (minutes)", default=60)
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

class Group(models.Model):
    name = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    instructors = models.ManyToManyField('CustomUser', limit_choices_to={'is_instructor': True})
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    max_participants = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'groups'
        verbose_name = "Group"
        verbose_name_plural = "Groups"

class Session(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    instructors = models.ManyToManyField('CustomUser', limit_choices_to={'is_instructor': True})
    
    class Meta:
        db_table = 'sessions'
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def duration(self):
        return self.end_time - self.start_time

class Membership(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'memberships'
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    member = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'attendance'
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"

class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    preferred_date = models.DateTimeField(verbose_name="Preferred Date", default=timezone.now)
    notes = models.TextField(verbose_name="Additional Notes", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_bookings'
        ordering = ['-created_at']
        verbose_name = 'Service Booking'
        verbose_name_plural = 'Service Bookings'

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.get_status_display()})"

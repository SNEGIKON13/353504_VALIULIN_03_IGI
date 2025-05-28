from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
        message="Номер телефона должен быть в формате: '+375 (29) XXX-XX-XX'"
    )
    phone = models.CharField(validators=[phone_regex], max_length=20, unique=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True)
    is_instructor = models.BooleanField(default=False)
    SUBSCRIPTION_CHOICES = [
        ('none', 'Нет абонемента'),
        ('single', 'Разовое посещение'),
        ('basic', 'Базовый'),  
        ('premium', 'Премиум'),
        ('unlimited', 'Безлимитный'),
    ]
    subscription = models.CharField(
        max_length=10, 
        choices=SUBSCRIPTION_CHOICES,
        default='none',
        verbose_name="Тип абонемента"
    )
    subscription_end = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Дата окончания абонемента"
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username
        
    def age(self):
        if self.birth_date:
            today = timezone.now().date()
            age = today.year - self.birth_date.year
            # Only subtract a year if birthday hasn't occurred this year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
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
    name = models.CharField(max_length=200, verbose_name="Название зала")
    description = models.TextField(verbose_name="Описание")
    capacity = models.IntegerField(verbose_name="Вместимость")

    class Meta:
        db_table = 'gyms'
        verbose_name = "Gym"
        verbose_name_plural = "Gyms"

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название оборудования")
    description = models.TextField(verbose_name="Описание")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='equipment', verbose_name="Зал")
    quantity = models.IntegerField(verbose_name="Количество")

    class Meta:
        db_table = 'equipment'
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"{self.name} ({self.gym.name})"

class Group(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название группы")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    duration = models.IntegerField(verbose_name="Длительность (минут)")
    instructors = models.ManyToManyField(CustomUser, related_name='instructor_groups', 
                                       limit_choices_to={'is_instructor': True}, 
                                       verbose_name="Инструкторы")
    members = models.ManyToManyField(CustomUser, through='Membership',
                                   related_name='member_groups', 
                                   verbose_name="Участники")
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True, 
                           verbose_name="Зал")
    capacity = models.IntegerField(verbose_name="Максимальное количество участников")
    start_date = models.DateField(verbose_name="Дата начала занятий")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    repeat_days = models.IntegerField(verbose_name="Повтор каждые N дней", 
                                    validators=[MinValueValidator(1)])
    total_sessions = models.IntegerField(verbose_name="Количество занятий", 
                                       validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'groups'
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name

    def clean(self):
        if not self.gym:
            logger.error(f"Attempted to create group without gym assignment")
            raise ValidationError("Необходимо указать зал для занятий")
        
        if self.capacity > self.gym.capacity:
            logger.warning(f"Attempted to set group capacity {self.capacity} greater than gym capacity {self.gym.capacity}")
            raise ValidationError(f"Количество участников не может превышать вместимость зала ({self.gym.capacity} человек)")
        
        if self.start_time >= self.end_time:
            logger.error(f"Invalid time range: {self.start_time} - {self.end_time}")
            raise ValidationError("Время начала должно быть раньше времени окончания")

    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            logger.info(f"Creating new group: {self.name}")
        else:
            logger.info(f"Updating group: {self.name} (ID: {self.pk})")
        super().save(*args, **kwargs)

class Membership(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('frozen', 'Заморожен'),
        ('completed', 'Завершен'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'memberships'
        unique_together = ['user', 'group']
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            logger.info(f"Creating new membership: {self.user.username} -> {self.group.name}")
        else:
            logger.info(f"Updating membership: {self.user.username} -> {self.group.name} (ID: {self.pk})")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Deleting membership: {self.user.username} -> {self.group.name} (ID: {self.pk})")
        super().delete(*args, **kwargs)

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendances')
    session_date = models.DateField()
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendances'
        unique_together = ['user', 'group', 'session_date']
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.session_date})"

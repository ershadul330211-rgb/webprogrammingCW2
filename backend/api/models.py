from django.db import models

class Character(models.Model):
    """
    Model for a Gintama Character
    """
    name = models.CharField(max_length=100)
    
    description = models.TextField(help_text="A brief bio of the character.")
    
    age = models.IntegerField(null=True, blank=True, help_text="Can be null")
    
    birthday = models.DateField(null=True, blank=True, help_text="Character's birthday")
    
    
    is_samurai = models.BooleanField(default=False)

    def __str__(self):
        """String representation."""
        return self.name

    def to_dict(self):
        """
        Returns a dictionary version of the Character and its quotes.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'age': self.age,
            'birthday': self.birthday.strftime('%Y-%m-%d') if self.birthday else None,
            'is_samurai': self.is_samurai,
            'quotes': [quote.to_dict() for quote in self.quotes.all()]
        }


class Quote(models.Model):
    """
    A quote by the character.
    """
    character = models.ForeignKey(
        Character, 
        on_delete=models.CASCADE, 
        related_name='quotes'
    )
    
    text = models.TextField()

    def __str__(self):
        """String representation."""
        return f'"{self.text[:50]}..." - {self.character.name}'

    def to_dict(self):
        """Puts the Quote into a dictionary."""
        return {
            'id': self.id,
            'character_id': self.character.id,
            'text': self.text,
        }
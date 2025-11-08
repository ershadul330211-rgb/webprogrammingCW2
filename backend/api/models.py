from django.db import models

class Character(models.Model):
    """
    Main model: Represents a single Gintama character.
    """
    # CharField
    name = models.CharField(max_length=100)
    
    # TextField
    description = models.TextField(help_text="A brief bio of the character.")
    
    # IntegerField
    age = models.IntegerField(null=True, blank=True, help_text="Can be null")
    
    # DateField
    birthday = models.DateField(null=True, blank=True, help_text="Character's birthday")
    
    # BooleanField
    is_samurai = models.BooleanField(default=False)

    def __str__(self):
        """String representation."""
        return self.name

    def to_dict(self):
        """
        Serializes the Character and its related Quotes into a dictionary
        for the JSON response.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'age': self.age,
            'birthday': self.birthday.strftime('%Y-%m-%d') if self.birthday else None,
            'is_samurai': self.is_samurai,
            # 'quotes' is the 'related_name' from the Quote model
            'quotes': [quote.to_dict() for quote in self.quotes.all()]
        }


class Quote(models.Model):
    """
    Secondary model: Represents a single quote by a character.
    """
    # ForeignKey creates the one-to-many relationship
    character = models.ForeignKey(
        Character, 
        on_delete=models.CASCADE, 
        related_name='quotes'
    )
    
    # TextField (Quotes can be long)
    text = models.TextField()

    def __str__(self):
        """String representation."""
        return f'"{self.text[:50]}..." - {self.character.name}'

    def to_dict(self):
        """Serializes the Quote into a dictionary."""
        return {
            'id': self.id,
            'character_id': self.character.id,
            'text': self.text,
        }
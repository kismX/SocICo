from django.db import models

class Terms(models.Model):
    word = models.CharField(max_length=100, unique=True)
    usage_count = models.IntegerField(default=0) # field, um such-statistiken zu erfassen
    synonyms = models.ManyToManyField('self', blank=True)  
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE, related_name='terms', null=True, blank=True) #falls wir kategorien mal brauchen, kann man dieses field nutzen

    # synonyms: die möglichkeit für synonyme irgendwann, 'self' macht hier, dass ein objekt von Term 
    # mit anderen objekten des selben term-modells (hier many-to-many) verknüpft/in beziehung gesetzt werden können
    # Beispiel: Wenn Sie ein Term-Objekt mit dem Wort "Auto" haben, können Sie ihm Synonyme wie 
    # "Kraftwagen" oder "Wagen" zuordnen, die ebenfalls Term-Objekte sind.
    # schau in doc: implementierun terms-datenbank und fuzzywuzzy
    
    def __str__(self):
        return self.word
    


# model für kategorien
class CategoryModel(models.Model):
    term_category = models.CharField(max_length=100, unique=True)
    term_category_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.term_category

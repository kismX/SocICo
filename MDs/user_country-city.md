# City und Country im UserModel

> pip install django-cities-light

Im settings.py 'cities_light' zu Apps hinzufügen und dann folgenden Command um die Datebank zu füllen:

> python manage.py cities_light

! Makemigrations und Migrate nicht vergessen !

_____________

## Ziel:

Der User soll bei der Registrierung ein Land eingeben und die dazu pasenden Städte vorgeschlagen bekommen. Dann soll der User die Möglichkeit haben dies in seinem Profil stehts ändern zu können.

______________

### Setup des Models und admin.py

```python
    # accounts/models.py
    class CustomUser(AbstractUser):
        country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True)
        city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True)
        ...
```

Wir fügen zu unserem CustomUser country und city hinzu und greifen hierbei auf die models aus der App 'cities_light' zu daher brauchen wir kein import statement.

```python
    # accounts/admin.py
    class CustomUserAdmin(UserAdmin):
        ...
        add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('name', 'country', 'city')}), )
        fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('name', 'country', 'city')}), )
```
In der admin.py müssen wir die fieldset variablen anpassen damit city und country auch auf der Adminseite angezeigt werden.
> Hier nochmal 'python manage.py makemigrations' und 'python manage.py migrate'

### Implementieren der Felder in Registrierung

Da unsere City/Country Objekte im User und nicht im Profile gespeichert werden müssen wir zuerst unser 'CustomUserCreationForm' anpassen.

```python
    # accounts/form.py
    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = CustomUser
            fields = UserCreationForm.Meta.fields + ('name', 'country', 'city' )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['city'].queryset = City.objects.none()

            if 'country' in self.data:
                try:
                    country_id = int(self.data.get('country'))
                    self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
```

Zuerst fügen wir zu 'fields' country und city hinzu. Dann überschreiben wir einen Teil der __init__ method.
Mit self.fields holen wir uns aus unseren fields variable den City-Wert und setzen ihn auf None. Das dient dazu dass keine Städte angezeigt werden sollen wenn der User noch kein Land angegeben hat.
Danach schauen wir ob ein 'country' Wert existiert:
    - (try) such nach den Städten die die selbe country-id haben wie unser eingegebenes Land und sortiere sie nach Namen
    - (except) wenn die Eingabe fehlerhaft sein sollte fall zurück zum leeren City Queryset
Ansonsten wenn es einen Primary Key gibt:
    - Setzen wir unser City Queryset gleich allen Städten sortiert nach Namen

```python
    # accounts/views.py
    from cities_light.models import City

    def load_cities(request):
        country_id = request.GET.get('country')
        cities = City.objects.filter(country_id=country_id).order_by('name')
        return render(request, 'city_dropdown_list_options.html', {'cities': cities})
```

In den views (noch bevor unsere Funktion zum händeln des Formulars aufgerufen wird (-> def profile)), fügen wir eine neue Funktion hinzu die unsere Städte lädt.
Zuerst holen wir uns die ID des Landes und nutzen diese um unsere City Objekte danach zu filtern. 
Returned wird dann die gefilterte Liste und unser neues html Dokument.

```python
    # accounts/urls.py
    path('ajax/load-cities/', load_cities, name='ajax_load_cities')
```

Der Pfad zu unserer Funktion load_cities um sie im HTML nutzen zu können.

```html
    <!-- city_dropdown_list_options.html -->
    <option value="">---------</option>
    {% for city in cities %}
    <option value="{{ city.pk }}">{{ city.name }}</option>
    {% endfor %}
```

Hier setzen wir 2 Zustände:
option value="" -> Wenn es keinen Wert gibt (z.B weil kein Land eingeben wurde)
option value="{{ city.pk }} -> Wenn eine Stadt gewht wurde übergeben wir hier den PK der Stadt

```html
    <!-- signup.html -->
    <form method="post" id="RegisterForm" data-cities-url="{% url 'ajax_load_cities' %}" novalidate>
    ...
    </form>
```

In der signup.html müssen wir nun dem Formular eine ID geben um es später ansprechen zu können und verbinden das Formular mit unserer load_cities funktion über die url 'ajax_load_cities'.

### AJAX und jQuery

```html
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script>
        $("#id_country").change(function () {
        var url = $("#RegisterForm").attr("data-cities-url");  // get the url of the `load_cities` view
        var countryId = $(this).val();  // get the selected country ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= localhost:8000/ajax/load-cities/)
            data: {
            'country': countryId       // add the country id to the GET parameters
            },
            success: function (data) {   // `data` is the return of the `load_cities` view function
            $("#id_city").html(data);  // replace the contents of the city input with the data that came from the server
            }
        });

        });
    </script>
```
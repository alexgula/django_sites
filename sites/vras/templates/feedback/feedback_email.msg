{% load future i18n markup %}{% trans "New message from feedback form!" %}

{% trans "User name" %}: {{ obj.name }}
{% trans "User phone" %}: {{ obj.phone }}
{% trans "User email" %}: {{ obj.email }}
{% trans "Post date" %}: {{ obj.post_date|date:'c' }}

------------------------------ {% trans "Message text" %} --------------------------------

{{ obj.text }}

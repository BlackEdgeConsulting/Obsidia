## Error when accessing Model - 'Model' has no 'objects' member
This happens because PyLint can't detect the properties and methods that your model, e.g. CaseFile, actually has. Typically we don't want to disable pylint warnings but this case makes sense to do. Below is an example of how to do that, which is just adding this specific comment on the line:
```py
organization = _get_current_users_organization()
tags = CaseFile.objects.filter(organization__id=organization.pk).select_related("tagSet__key") # pylint: disable=no-member
return HttpResponse(tags)
```

## 403 Error When POSTing - Forbidden (CSRF cookie not set)
Sometimes when you attempt to post to an endpoint that doesn't handle HTTP then you'll get an error of `Forbidden (CSRF cookie not set.): ...`. This can be temporarily mitigated by doing:
- `CSRF_COOKIE_SECURE = True`
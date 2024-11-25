## 0.2.0a7 (2024-11-25)

### Feat

- **Assets**: add location to assets, fix failing tables and details
- **Location**: add "up to" link to nested locations
- **LocationDetailView**: add link to parent
- **LocationAdmin**: add ContainerInline
- **AssetAttachmentForm**: try to add a form for asset attachments
- **Location**: add breadcrumbs
- **admin**: add iommi admin for assets

### Fix

- **merge**: merge upstream changes into local
- **ItemBaseModel**: remove override decorator for 3.11
- **django-extensions**: move out of optional group into main group
- **settings**: move `django_extensions` from local to base for AutoSlugField
- **iommi**: use single quotes in f-string for older python versions

### Refactor

- **Asset**: add `primary_thumbnail` property to make detail pages easier

## 0.2.0a6 (2024-11-04)

### Feat

- **iommi**: integrate iommi in several locations

### Fix

- **primary_image**: add if statement to template to not show preview if none is available
- **primary_image**: handle if no attachment

## 0.2.0a5 (2024-10-21)

### Feat

- **views**: add views/tables/thumbnails

### Fix

- **migrations**: add in empty migrations to fill some mistakes I made
- **migrations**: un-delete attachment migrations

## 0.2.0a4 (2024-10-21)

### Feat

- **attachments**: move attachments to generic attachments; improve primary_image in containers and assets
- **assets**: add assets and jazzmin

## 0.2.0a3 (2024-10-17)

### Feat

- **sorting**: allow for "primary" images on containers by using sorting on the attachments in admin

## 0.2.0a2 (2024-10-17)

### Feat

- **admin_thumbnails**: include thumbnails in admin interface for attachments

## 0.2.0a1 (2024-10-17)

### Fix

- **secrets**: add `.secret_value` to `get_secret` calls
- **django-rubble**: add missing extra `django-simple-history`

## 0.2.0a0 (2024-10-16)

### Feat

- **models**: add several models for basic functionality

### Refactor

- **ruff.toml**: separate ruff config into its own file

# Backend - CMS and Content

## Responsibilities

- CMS pages and widgets
- Banners and promotional blocks
- Translations and localization
- Content approval and audit

## Key controllers

- CMSStaticPageController, CMSBannerController
- PageConfigurationAdminController, PageConfigurationPublicController
- WidgetAdminController, WidgetTranslationController
- TranslationAdminController, TranslationPublicController
- ContentController, ContentTypeController

## Data model highlights

- PageConfiguration, PageContentWidget, WidgetTemplate
- Translations and translation keys
- Content audit logs

## Dependencies

- PostgreSQL for content storage
- Redis caches for CMS

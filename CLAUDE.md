# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CutMyCode is a Django-based code snippet sharing application. Users can create, share, and discover code snippets with syntax highlighting and temporary sharing links.

## Key Technologies & Dependencies

- **Django 5.2.3** - Main web framework
- **django-cotton** - Template component system
- **django-htmx** - HTMX integration for dynamic interactions
- **django-debug-toolbar** - Development debugging tools
- **django-environ** - Environment variable management
- **SQLite** - Default database (configurable via DATABASE_URL)

## Architecture

### App Structure

The project follows Django's app-based architecture with four main apps:

- **`apps/core/`** - Core shared functionality
- **`apps/accounts/`** - User authentication and profiles (CustomUser model)
- **`apps/snippets/`** - Code snippet management (Snippet, SharedSnippet models)
- **`apps/comments/`** - Comment system for snippets

### Key Models

- **CustomUser** - Extended Django user model with profile URLs
- **Snippet** - Core model for code snippets with title, description, code, language, and user ownership
- **SharedSnippet** - Temporary sharing system with UUID tokens and expiration (24 hours)
- **Comment** - Comments linked to snippets and users

### URL Structure

- `/` - Explore view (public snippet listing)
- `/snippets/dashboard/` - User's personal snippet dashboard
- `/snippets/create/` - Create new snippet
- `/snippets/<id>/` - View snippet details
- `/snippets/<id>/edit/` - Edit snippet (owner only)
- `/snippets/<id>/share/` - Generate temporary share link
- `/snippets/shared/<token>/` - View shared snippet via token
- `/accounts/signup/` - User registration
- `/accounts/<username>/` - User profile view

## Development Commands

### Basic Django Commands

- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create new migrations
- `python manage.py migrate` - Apply migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py shell` - Django shell
- `python manage.py collectstatic` - Collect static files

### Testing

- `python manage.py test` - Run all tests
- `python manage.py test apps.snippets` - Run specific app tests

## Configuration

### Environment Variables

The app uses django-environ for configuration. Required environment variables:

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (default: False)
- `DATABASE_URL` - Database connection string (default: sqlite:///db.sqlite3)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### Settings Structure

- `config/settings/base.py` - Main settings file
- `config/settings/dev.py` - Development overrides
- `config/settings/prod.py` - Production settings
- Default uses `config.settings.base`

## Authentication & Authorization

- Custom user model: `accounts.CustomUser`
- Login/logout URLs configured
- User ownership enforced on snippets (edit/delete)
- Share functionality creates temporary public access via UUID tokens

## Templates & Static Files

- Templates in `templates/` directory
- Uses django-cotton for component-based templating
- Static files in `static/` with CSS tokens system
- HTMX integration for dynamic interactions

## Key Features

1. **Snippet Management** - CRUD operations with syntax highlighting
2. **Temporary Sharing** - Generate shareable links that expire in 24 hours
3. **User Profiles** - Custom user model with profile pages
4. **Comments System** - Users can comment on snippets
5. **Responsive Design** - Modern CSS with design tokens
6. **Debug Toolbar** - Development debugging tools

## Common Development Patterns

### Adding New Views

Follow the existing pattern in `apps/snippets/views.py`:

- Use class-based views (ListView, DetailView, CreateView, etc.)
- Apply `LoginRequiredMixin` for authenticated views
- Use `UserPassesTestMixin` for ownership checks
- Set appropriate `template_name` and `context_object_name`

### Model Relationships

- Use `settings.AUTH_USER_MODEL` for user foreign keys
- Apply `on_delete=models.PROTECT` for user relationships
- Use `on_delete=models.CASCADE` for dependent relationships
- Include `related_name` for reverse relationships

### URL Patterns

- Use app namespaces (`app_name = "snippets"`)
- Follow RESTful patterns where applicable
- Use descriptive URL names for reverse lookups

## UI design system

### Architecture Philosophy

- **ITCSS (Inverted Triangle CSS)** for structural organization
- **CUBE CSS** for progressive enhancement philosophy
- **BEM methodology** for naming conventions
- **Modern CSS features** like Custom Properties, @layer, and clamp()
- **Vanilla-first**: No preprocessors or build tools required
- **Component-oriented**: Self-contained, reusable components
- **Semantic tokens**: Purpose-driven naming (not value-based)
- **Progressive enhancement**: Works with basic styles, enhanced by specifics
- **Modern units**: Prefer rem/em over px, use clamp() for fluid scaling

### CSS Architecture Layers (ITCSS-based)

```css
@layer reset, global, composition, components, utilities;
```

1. **reset** - CSS reset and normalization
2. **global** - Design tokens (custom properties) and base element styles
3. **composition** - Layout primitives (.wrapper, .grid-auto, .flow)
4. **components** - UI components with BEM naming (c- prefix)
5. **utilities** - Override classes (u- prefix)

### Naming Conventions (BEM style)

- **Components**: `.c-component` (e.g., `.c-button`, `.c-card`)
- **Elements**: `.c-component__element` (e.g., `.c-card__title`)
- **Modifiers**: `.c-component--modifier` (e.g., `.c-button--primary`)
- **Utilities**: `.u-utility` (e.g., `.u-text-center`)
- **Composition**: No prefix (e.g., `.wrapper`, `.flow`, `.grid`, `cluster`)

### Responsive Design Approach

- Use `clamp()` for fluid scaling: `clamp(min, preferred, max)`
- Prefer CSS Grid and Flexbox over float-based layouts
- Mobile-first approach with progressive enhancement
- Minimal media queries - rely on intrinsic sizing where possible

### Accessibility Requirements

- Semantic HTML foundation for all components
- Color contrast compliance (4.5:1 minimum)

## CSS Design Patterns

### CUBE CSS Conventions

- **Class Composition**: Use pipe (|) separator to show class composition

  - Example: `c-header | wrapper | u-pad-l` showing:
    - Component class (c-header)
    - Layout primitive (wrapper)
    - Utility classes (u-pad-l)

- **Separation of concerns**: Each component is built on a primitive and carries styles

  - e.g. `c-tags | cluster | u-pad-m` indicates that the component tags is a cluster that's padded and carries some styles that will be defined in the c-tags.
  - the components themselves shouldn't house any layout/spacing (pad/margin etc) related styles as these responsibilities are for primitives and utilities.
  - If we some element becoming too long in the html: `c-comp__elem | wrapper | u-pad-m u-bg-secondary u-border-top u-text-mute` in this case, it's wise to incorporate the styles that the utilities perform within the c-comp\_\_elem style, such that we only need to do `c-comp_elem | wrapper | u-pad-m`

- **Composition over Specificity**:

  - Layout handled by primitives (`.wrapper`, `.stack`, `.grid`)
  - Aesthetics handled by components (`.c-header`, `.c-button`)
  - One-off adjustments use utilities (`.u-pad-l`, `.u-border-bot`)

- **Refactoring Pattern**:

  - When common utility patterns emerge, refactor into component
  - Reduces repetitive utility usage in HTML

- **BEM for Modifiers**:
  - Use BEM-style modifiers for layout (`.grid--2`)
  - Use BEM-style modifiers for components (`.c-button--primary`)

### Benefits of This Architecture

- Scales well (clear separation of concerns)
- Maintainable (predictable patterns)
- Composable (styles + primitives)
- Flexible (custom properties for overrides)
- Follows modern CSS best practices


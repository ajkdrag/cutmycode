# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based code snippet sharing application called "cutmycode" that follows Clean Architecture principles. The application allows users to create, share, and manage code snippets with syntax highlighting.

## Architecture

The codebase follows a layered architecture with clear separation of concerns:

- **`src/domain/`**: Core business logic layer

  - `entities.py`: Domain entities (User, Snippet, Comment, Like) as dataclasses
  - `repositories/`: Abstract repository interfaces
  - `policies.py`: Business rules and authorization logic
  - `constants.py`: Domain constants like Language choices

- **`src/usecases/`**: Application services layer

  - `snippets.py`: Snippet-related business operations
  - `social.py`: Social features (likes, comments)
  - Functions return response dataclasses and accept repository dependencies

- **`src/data/orm/`**: Data access layer

  - `models.py`: Django ORM models (CustomUser, Snippet)
  - `repositories/`: Concrete implementations of domain repository interfaces
  - Uses repository pattern to abstract Django ORM from business logic

- **`src/interfaces/web/`**: Web interface layer
  - `views/`: Django view functions that orchestrate use cases
  - `forms/`: Django forms for user input validation
  - `templates/`: HTML templates using Django Cotton components
  - `static/`: CSS organized in tokens/utilities/components structure

## Development Commands

```bash
# Start development server
python manage.py runserver

# Run database migrations
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Key Patterns

1. **Repository Pattern**: Domain repositories define interfaces, ORM repositories implement them
2. **Use Case Functions**: Business logic organized as pure functions accepting dependencies
3. **Policy Objects**: Authorization and business rules encapsulated in policy classes
4. **Response Dataclasses**: Use cases return structured response objects
5. **Entity Mapping**: ORM repositories convert between Django models and domain entities

## Dependencies

- Django 5.2+ with DRF
- django-cotton for component-based templates
- django-environ for environment configuration
- Pygments for syntax highlighting
- UV for dependency management

## Configuration

- Settings use environment variables via django-environ
- Database: SQLite by default, configurable via DATABASE_URL
- Custom user model: `orm.CustomUser`
- Templates located in `src/interfaces/web/templates/`
- Static files in `src/interfaces/web/static/`

## Testing

No test framework is currently configured. When adding tests, consider the layered architecture and test each layer appropriately.

## Code Memory

- Data flow follows a unidirectional path:
  - Web interface (views) calls use cases
  - Use cases interact with domain repositories
  - Repositories fetch/persist data through ORM models
  - Entities are mapped between layers to maintain separation of concerns
- Actions are performed by passing data and dependencies through each architectural layer
  - Web views receive HTTP requests
  - Use cases process business logic
  - Repositories handle data persistence
  - Policies enforce business rules and authorization

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


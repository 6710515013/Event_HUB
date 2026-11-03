# EventHub Project Structure

This repository uses Django apps separated by responsibility.

```text
Event_HUB/
├── accounts/                 # Existing login, registration and account/profile features
├── events/                   # Event model; Organizer event management; Student event browsing
│   └── templates/events/
│       ├── management/       # Organizer event pages
│       └── browse/           # Student event pages
├── registrations/            # Internal student registration and registration history
├── dashboard/                # Student and Organizer dashboards
├── event_hub/                # Django project settings and root URL configuration
├── templates/                # Shared templates (base.html, shared navigation, footer)
└── static/
    ├── css/                  # Shared styles
    ├── js/                   # Shared JavaScript
    └── images/               # Shared images
```

## Important decisions

- Do not create a separate `clubs` app or Club model. Organizer enters the club/organization name as text when creating an event; store it on the Event.
- Keep the existing Login/Register implementation in `accounts`.
- Organizer manages only their own events.
- Student browsing displays events that are published/open.
- Closing registration must not delete the event or its registration history.
- An event may use internal registration or an external form URL. External form responses do not automatically become internal Registration records.

## App ownership

| App / area | Main responsibility |
|---|---|
| `accounts` | Existing authentication and Organizer profile/account management |
| `events` | Event data, Organizer CRUD, Student browsing |
| `registrations` | Internal registration, capacity checks, history |
| `dashboard` | Student and Organizer dashboard summaries |
| Shared templates/static + project config | Base layout, styling, root URL integration |

See the team task split agreed in the project discussion before changing shared models or settings.

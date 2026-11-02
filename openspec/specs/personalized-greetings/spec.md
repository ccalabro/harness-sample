# Personalized Greetings

## Purpose

Personalized greetings make the starter application respond to a person's name. This capability defines a small, testable input and output contract.

## Requirements

### Requirement: Greet a person by name

The application SHALL return `Hello, <name>!` for a nonblank name after trimming leading and trailing whitespace. It SHALL preserve the name's capitalization and internal spaces.

#### Scenario: Greet a named person

- **WHEN** a caller provides `Ada Lovelace`
- **THEN** the application returns `Hello, Ada Lovelace!`

#### Scenario: Trim surrounding whitespace

- **WHEN** a caller provides `  Ada Lovelace  `
- **THEN** the application returns `Hello, Ada Lovelace!`

### Requirement: Reject blank names

The application SHALL raise `ValueError` with the message `name must not be blank` when the supplied name is empty or contains only whitespace.

#### Scenario: Reject an empty name

- **WHEN** a caller provides an empty name
- **THEN** the application raises `ValueError` with the message `name must not be blank`

#### Scenario: Reject a whitespace-only name

- **WHEN** a caller provides a name containing only spaces or tabs
- **THEN** the application raises `ValueError` with the message `name must not be blank`

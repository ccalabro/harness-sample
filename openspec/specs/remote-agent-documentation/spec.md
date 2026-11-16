# remote-agent-documentation Specification

## Purpose

Document how agent plans and builds can run remotely and hand off draft pull requests for human review.

## Requirements

### Requirement: Final README section describes remote agent work

README.md SHALL end with a section titled exactly `## Running agents remotely`, after the existing Contact section. The section SHALL contain the following two sentences in American English:

Plans and builds can run headlessly on a dedicated machine. The resulting changes can be opened as draft pull requests for human review.

#### Scenario: A reader reaches the end of the README

- **WHEN** a reader reaches the end of README.md
- **THEN** the final section heading is `## Running agents remotely`
- **AND** its two sentences explain headless plans and builds on a dedicated machine and draft pull requests for human review using the exact wording above

### Requirement: Documentation-only scope

The product change SHALL be limited to appending the specified section to README.md, preserving its existing content. It SHALL NOT change code, dependencies, configuration, or runtime behavior or create a pull request. Workflow specification and review artifacts MAY be maintained separately as required by the repository process.

#### Scenario: The change is reviewed

- **WHEN** the product diff is inspected
- **THEN** README.md contains only the appended section and the separating whitespace needed for valid Markdown
- **AND** no code, dependency, configuration, or runtime behavior changes are present

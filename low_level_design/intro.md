# Low Level Design
It is where the code starts to take shape.
Bridge b/w the architecture and actual implementation.
When we get into extreme details.

Key Characteristics of LLD:
- Granular and code level
- Implementation focus
- Applying OOPs principles

Why LLD is important:
- avoids rework
- improves collaboration
- Promotes scalability
- Encourages best practices

# Principles of Software Design

1. DRY (Donot Repeat Yourself) Principle
- Each piece of logic or knowledge should have a single, unambiguous representation within the system.
Importance:
 - reduces redundancy
 - Easier Maintainance
 - Single point of change

How to apply?
- Identify repetitive code -> replace it with single, reusable code segement.
- Extract common functionality into methods or utility classes
- Leverage libraries and frameworks -> no need of reinventing the wheel
- refactor duplicate logic regularly across classes or layers


2. KISS (Keep It Simple, Stupid) Principle
- A design should be kept as simple as possible, Complexity should only be introduced when absolutely necessary.
Importance:
 - Easier debugging
 - improved readability
 - better maintainability
 - faster development


3. YAGNI (You Aren't Gonna Need It) Principle
- Always implement things when you actually need them, never when you just forsee that you might need them.
- In simple terms, don't add functionality until it's necessary. Avoid building features that you think you might need in the future.
Importance:
 - reduced waste
 - simplified codebase
 - faster development

When not to follow:
 - When the requirements are well-known
 - Performance critical area

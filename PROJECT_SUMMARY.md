# InnovatEPAM Portal - Project Summary

## 1) Brief Project Overview
InnovatEPAM Portal is a web application designed to provide secure system access for users with different roles while establishing a solid foundation for future portal and submission workflows. At this stage, the primary focus was building the first working slice of the product: the **MVP authentication (Auth)** layer, implemented with sound engineering practices.

## 2) Completed MVP Features (Auth System)
In this iteration, the following core Auth capabilities were completed:

- **Register:** Create a new user account
- **Login:** Authenticate user credentials and grant access
- **Logout:** End session and support token revocation flow
- **Current User (Me):** Return the profile of the authenticated user
- **Token Architecture:** Access + Refresh token model
- **Authorization and Error Handling Base:** Consistent handling of unauthorized and invalid-credential scenarios

This scope provides a secure and testable core for the remaining product modules.

## 3) Technology Stack
The MVP was developed using the following core technologies:

- **Backend:** FastAPI (Python)
- **Frontend:** React
- **Testing:** Pytest

This combination enables rapid API development, a modern client experience, and strong automated testing practices.

## 4) Personal Learnings: From Vibe Coding to Spec-Driven Development
The most important shift in this project was moving from a "code-first" reflex to a "specification-first" discipline. While Vibe Coding can feel fast, decisions may remain too ad hoc, which increases scope drift, requirement ambiguity, and rework cost. With Spec-Driven Development:

- Requirements were clarified up front,
- Plans and tasks were defined together with a testing strategy,
- Implementation progressed according to explicit contracts and scenarios.

As a result, development evolved from producing merely "working code" to delivering "verifiably correct behavior."

## 5) Impact of TDD and Constitution on Code Quality
Two major levers significantly improved quality in this project: **TDD** and the **Constitution**.

### TDD impact
- The RED -> GREEN -> REFACTOR cycle exposed defects early.
- Features were implemented against explicit, test-driven behavior.
- Refactoring became safer because tests acted as a regression safety net.

### Constitution impact
- Team and individual standards became explicit and non-optional.
- The testing pyramid discipline (unit/integration/e2e balance) was preserved.
- Process quality became mandatory, not only feature completion.

Together, these practices noticeably improved maintainability, readability, and reliability. The key gain was embedding quality directly into day-to-day development instead of deferring it to the end of a sprint.

## 6) Conclusion
The completed Auth MVP for InnovatEPAM Portal is not only a functional starting point; it is also the first concrete outcome of a specification-driven, test-guided, and quality-governed engineering culture. This foundation enables lower-risk progress for upcoming user management and role-based authorization features.

# OCW Downloader System Analysis Document

## Executive Summary

The OCW Downloader System is a content acquisition and organization solution designed to systematically download and persist OpenCourseWare materials. The system interfaces with multiple OCW APIs to retrieve course metadata, hierarchical content structure, and binary session files, organizing them into a deterministic filesystem structure. This architecture enables reliable, repeatable downloads with human-readable directory organization following the pattern: `course_title/chapter_sort__chapter_title/session_sort__session_title.ext`.

## System Overview

### Core Components

The system architecture comprises five primary components working in orchestrated harmony:

1. #### User/CLI Interface

- Entry point for system interaction
- Accepts courseId as primary input parameter
- Receives status updates and completion summaries

1. #### Downloader (Spider/Worker)

- Central orchestration engine
- Manages API communication sequencing
- Handles error recovery and retry logic
- Implements deterministic path generation algorithm

1. #### OCW API Suite

- **Course API**: Provides course-level metadata (title, type)
- **Sessions API**: Returns hierarchical content structure with sort ordering
- **Sessions Link**: Binary content delivery endpoint

1. #### Local Storage (File System)

- Persistent storage layer
- Maintains hierarchical directory structure
- Preserves content with deterministic naming convention

### Component Interaction Diagram

```plantuml
@startuml
title OCW Downloader — System Architecture

!define RECTANGLE_COLOR #E1F5FE
!define API_COLOR #FFF3E0
!define STORAGE_COLOR #E8F5E9
!define WORKER_COLOR #F3E5F5

left to right direction
skinparam componentStyle rectangle
skinparam wrapWidth 220
skinparam maxMessageSize 220
skinparam arrowColor #abb2bf
skinparam actorBackgroundColor #61afef
skinparam componentBackgroundColor #2c323c
skinparam componentBorderColor #61afef
skinparam databaseBackgroundColor #2c323c
skinparam databaseBorderColor #98c379
skinparam nodeBackgroundColor #2c323c
skinparam nodeBorderColor #e06c75


' Dark Mode Theme
skinparam backgroundColor #282c34
skinparam defaultTextAlignment left
skinparam noteTextAlignment left
skinparam ArrowColor #abb2bf
skinparam NoteBorderColor #61afef
skinparam NoteBackgroundColor #2c323c
skinparam NoteFontColor #abb2bf
skinparam Nodesep 100
skinparam Ranksep 100
skinparam Dpi 96
skinparam PageMargin 150
skinparam BoxPadding 150



actor "User/CLI" as User #61afef
component "Downloader\n(Spider/Worker)" as D <<core>> #2c323c

node "OCW API Gateway" as API #2c323c {
  component "Course API\nPOST /api/v1/ocw/course/get" as CourseAPI #2c323c
  component "Sessions API\nPOST /api/v1/ocw/sessions" as SessionsAPI #2c323c
  component "Session Link\nGET /cms/ocw/session_link" as SessionLink #2c323c
}

database "Local Storage\n(File System)" as FS #2c323c

User -[#61afef]-> D : courseId
D -[#e06c75]-> CourseAPI : POST {"id": courseId}
CourseAPI -[#98c379]-> D : {title, type}

D -[#e06c75]-> SessionsAPI : POST {\n  "limit": null,\n  "order_type": "ASC",\n  "course_id": courseId,\n  "status": ["free","non-free"]\n}
SessionsAPI -[#98c379]-> D : chapters[] {title, sort,\n  sessions[] {title, link, type, sort}}

D -[#e06c75]-> SessionLink : GET session.link\n(per session)
SessionLink -[#98c379]-> D : binary content

D -UP[#c678dd]-> FS : save as\ncourse_title/\n  chapter_sort__chapter_title/\n    session_sort__session_title.ext

note bottom of D #2c323c
  <color:#abb2bf>Orchestrates entire workflow
  Implements retry logic
  Handles path generation</color>
end note

note top of API #2c323c
  <color:#abb2bf>RESTful API endpoints
  JSON request/response
  Binary content delivery</color>
end note
@enduml
```

## Interaction Analysis

The system demonstrates a well-structured service-oriented architecture with clear separation of concerns:

### Key Interaction Patterns

1. **Sequential Dependency Chain**: Course metadata must be retrieved before session listing, establishing a critical path for data acquisition
2. **Hierarchical Data Resolution**: The Sessions API provides complete navigational structure in a single response, minimizing API calls
3. **Parallel Download Capability**: Individual session downloads are independent, enabling potential parallelization
4. **Deterministic Path Generation**: Sort keys ensure consistent, reproducible filesystem organization across multiple executions

### Communication Protocols

- **Metadata APIs**: JSON-based POST requests with structured payloads
- **Binary Endpoint**: Simple GET requests with URL-based session identification
- **Error Handling**: Non-blocking session failures with graceful degradation

## Process Flow Analysis

### Sequence Diagram

```plantuml
@startuml
title OCW Downloader — Process Flow

' Dark Mode Theme
skinparam backgroundColor #282c34
skinparam defaultTextAlignment left
skinparam noteTextAlignment left
skinparam ArrowColor #abb2bf
skinparam NoteBorderColor #61afef
skinparam NoteBackgroundColor #2c323c
skinparam NoteFontColor #abb2bf
skinparam Nodesep 100
skinparam Ranksep 100
skinparam Dpi 96
skinparam PageMargin 150
skinparam BoxPadding 150

skinparam sequenceArrowColor #0f58e0
skinparam sequenceLifeLineBorderColor #4b5263
skinparam sequenceParticipantBackgroundColor #2c323c
skinparam sequenceParticipantBorderColor #61afef
skinparam sequenceActorBackgroundColor #2c323c
skinparam sequenceActorBorderColor #61afef
skinparam sequenceGroupBackgroundColor #2c323c
skinparam sequenceGroupBorderColor #61afef
skinparam sequenceGroupHeaderFontColor #61afef
skinparam sequenceDividerBackgroundColor #2c323c
skinparam sequenceDividerBorderColor #61afef
skinparam sequenceDividerFontColor #61afef
skinparam sequenceLifeLineBackgroundColor #2c323c

autonumber "<b>[00]"
actor Client #61afef
participant "Downloader\n(Spider/Worker)" as D #c678dd
participant "Course API\nPOST /api/v1/ocw/course/get" as CourseAPI #e06c75
participant "Sessions API\nPOST /api/v1/ocw/sessions" as SessionsAPI #e06c75
participant "Session Link\nGET /cms/ocw/session_link" as CMS #e06c75
database "File System" as FS #98c379

== Initialization ==
Client -> D : start(courseId)
activate D

== Phase 1: Course Metadata Retrieval ==
group #2c323c Fetch Course Metadata
  D -> CourseAPI : POST { "id": courseId }
  activate CourseAPI
  alt #98c379 Success [200 OK]
    CourseAPI --> D : { title: "Data Structures", type: "undergraduate" }
    note right #2c323c: Course metadata fetched\nfor directory naming
  else #e06c75 Error [4xx/5xx]
    CourseAPI --> D : 4xx/5xx
    deactivate CourseAPI
    D --> Client : ERROR: Course fetch failed
    deactivate D
    return
  end
  deactivate CourseAPI
end

== Phase 2: Content Hierarchy Discovery ==
group #2c323c Fetch Chapter/Session Hierarchy
  D -> SessionsAPI : POST {\n "limit": null,\n "order_type": "ASC",\n "course_id": courseId,\n "status": ["free","non-free"]\n}
  activate SessionsAPI
  alt #98c379 Success [200 OK]
    SessionsAPI --> D : chapters[] { title, sort,\n  sessions[] { title, link, type, sort } }
    note right #2c323c: Complete hierarchy\nretrieved in single call
  else #e06c75 Error [4xx/5xx]
    SessionsAPI --> D : 4xx/5xx
    deactivate SessionsAPI
    D --> Client : ERROR: Sessions fetch failed
    deactivate D
    return
  end
  deactivate SessionsAPI
end

== Phase 3: Content Download Execution ==
group #2c323c Download Sessions (Ordered Processing)
  loop for each chapter (ascending by sort)
    note over D #2c323c: Create chapter directory\nif not exists
    loop for each session (ascending by sort)
      D -> CMS : GET session.link
      activate CMS
      alt #98c379 Success [200 OK]
        CMS --> D : content bytes
        deactivate CMS
        D -> FS : write course_title/\n chapter_sort__chapter_title/\n  session_sort__session_title.ext
        activate FS
        FS --> D : write confirmation
        deactivate FS
        note right #2c323c: Path deterministically\ngenerated from metadata
      else #e06c75 Error [4xx/5xx]
        CMS --> D : 4xx/5xx
        deactivate CMS
        D --> Client : WARN: Session skipped
        note right #2c323c: Continue with\nnext session
      end
    end
  end
end

== Completion ==
D --> Client : done(summary: {\n  total_sessions: 47,\n  successful_downloads: 45,\n  failed_downloads: 2,\n  target_paths: "./Data_Structures/"\n})
deactivate D
@enduml
```

### Process Flow Characteristics

1. **Three-Phase Execution Model**:

    - **Phase 1**: Course metadata acquisition (blocking)
    - **Phase 2**: Session hierarchy retrieval (blocking)
    - **Phase 3**: Content download (non-blocking per session)

2. **Error Recovery Strategy**:

    - Critical failures (Phases 1-2): Terminate execution
    - Non-critical failures (Phase 3): Log and continue

## Data Model Analysis

### API Data Model Diagram

```plantuml
@startuml
title OCW API Data Model

' Dark Mode Theme
skinparam backgroundColor #282c34
skinparam defaultTextAlignment left
skinparam noteTextAlignment left
skinparam ArrowColor #abb2bf
skinparam NoteBorderColor #61afef
skinparam NoteBackgroundColor #2c323c
skinparam NoteFontColor #abb2bf
skinparam Nodesep 100
skinparam Ranksep 100
skinparam Dpi 96
skinparam PageMargin 150
skinparam BoxPadding 150

skinparam classBackgroundColor #2c323c
skinparam classBorderColor #61afef
skinparam classAttributeIconSize 0
skinparam classFontStyle bold
skinparam classFontColor #abb2bf
skinparam arrowColor #98c379
skinparam entityBackgroundColor #2c323c
skinparam entityBorderColor #61afef
skinparam entityFontColor #abb2bf
skinparam entityAttributeFontColor #abb2bf
skinparam packageBackgroundColor #2c323c
hide empty methods

entity "Course" as Course <<Entity>> #2c323c {
  <color:#61afef>title</color> : String [NOT NULL]
  --
  <color:#abb2bf><i>Constraints:</i>
  • Title used for root directory
}

entity "Chapter" as Chapter <<Entity>> #2c323c {
  <color:#61afef>title</color> : String [NOT NULL]
  <color:#e06c75>sort</color> : Integer [UNIQUE per course]
  --
  <color:#abb2bf><i>Constraints:</i>
  • Sort determines processing order
  • Sort used in directory naming
  • No direct content storage</color>
}

entity "Session" as Session <<Entity>> #2c323c {
  <color:#61afef>title</color> : String [NOT NULL]
  <color:#c678dd>link</color> : URL [NOT NULL]
  <color:#c678dd>ext</color> : String
  <color:#e06c75>sort</color> : Integer [UNIQUE per chapter]
  --
  <color:#abb2bf><i>Constraints:</i></color>
  <color:SUBTEXT_COLOR>• Link points to binary content</color>
  <color:SUBTEXT_COLOR>• Sort ensures consistent ordering</color>
  <color:SUBTEXT_COLOR>• Ext derived from Link</color>
}


Chapter ||-R-o{ Session : "contains\n(1:N)"   #98c379

note top of Course #2c323c
<color:#abb2bf><b>Primary Entity</b>
Identified by external courseId
Retrieved via Course API
Forms root of storage hierarchy</color>
end note

note top of Chapter #2c323c
<color:#abb2bf><b>Organizational Container</b>
Groups related sessions
Sort-prefixed directory naming
No direct downloadable content</color>
end note

note bottom of Session #2c323c
<color:#abb2bf><b>Content Unit</b>
Atomic downloadable resource
Binary content via link URL
Sort-prefixed file naming</color>
end note

note as StorageFormula #2c323c
<color:#abb2bf><b>Storage Path Generation Algorithm:</b>
<code>
Path = {course.title}/
       {chapter.sort}__{chapter.title}/
       {session.sort}__{session.title}.{ext}
</code>

<b>Example:</b>
<code>
"Introduction to Python/
 01__Getting Started/
 01__Installation Guide.pdf"
</code></color>
end note

StorageFormula .. Session
@enduml
```

### Data Model Insights

#### Schema Characteristics

1. ##### Course Schema

    - Key attributes: title (directory naming)

2. ##### Chapter Schema

    - Organizational unit without direct content
    - Sort attribute ensures deterministic ordering
    - Relationship: Children (Sessions)

3. ##### Session Schema

    - Atomic content unit with downloadable resource
    - Link attribute provides content access URL
    - Sort attribute maintains consistent ordering within chapter

#### Data Integrity Considerations

- Sort values must be unique within their scope (course/chapter)
- Path generation algorithm ensures filesystem compatibility

**Aim**

The aim of this project is to develop a web application called "Unit Set Builder" for the University of Western Australia (UWA). This application will feature a user-friendly interface designed to manage various types of unit sets associated with courses or majors. The system is intended to replace some functionality of the existing "Caidi" system, focusing on an improved UI/UX that handles complex scenarios, including nested groups with unique attributes, and to produce outputs that are easily understood by users. An API will be developed to output unit set data in a JSON format, which will be used in various UWA platforms such as the UWA Handbook, future students' website, marketing materials, and study planners.

**Background**

The University of Western Australia currently uses a system called "Caidi" to manage unit sets for its courses and majors. The existing system has several limitations, particularly in its user interface, which the client has identified as a significant pain point. The new system must be user-friendly for academic staff who will input data and produce outputs that are accessible to students, especially those without an IT background. The client also recommended reviewing how other universities, structure their unit sets to gain insights for this project.

**User Stories:**

1.  As a Teaching Staff, I want to create and manage unit sets with nested groups so that I can accurately represent the structure of courses and majors, including bridging, core, and optional units.
2.  As a Teaching Staff, I want to view and edit unit sets linked to specific courses, allowing for efficient updates and maintenance.
3.  As a Teaching Staff, I want an intuitive and responsive UI/UX that simplifies the process of building and modifying unit sets, reducing the time and effort required.
4.  As a developer, I need an API that outputs unit set data in a JSON format so that I can easily integrate it with other university systems.
5.  As an administrator, I want to be able to query the system to retrieve unit set information related to study planning, ensuring that I can make informed decisions.
6.  As a prospective student, I want to easily understand the unit set information presented to me, so that I can plan my studies effectively without needing an IT background.

**Software Requirements:**

1.  User Interface/Experience (UI/UX):

-   Design a clean, intuitive UI that is user-friendly and accessible.
-   Implement functionality for creating and modifying nested groups within unit sets.
-   Ensure the output is presented in a simplified, understandable format for students with varying levels of IT knowledge.

3.  Data Structure:

-   Develop a flexible and scalable data structure capable of handling complex nested unit sets with unique attributes per group and element.
-   Ensure the data structure supports efficient querying, particularly for study planning purposes.

5.  API Development:

-   Create an API that outputs unit set data in a JSON format.
-   Ensure the API is well-documented and supports integration with other university systems, including the UWA Handbook, study planners, and marketing materials.

7.  Backend and Database:

-   Implement a backend system that securely manages unit set data, including user authentication and role-based access control.
-   Use a database system that can efficiently store and retrieve complex nested data structures.

9.  Performance and Optimization:

-   Optimize the application for fast loading times and responsiveness, even with large datasets.
-   Implement caching strategies to reduce server load and improve performance for frequently accessed data.

11. Deployment and Maintenance:

-   Plan for seamless deployment with minimal disruption to users.
-   Provide documentation and training for administrators and end-users.
-   Establish a maintenance plan for ongoing support and updates.
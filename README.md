# Henna

## Table of Contents

1. [Introduction](#introduction)
2. [Objective](#objective)
3. [Key Features](#key-features)
    - [Navigation](#navigation)
    - [Home Page](#home-page)
    - [Profile Page](#profile-page)
    - [Admin Panel Feature](#admin-panel-feature)
    - [Booking Page](#booking-page)
4. [UX/UI](#uxui)
    - [User Stories](#user-stories)
        - [New Visitor](#new-visitor)
        - [Returning User](#returning-user)
        - [Frequent User](#frequent-user)
        - [Admin](#admin)
    - [Colour Scheme](#colour-scheme)
        - [Primary Colour](#primary-colour)
        - [Secondary Colour](#secondary-colour)
        - [Accent Colour](#accent-colour)
        - [Supporting Colours](#supporting-colours)
        - [Background Colour](#background-colour)
    - [Typography](#typography)
5. [Wireframes](#wireframes)
    - [Home Page](#home-page1)
6. [UML Use Case Diagram](#uml-use-case-diagram)
7. [Database](#database)
    - [Entity-Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Planned Improvements](#planned-improvements)
11. [Tools and Technologies Used](#tools-and-technologies-used)
12. [Credits](#credits)
13. [Acknowledgments](#acknowledgments)

---


## Introduction
Welcome to Henna, my Milestone Project 4 for the Level 5 Diploma in Full Stack Web Application Development! <br>
This project will demonstrate my full-stack web development skills by creating a seamless and user-friendly platform <br>
for booking henna services and purchasing henna products.

![mockup](documentation/images/readme/mock-up-p1.png)

**Live Site:**  https://henna-9c8a6d07b833.herokuapp.com/

## Objective
The main aim of Henna is to offer a seamless, intuitive, and engaging experience for clients looking to book henna services and buy henna products. The application uses modern web technologies to provide a dynamic solution that meets both personal and commercial needs.

## Key Features

- **User Management:** Allows users to register, log in, and manage their accounts easily.

- **Product Purchasing:** Offers a detailed catalogue of henna products, with features to add items to a cart and proceed through a secure checkout process.

- **Secure Payments:** Integrates Stripe for safe and efficient payment handling.

- **Media Storage:** Utilises Amazon S3 for reliable and scalable storage of media files, such as images of henna designs and product photos.

- **Admin Panel:** Provides administrators with tools to manage service listings, product inventories, and user accounts.

### Navigation
![navbar](documentation/images/readme/navbar.png)

![Small Nav](documentation/images/readme/sm-navbar.png)

![nav1](documentation/images/readme/nav1.png)

![nav3](documentation/images/readme/nav2.png)

### Home Page

![Home Page ](documentation/images/readme/hompage.png)

### Profile Page

![profile page](documentation/images/readme/profilepage.png)

### Admin Panel Feature

![admin](documentation/images/readme/admin.png) 

![admin4](documentation/images/readme/admin4.png)

![admin2](documentation/images/readme/admin2.png)

![admin3](documentation/images/readme/admin3.png)

 
## UX/UI
### User Stories

**New Visitor**
- As a first-time visitor, I want to explore the available henna services and products without needing to create an account, so I can decide if I’m interested in what’s on offer.

- As a first-time visitor, I want to see detailed information about each service and product, including prices and customer reviews, so I can make an informed decision.

- As a first-time visitor, I want to sign up easily using my email or social media accounts, so I can quickly access all features of the platform.

- As a first-time visitor, I want to receive a discount code for my first booking or purchase, so I feel encouraged to try the service.

**As a Returning User**
- As a returning user, I want to log in quickly to my account with saved credentials, so I can continue where I left off.

- As a returning user, I want to see the items I previously added to my cart, so I can easily pick up my shopping where I left off.

- As a returning user, I want to view my past bookings and purchases, so I can reorder products or rebook services I liked.

- As a returning user, I want to be informed about any special offers or discounts available to returning customers, so I feel valued and motivated to complete a purchase.

**As a Frequent User**
-  As a frequent user, I want to rebook my favourite henna artist service quickly, so I can save time and effort.
Loyalty Programme:

- As a frequent user, I want to earn loyalty points or rewards with each booking or purchase, so I feel appreciated and encouraged to keep using the app.

- As a frequent user, I want to receive personalised offers and discounts based on my history, so I can enjoy special perks tailored to my preferences.
Quick Access to History:

- As a frequent user, I want to access my full booking and purchase history easily, so I can track my activity and reorder or rebook with minimal effort.

**As an Admin**
- As an admin, I want to add, update, or remove services and products from the catalogue, so I can keep the offerings current and relevant.

- As an admin, I want to view and manage user accounts, including resetting passwords and handling account issues, so I can ensure a smooth user experience.

- As an admin, I want to view and manage all orders and bookings, including processing refunds and handling cancellations, so I can maintain efficient operations.

- As an admin, I want to create and manage discount codes and promotions, so I can attract more customers and drive sales.

---

### Colour Scheme
![henna-coolors](documentation/images/design/henna2.png)
For the Henna web application, I’ve selected a streamlined colour scheme to ensure both style and readability:

#### **Primary Colour**

- **Deep Burgundy (#6D4C53)**
  - *Usage:* Main accents, buttons, links.
  - *Reason:* Offers a rich and elegant appearance, perfect for highlighting key elements.

#### **Secondary Colour**

- **Warm Sand (#D4A78D)**
  - *Usage:* Backgrounds, cards, and highlights.
  - *Reason:* Provides a warm, neutral backdrop that complements the primary colour and creates a calming effect.

#### **Accent Colour**

- **Golden Ochre (#F6C857)**
  - *Usage:* Call-to-action buttons, highlights, and active elements.
  - *Reason:* Adds a vibrant contrast that draws attention to important actions and features.

#### **Supporting Colours**

- **Soft Olive (#9B8A5B)** and **Charcoal Grey (#4A4A4A)**
  - *Usage:* Secondary buttons, text, and subtle details.
  - *Reason:* Enhances contrast and readability without overpowering the primary palette.

#### **Background Colour**

- **Light Beige (#F9F7F1)**
  - *Usage:* Main background.
  - *Reason:* Ensures a clean, unobtrusive backdrop that enhances overall readability.

---
### Branding

![brand-logo](documentation/images/brand/brand-logo.png)

-  **Logo**
![logo1](documentation/images/brand/logo-color.png)
![logo2](documentation/images/brand/logo-black.png)
![logo3](documentation/images/brand/logo-white.png)
![logo4](documentation/images/brand/logo-no-background.png)

-  **Favicon**

![favicon1](documentation/images/brand/henna-store-favicon-black.png)
![favicon2](documentation/images/brand/henna-store-favicon-color.png)

### Typography

I’ve selected five different fonts for the Henna web application to achieve a visually appealing and functional design that enhances the user experience. Each font has a specific role: 

- **[Playfair Display](https://fonts.google.com/specimen/Playfair+Display)** adds elegance to headings.
![playfair-display](documentation/images/design/playfair-display.png)

- **[Lora](https://fonts.google.com/specimen/Lora)** provides readability for body text.
![lora](documentation/images/design/lora.png)

- **[Castoro Titling](https://fonts.google.com/specimen/Castoro+Titling)** offers a modern touch for subheadings and UI elements.
![castoro](documentation/images/design/castoro.png)

- **[Open Sans](https://fonts.google.com/specimen/Open+Sans)** ensures clarity and accessibility for general content.
![open-sans](documentation/images/design/open-sans.png)

- **[Pacifico](https://fonts.google.com/specimen/Pacifico)** adds a unique character to decorative elements.
![pacifico](documentation/images/design/pacifico.png)

---

### Wireframes

#### Home Page
![home-page-wireframe](documentation/images/wireframe/home-page-wf.png)

####  Products Page 
![product-page-wireframe](documentation/images/wireframe/prod-page-wf.png)

-  **Product Details Page**
![product-details-page-wireframe](documentation/images/wireframe/prod-details-page-wf.png)


#### Dashboards

-  **User Dashboard**
![user-dashboard-page-wireframe](documentation/images/wireframe/user-dash-wf.png)

-  **Admin Dashboard**
![admin-dashboard-page-wireframe](documentation/images/wireframe/admin-dash-wf.png)


## UML Use Case Diagram

I have created the UML Use Case Diagram to depict how different types of users and administrators interact with the system. The diagram features actors such as New Visitor, Registered User (including Returning User and Frequent User), and Admin. It outlines essential functionalities like browsing products, managing services and orders, processing payments, and handling user accounts. I have used `<<include>>` to show mandatory interactions and `<<extend>>` for optional ones, providing a clear overview of how these components are connected.

Below is the diagram image for a visual representation:

![henna-uml-use-case](documentation/images/uml/henna-uml.jpeg)

## Database

For development, I utilised the SQLite3 database, as it is the default option for Django projects and is straightforward to set up in a development environment. When the site moves to Heroku, I will switch to PostgreSQL, provided by Code Institute. PostgreSQL is better suited for production, delivering enhanced performance, scalability, and efficient management of larger datasets and multiple users.

---

### Entity-Relationship Diagram (ERD)

The Entity-Relationship Diagram (ERD) for this project provides a clear representation of the database structure. It shows how key entities such as users, roles, profiles, services, products, orders, bookings, and reviews are related to each other. The diagram helps define how data will be organised and managed within the application, ensuring smooth operation and scalability.

![henna-erd](documentation/images/uml/p2-1.png)

The ERD includes the following relationships:


## Models Overview

### 1. User and Profile
- **AuthUser**: Represents the users of the store with fields for authentication (username, password, email) and personal information (first/last name).
- **ProfilesUserprofile**: Stores additional personal details for each user, linked to a single `AuthUser` (One-to-One relationship).

### 2. Orders
- **CheckoutOrder**: Captures order details, including customer information (name, email), order totals, and selected delivery method. Each user can place multiple orders (One-to-Many relationship).
- **CheckoutOrderitem**: Represents individual items within an order, including product details and quantity. Each order can contain several order items (One-to-Many relationship).
  
### 3. Products
- **ProductsHennaproduct**: Defines the products available for purchase, with attributes such as SKU, name, description, and price. Each product can be linked to multiple order items (Many-to-One relationship).
- **ProductsDiscount**: Represents promotional discounts that can be applied to multiple products, supporting flexible marketing strategies (Many-to-Many relationship).

### 4. Delivery
- **CheckoutDelivery**: Manages various delivery options available to users. Each order can specify a delivery type, allowing for user choice (One-to-Many relationship).

### 5. Authentication and Permissions
- **AuthGroup**: Defines user groups for managing permissions.
- **AuthPermission**: Contains permissions linked to specific actions and content types, allowing for fine-grained access control.

### 6. Social Accounts
- **SocialaccountSocialaccount**: Manages social media account links for users, supporting OAuth authentication methods.

## Relationships
- **User - Profile (One-to-One)**: Each user has one associated profile.
- **User - Order (One-to-Many)**: A user can place multiple orders.
- **Order - OrderItem (One-to-Many)**: Each order can include several items.
- **OrderItem - Product (Many-to-One)**: Many order items can link back to a single product.
- **Products - Discount (Many-to-Many)**: Many products can have multiple discounts applied.
- **Order - Delivery (One-to-Many)**: Each order can specify one delivery method from various available options.

Henna Store data schema is designed to ensure efficient user management and order processing while supporting product promotions and diverse delivery methods. It is structured for scalability and flexibility as the Henna Store application grows, providing a solid foundation for further development and features.

---

## Testing
The app's functionality was also tested by friends and family. Their feedback was invaluable in identifying any issues and making necessary improvements.

For a detailed list of all testing steps taken, please refer to [TESTING.md](documentation/TESTING.md)

## Deployment

- **App Deployment:** The Henna Store app was deployed on Heroku, a cloud platform that facilitates easy and scalable application hosting. For more information about Heroku, click [here](https://www.heroku.com/).

- **Database Deployment:** The PostgreSQL database is used for data management, provided by Code Institute for students. More information about PostgreSQL can be found [here](https://www.postgresql.org/).

- **Static Files Deployment:** The app utilises Amazon S3 for hosting static files, ensuring efficient file storage and delivery. Learn more about S3 [here](https://aws.amazon.com/s3/).

- **Stripe Payments Integration:** The app incorporates Stripe for secure payment processing, including payment hooks and setup. Find out more about Stripe [here](https://stripe.com/docs).

The deployment process comprised several steps to guarantee the successful and efficient deployment of the Henna Store app on Heroku. For a comprehensive guide, please refer to [DEPLOYMENT.MD](documentation/DEPLOYMENT.md) for all deployment details and instructions.

---

### Planned Improvements

- **User Reviews and Ratings**  
  **Description:** Enable users to rate and leave reviews for products, encouraging community interaction and feedback.  
  **Reason for Delay:** Setting up a moderation system for user-submitted content is complex and requires time to implement correctly.

- **Order Tracking System**  
  **Description:** Offer customers real-time tracking information for their orders after purchase.  
  **Reason for Delay:** Integrating an effective tracking solution requires substantial backend adjustments and testing.

- **Promotional Discounts Feature**  
  **Description:** Introduce the option for users to apply discount codes during the checkout process.  
  **Reason for Delay:** Building a flexible system to manage and validate various discount codes needs detailed planning and development.

- **User Engagement Analytics**  
  **Description:** Create reports on user activity and product performance to gain better insights and inform decisions.  
  **Reason for Delay:** Developing advanced reporting features with customisable metrics involves significant coding and testing.


While I aim to implement these enhancements to improve the Henna Store app, certain features may encounter delays due to their complexity and the time required for development. I am dedicated to continuously refining the app and will prioritise features based on user feedback and available resources.

---

## Tools and Technologies Used

- **Backend:**
  - **[Django](https://www.djangoproject.com/)**: The web framework managing server-side logic and interactions.
  - **[Python](https://www.python.org/)**: The primary programming language for backend development.
  - **[PostgreSQL](https://www.postgresql.org/)**: A robust relational database used for handling data storage and queries.

- **Frontend:**
  - **[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)** / **[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)**: Utilised for structuring and styling the user interface.
  - **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**: Enhances the interactivity of the application.

- **Payment Processing:**
  - **[Stripe](https://stripe.com/)**: Used to handle secure card payments and payment intent functionalities.

- **Deployment and Version Control:**
  - **[Heroku](https://www.heroku.com/)**: For deploying and managing the application.
  - **[GitHub](https://github.com/)**: For version control and collaboration.

- **File Storage:**
  - **[AWS S3](https://aws.amazon.com/s3/)**: Used to manage static files and media storage for reliable content delivery.

---
## Other Tools

- **Image Resizing:** [Birme.net](https://www.birme.net/) was used to resize images.
- **Wireframing:** [Balsamiq](https://balsamiq.com/) helped create wireframes for the application.
- **Performance Testing:** [Lighthouse](https://developers.google.com/web/tools/lighthouse) was employed to evaluate and optimise the app’s performance.
- **HTML & JavaScript Validation:** [HTMLHint](https://htmlhint.com/) and [JSHint](https://jshint.com/) were used to ensure clean and error-free code.
- **Image Editing:** [GIMP](https://www.gimp.org/) was used for image editing and custom graphics creation.

---  

## Credits

- **Background Images:** Images sourced from [PNGTree](https://www.pngtree.com/) and [Freepik](https://www.freepik.com/).
- **Favicon:** Created using a [favicon generator](https://www.favicon-generator.org/).

---

#### Research Websites

- **Django Documentation:** Learn more about Django at [Django Docs](https://docs.djangoproject.com/).
- **PostgreSQL Documentation:** Explore PostgreSQL's capabilities at [PostgreSQL Docs](https://www.postgresql.org/docs/).
- **Stripe Documentation:** Discover Stripe's functionalities at [Stripe Docs](https://stripe.com/docs).
- **W3Schools:** Comprehensive tutorials and references on HTML, CSS, JavaScript, and more. Visit [W3Schools](https://www.w3schools.com/).
- **MDN Web Docs:** Detailed documentation for web development technologies, including HTML, CSS, and JavaScript. Visit [MDN Web Docs](https://developer.mozilla.org/).
- **Stack Overflow:** A community platform to find answers to coding questions and learn from others. Visit [Stack Overflow](https://stackoverflow.com/).
- **GitHub Learning Lab:** Learn about version control and collaboration with GitHub tutorials. Visit [GitHub Learning Lab](https://lab.github.com/).

---

## Acknowledgments

- **Julia Konovalova:** Thank you for your invaluable guidance throughout this project.
- **Jonathan Jacobson:** I appreciate your support and insights as my tutor.
- **Code Institute Community:** For their help and support during development.
- **Boutique Ado and Hello Django:** I found these walkthrough projects on the Code Institute learning platform to be immensely helpful in enhancing my understanding of Django.
- **Family and Friends:** For their encouragement and understanding during my learning journey.
- **Online Coding Communities:** For providing platforms like Stack Overflow and Discord, where I could seek help and share knowledge.
- **Tutorial Authors:** Appreciation for all the authors of tutorials and blogs that have guided me through various challenges.

---

## Reflection on Commit Practices

I acknowledge that my commit messages may not consistently adhere to best practices. I strive to improve by using commit types such as:

- **feat:** A new feature added.
- **fix:** A bug fix has been implemented.
- **chore:** Changes that do not relate to a fix or feature.
- **refactor:** Code that has been restructured without adding features or fixing bugs.
- **docs:** Updates to documentation files.

---
### Personal Improvements

- **Improved Code Readability**  
  **Description:** I plan to enhance the readability of my code by adopting consistent naming conventions, maintaining proper indentation, and using clear comments only when necessary. This will help others (and my future self) understand the code more easily.  
  **Reason for Focus:** Clearer code is easier to maintain, debug, and extend, especially as projects grow in complexity.

- **Better Git Commit Practices**  
  **Description:** I aim to improve my commit messages by making them more descriptive, using a standard format, and ensuring each commit represents a single logical change.  
  **Reason for Focus:** Well-structured commit history makes it easier to track changes and manage version control, especially when collaborating with others.

- **Refactoring for Efficiency**  
  **Description:** I intend to revisit my code regularly to refactor and optimise it for better performance and readability. This will include reducing redundancy and applying principles such as DRY (Don’t Repeat Yourself).  
  **Reason for Focus:** Cleaner, more efficient code improves overall project quality and helps prevent bugs.

- **Enhanced Debugging Skills**  
  **Description:** I want to strengthen my ability to identify and resolve issues more systematically by using print statements, logging, and breakpoints effectively.  
  **Reason for Focus:** Efficient debugging saves time and leads to quicker problem resolution.

- **Regular Peer Reviews and Feedback**  
  **Description:** I plan to actively seek out feedback from peers and mentors on my code, using it to identify areas for improvement and refine my programming style.  
  **Reason for Focus:** Peer reviews provide valuable perspectives and help improve code quality and learning through collaboration.

- **Consistent Documentation**  
  **Description:** I will document my code more thoroughly, including README files, function descriptions, and project structure outlines to provide a clear guide for future development.  
  **Reason for Focus:** Good documentation ensures that the purpose and functionality of the code are clear, making it easier for others to use and contribute to the project.
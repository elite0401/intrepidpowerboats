# Version 0.3.0 (Sprint 3)

* **Owner's portal**
  * [#12 - Owner login and logout](#12): Owners can log in to the site, enabling their personal 'Owner's portal' site functionality.
  * [#27 - BUG: Forum](#27): Fix a few forum bugs:
      * External links now function properly.
      * Restore breadcrumbs, links to search and profile editing.
      * Fix topic titles and links for imported old data.
  * [#117 - Cinemagraph videos autoloop](#117): Add autoloop for cinemagraph videos.
  * [#15 - Process report](#15): Allow user to see his boat report and admin to change it
  * [#152 - Edit user's boat name](#152): Allow user to edit their boat name from the Dashboard.

* **All Models page**
  * [#138 - Boat names in footer](#138): The boat names in the footer now link to their respective model pages.

* **Boat Model page**
  * [#146 - Dropdown selector](#146): A user can navigate to a different model's page using the dropdown selector.
  * [#24 - Optional equipment](#24): This tab shows a list of optional features a user may select. Hovering over an item produces a thumbnail tooltip with an image or a video.
  * [#118 - BUG: Reset sample colors](#118): When a user resets a chosen color in 'build-a-boat', the color sample now resets along with the image.

* **Intrepid Difference page**
  * [#143 - BUG: Testimonial form](#143): The 'share testimonial' form is now displaying correctly again.

* **Events page**
  * [#153 - BUG: section not set up correctly](#143): Event items now link to an external site instead of a full article on the site.

# Version 0.2.0 (Sprint 2)

* **Home page**
  * [#106 - Add export to CSV action on Newsletter admin](#106): Newsletter subscriber list can be exported as a CSV file.
* **Contact**
  * [#34 - Contact page](#34): Add a contact page incluidng (editable) staff member information and a 'Contact us' form.
* **CMS Administration**
  * [#101 - Filter plugin types](#101): CMS placeholders now receive only relevant plugins. Text plugins and fields allow rich text editing.
* **Misc.**
  * [#29 - Gear](#29): Add an external link controlled by settings.
* **All Models page**
  * [#73 - Build a boat](#73): Allow to select hull colors, motor and features. Also allow to share by email or on Facebook

# Version 0.1.0 (Sprint 1)

* **Home page**
  * [#6 - Home](#6): Implement home page and allow configuring the background slider
  * [#32 - Newsletter signup](#32): Users can subscribe to the newsletter from a modal on the home page. Subscriber information is archived in the database.
* [#28 - Pre-Owned](#28): Allow to set a external link by settings
* [#51 - Forum](#51): Add a django forum app and migrate old forum data
* [#37 - i18n](#37): Add i18n support. English and Spanish (only placeholders)
* **All Models page**
  * [#17 - All models](#17): Show a view with a list of boat model groups.
  * [#18 - All models comparison](#18): Show group boats modal with checkboxes and the comparison modal.
* **Intrepid Difference page**: CMS-editable page.
  * [#7 - About](#7): Page tab including images, text, and a list of user-sent 'Testimonials'.
  * [#8 - Share testimonial (share video)](#8): Allow users to upload and image or video.
  * [#9 - One-of-a-kind](#9): Page tab including text.
  * [#10 - Versatility](#10): Page tab including text sections with images.
  * [#11 - Craftmanship](#11): Another page tab including text sections with images.

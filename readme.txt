Modules 
=================
1. Donations
2. Event Management
3. Email Notification
4. Blogs
5. Environment news and updates 
6. Recycling Tips
7. Chat for inquiry

Databases :

event_category -
> id
> catagory 

volunteer - 
> id
> first_name
> last_name
> Email
> contact 
> gender
> dob
> age_limit (18-60)
> full_address 
> profile_pic 
> participation_history
> joined_on
> is_active
> is_blocked 

donation:
> id 
> donated_by
> amount 
> date_time 
> if_donated_for_event (true/false)
> event_info (fk-event)
> donation_history


organizer - 
> id
> event_name
> category(fk)
> date_from
> date_to
> time_from
> time_to
> banner
> about 
> venue
> Create date_time 
> Update date_time 
> is_expired
> is_active
> is_volunteer_required 
> volunteers
> volunteer_capacity
> sponsers
> donations
> terms_condition



Module 1 : Organizer (5 Jun)
Fields - 
> Event Name 
> Event catagory 
> Organizer - company name 
> Images 
> Source Link 
> Create date_time 
> Update date_time 
> Expired
> Description / About 
> Venue
> volunteers required - (Max Capacity - 40)
> volunteers requirements 
> active_status 
> sponsers - list of names 
> Donate 
> Terms and Conditions 
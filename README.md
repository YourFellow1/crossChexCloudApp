This is my first trip into creating a standalone program.
The prompt? CrossChex Cloud has a pretty terribly user interface online. Our usecase is to have an accurrate list of who's onsite when there's an emergency.
Other timeclock apps are expensive - $2.50-$5.00 per person per month. For something that is supposed to save money (by saving time while increasing accuracy), it wasn't going to be worth pitching to corporate.
Instead, we took a free cloud system with relatively cheap timeclock devices, and we decided to add a way to get the data and work with it.
There's an OKAY list of data that can be pulled from API requests. So I set out to learn what that meant and make an app.

Long-term, I want this to use the Kivy framework and create a GUI that will be on our managers' phones. Until then, a command prompt app to pull lists at a given time is the focus.
On the backend, since we have the data, we also want to keep track of hours worked onsite by each contractor group on a daily, weekly, and monthly basis. This data will be available to the SM onsite.

For other time inquiries, it will be under lock n key for upper management to handle themselves.

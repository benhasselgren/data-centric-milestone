<h6>Ben Hasselgren</h6>
<h1> Data Centric Milestone Project  </h1>

<h3>Purpose</h3>
<p>
    The purpose of this project is to create a website that allows users
    to sign up to a cooking recipe website. On this website they can create their own cooking recipes and 
    then share those recipes to other people. The user can also view all their own recipes they have made and then edit or
    delete them. The user can also query the recipes database and view everone elses recipes and rate them.
</p>

<h3>Functionality/Technologies</h3>
<p>
    This website has lots of functionality. One functioniality is that it's resposnive. It uses materialize which is webdevelopment library
    like bootstrap. Using the provided classes and javascript code, the website has a very resposive interface and adaps to screen sizes.
    The website allows the user to create an account which they can then log into to make their own recipes. This was possible because of
    the Flask framework. This technology allowed lots of functionality. Mainly to create url routes to guide users around the website 
    with their own unique username and allow them to create, edit and delete recipes and also to let them view and query other users recipes.
    Another piece of functionality is the ratings of recipes. The user can also like other peoples recipes. Flask/Jinja also allowed me to easily
    create html through the use of passing through data in the url and then loop through items and create html structure for those items without
    having to write things out over and over again. This also made my code way more readable.
</p>

<p> 
    All this data created by the useris kept in a database. The database was set up using mysql. I firest created a database schema which is where I identified the strucure and relationships of my tables. I started by creating a user table. I then added a recipe table which used the user id aas a foreign key. I then added an ingredient table and method table that used the recipe id of the relevant recipe as a foreign key. I then added a rating table which used the recipe id of a relevant recipe as a foreign key. If i were to do this again, I owuld have used the user id as another foreign key. This would have allowed me to reutrn users liked reciped and display them in their profile or also tell the user if they had already liked a recipe, etc. To then create tables, mysqlalchemy-flask was installed. Rather than writing sql, I instead was able to to write python code. Each table was represented by a class. This made it far easier to query, delete, add and update all the
    data in the database. 
</p>

<h3>Testing/Deployment</h3>
<p>
    This website was tested in different ways. MySqlWorkbench(GUI) was installed to view the database in a more readable way. This allowed me to check
    if the functionality in my code was working as I could see if the correct data was being added, removed in the database. I also used chrome developer tools
    to test if there was anything wrong with my html, css or javascript files. I also made use of flasks/jinja's error page that appeared when my code had errors in it. This helped me spot things wrong in my code quickly.
</p>
<p>
    This website was deployed to heroku. I created a heroku app and then pushed my code to it. To ensure it worked I had to add some config variables on the heroku dashboard. I then had to add a procfile and a reuiqrments.txt file so heroku would know how to set up my app. The main issue with deploying my data was migrating all the data from the database to heroku. I didn't want to migrate to postgres in this project so I found a heroku resource called ClearDB. It is basically what heroku uses to store mysql databases. It was easy to migrate. I copied my cleardb config value I was given and placed it in an environment variable in my local code. This then migrated my current, local mysql database to the cleardb one on heroku.
</p>
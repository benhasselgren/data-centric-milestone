<h6>Ben Hasselgren</h6>
<h1> Data Centric Milestone Project  </h1>

<a href="" target="_blank"><span>Site currently unavailable</span></a>

<h3>Purpose</h3>
<p>
    The purpose of this project is to create a website that allows users
    to sign up to a cooking recipe website. On this website they can create their own cooking recipes and 
    then share those recipes to other people. The user can also view all their own recipes they have made and then edit or
    delete them. The user can also query the recipes database and view everone elses recipes and rate them.
</p>

<small>Before following the tutorial take note that the databse uses cleardb and this seems to cause some connection errors sometimes and the application will stop for a second. If this happens, just refresh the page and continue using it. My plan is to use postgres databses from now on when using heroku.</small>

<h3>Quick Tutorial</h3>
<ol>
    <li>First, register an account. This can be achieved by entering in your details in the sign up form. As user authentication was an option in this project it is not a very robust authentication so for this tutorial make sure your email is unique. </li>
    <li>Once registered and signed in you will be directed to your profile.</li>
    <ul>
        <h5>Profile</h5>
        <li>In your profile you can add recipes pressing the add recipe button. It will also recipes you have created.</li>
        <li>You can also delete and edit recipes</li>
    </ul>
    <li>Now click on search recipes in the navbar</li>
    <ul>
        <h5>Searching for recipes</h5>
        <li>This page allows you to build a custom query. The more fields you add values to will make your query more specific. The only field that can't be changed is the temprature so make sure it matches recipe tempratures that exist. (I plan to make this field a range instead of just one value to you can search for recipes more generally.</li>
        <li>The query will return a bunch of relevant recipes</li>
        <li>These recipes can be upvoted and also clicked on to be viewed in more detail.</li>
    </ul>
    <li>Now click on add recipes in the navbar</li>
    <ul>
        <h5>Adding recipes</h5>
        <li>The add recipe page allows you to create recipes easily</li>
        <li>Enter in all the field and don't leave anything blank</li>
        <li>Then click create recipe.</li>
    </ul>
    <li>Now click on statistics</li>
    <ul>
        <h5>Statistics</h5>
        <li>The statistics page shows a summary of the recipes databse in graphs using dc/d3 javscript library.</li>
        <li>You can click on the graphs bars to drill the graphs down into filtered graphs.</li>
        <li>The graphs are read from a csv file. This has caused some issues because of heroku, so the graphs might not be updated correctly sometimes.</li>
    <li>Now log out. Thats all you need to know to use this website. Enjoy!</li>
</ol>

<h3>Functionality/Technologies</h3>
<p>
    This website has lots of functionality. One functioniality is that it's resposnive. It uses materialize which is webdevelopment library
    like bootstrap. Using the provided classes and javascript code, the website has a very resposive interface and adaps to screen sizes.
</p>
<p>
    The website allows the user to create an account which they can then log into to make their own recipes. This was possible because of
    the Flask framework. This technology allowed lots of functionality. Mainly to create url routes to guide users around the website 
    with their own unique username and allow them to create, edit and delete recipes and also to let them view and query other users recipes.
</p>
<p>
    Another piece of functionality is the ratings of recipes. The user can like other peoples recipes by pressing the upvote button after searching for recipes.
</p>
<p>
    Flask/Jinja also allowed me to easily create html through the use of passing through data in the url and then loop through items and create html structure for those items without having to write things out over and over again. This also made my code way more readable.
</p>

<p> 
    All this data created by the useris kept in a database. The database was set up using mysql. I firest created a database schema which is where I identified the strucure and relationships of my tables. I started by creating a user table. I then added a recipe table which used the user id aas a foreign key. I then added an ingredient table and method table that used the recipe id of the relevant recipe as a foreign key. I then added a rating table which used the recipe id of a relevant recipe as a foreign key. If i were to do this again, I owuld have used the user id as another foreign key. This would have allowed me to reutrn users liked reciped and display them in their profile or also tell the user if they had already liked a recipe, etc. 
</p>
<p>
    To then create tables, mysqlalchemy-flask was installed. Rather than writing sql, I instead was able to to write python code. Each table was represented by a class. This made it far easier to query, delete, add and update all the
    data in the database. 
</p>

<h3>Testing</h3>
<p>
    This website was tested in different ways. MySqlWorkbench(GUI) was installed to view the database in a more readable way. This allowed me to check
    if the functionality in my code was working as I could see if the correct data was being added, removed in the database. I also used chrome developer tools
    to test if there was anything wrong with my html, css or javascript files. I also made use of flasks/jinja's error page that appeared when my code had errors in it. This helped me spot things wrong in my code quickly.
</p>
<p>
    I also did some manual tests. Here are a couple examples
</p>
<table>
    <tr>
        <th>Test</th>
        <th>Input</th>
        <th>Expected output</th>
        <th>Output</th>
        <th>Pass?</th>
    </tr>
    <tr>
        <td>Testing to see if the correct user is logged in by checking to see if the correct username is displayed in the profile page.</td>
        <td>Signed in as admin</td>
        <td>url = "http://data-centric-dev-milestone.herokuapp.com/my_cookbook/admin"</td>
        <td>http://data-centric-dev-milestone.herokuapp.com/my_cookbook/admin</td>
        <td>Yes</td>
    </tr>
    <tr>
        <td>Testing to see if the correct recipe('s) appear when searching</td>
        <td>Searching recipes where tempratures = 120</td>
        <td>Results should shows recipes: Spaghetti Bolognese and Macaroni Cheese</td>
        <td>Results showed recipes: Spaghetti Bolognese and Macaroni Cheese1</td>
        <td>Yes</td>
    </tr>
</table>
<h3>Deployment</h3>
<p>
    This website was deployed to heroku. I created a heroku app and then pushed my code to it. To ensure it worked I had to add some config variables on the heroku dashboard. I then had to add a procfile and a reuiqrments.txt file so heroku would know how to set up my app. The main issue with deploying my data was migrating all the data from the database to heroku. I didn't want to migrate to postgres in this project so I found a heroku resource called ClearDB. It is basically what heroku uses to store mysql databases. It was easy to migrate. I copied my cleardb config value I was given and placed it in an environment variable in my local code. This then migrated my current, local mysql database to the cleardb one on heroku. UPDATE: AFTER USING MY APPLICATION I HAVE REALISED THET CLEARDB CAUSES CONNECTION ERRORS A LOT. WOULD SUGGEST JUST USING POSTGRES WHEN MIGRATING YOUR DATABASES.
</p>

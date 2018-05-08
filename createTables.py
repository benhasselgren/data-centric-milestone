from db import db
from db import User

"""-------------------------------Create Tables--------------------------------"""

db.drop_all()
db.create_all()

admin = User(first='Ben', 
			 last='Hasselgren',
			 username='benhasselgren',
			 email='admin@example.com',
			 password='lol')

db.session.add(admin)
db.session.commit()


"""
<h2>Recipe</h2>
Receipe: <input data-bind="value: recipeName"/>
<table>
    <thead><tr>
        <th>Ingredient</th><th></th>
    </tr></thead>
    
    <tbody data-bind="foreach: ingredients">
    <tr>
      <td><input data-bind="value: name"/></td>
      <td><button data-bind="click: $parent.removeMe">Remove</button></td>
    </tr>
    </tbody>
</table>
<button data-bind="click: addIngredient">Add Ingredient</button>
<button data-bind="click: sendToServer">Commit</button>

// Class to represent a row in the seat reservations grid
function Ingredient(name) {
    var self = this;
    self.name = name;
    
}

// Overall viewmodel for this screen, along with initial state
function ReservationsViewModel() {
    var self = this;
    
    self.recipeName = ko.observable('dfsdf');
     


    // Editable data
    self.ingredients = ko.observableArray([
        new Ingredient("Steve"),
        new Ingredient("Bert")
    ]);
    
    self.addIngredient = function() {
        self.ingredients.push(new Ingredient("New one"));
    }
    
    self.removeMe = function(itm) {
        self.ingredients.remove(itm);
    }
    
    self.sendToServer = function() {
        var ingredients = [];
        for (i = 0; i < self.ingredients().length; i++)
        {
           ingredients.push(self.ingredients()[i].name);
        }
        alert({recipe: self.recipeName, ingredients: ingredients});
    }
}

ko.applyBindings(new ReservationsViewModel());
"""

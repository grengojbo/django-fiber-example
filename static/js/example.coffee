class Person extends Backbone.Model
     defaults:
        name: 'Noname'
        job: 'босс'
        age: 38
     
 person  = new Person name: "Oleg"

 console.console.log person.toJSON()

 class PersonView extends Backbone.View
     initialize: ->
         @model.on 'someEvent', @doThis

    doThis: =>
        console.log this
     
person = new Person
personView = new PersonView model: person

person.trigger 'someEvent'
 
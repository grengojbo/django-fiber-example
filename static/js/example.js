// Generated by CoffeeScript 1.6.2
var Person, PersonView, person, personView, _ref, _ref1,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  _this = this;

Person = (function(_super) {
  __extends(Person, _super);

  function Person() {
    _ref = Person.__super__.constructor.apply(this, arguments);
    return _ref;
  }

  Person.prototype.defaults = {
    name: 'Noname',
    job: 'босс',
    age: 38
  };

  return Person;

})(Backbone.Model);

person = new Person({
  name: "Oleg"
});

console.console.log(person.toJSON());

PersonView = (function(_super) {
  __extends(PersonView, _super);

  function PersonView() {
    _ref1 = PersonView.__super__.constructor.apply(this, arguments);
    return _ref1;
  }

  PersonView.prototype.initialize = function() {
    return this.model.on('someEvent', this.doThis);
  };

  return PersonView;

})(Backbone.View);

({
  doThis: function() {
    return console.log(_this);
  }
});

person = new Person;

personView = new PersonView({
  model: person
});

person.trigger('someEvent');
